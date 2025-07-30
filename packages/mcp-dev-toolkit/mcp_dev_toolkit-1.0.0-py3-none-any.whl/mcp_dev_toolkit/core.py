"""
Core SDK classes and functions for MCP Development Toolkit
"""

import asyncio
import inspect
import json
import logging
import traceback
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type, Union, get_type_hints, TYPE_CHECKING
import functools
import uuid

# External dependencies
try:
    import pydantic
    from pydantic import BaseModel, ValidationError
except ImportError as e:
    raise ImportError(f"Missing required dependency: {e}. Run: pip install mcp-dev-toolkit[full]")

# MCP imports
try:
    import mcp.types as types
    from mcp.server import Server
    from mcp.server.models import InitializationOptions
    from mcp.server import NotificationOptions
except ImportError:
    raise ImportError("MCP library not found. Run: pip install mcp")

# Type checking imports to avoid circular dependencies
if TYPE_CHECKING:
    from .middleware import Middleware


class ToolType(Enum):
    """Types of tools that can be created"""
    SIMPLE = "simple"
    AGENTIC = "agentic"
    WORKFLOW = "workflow"
    INTEGRATION = "integration"
    UTILITY = "utility"


class MiddlewarePhase(Enum):
    """Phases when middleware can execute"""
    PRE_EXECUTION = "pre"
    POST_EXECUTION = "post"
    ERROR_HANDLING = "error"


@dataclass
class ToolMetadata:
    """Metadata for MCP tools"""
    name: str
    description: str
    tool_type: ToolType
    tags: List[str] = field(default_factory=list)
    examples: List[Dict[str, Any]] = field(default_factory=list)
    version: str = "1.0.0"
    author: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class InputParameter:
    """Input parameter specification"""
    name: str
    param_type: Type
    required: bool = True
    default: Any = None
    description: str = ""
    enum_values: Optional[List[Any]] = None


@dataclass
class ToolSchema:
    """Complete schema for a tool"""
    metadata: ToolMetadata
    input_parameters: List[InputParameter]
    output_schema: Optional[Dict[str, Any]] = None
    handler_function: Optional[Callable] = None


class MCPDevelopmentSDK:
    """Main SDK class for building MCP tools"""

    def __init__(self, name: str = "mcp-tools", version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.tools: Dict[str, ToolSchema] = {}
        self.middleware: List['Middleware'] = []
        self.error_handlers: Dict[Type[Exception], Callable[..., Any]] = {}
        self.gateway_client = None

        # Import middleware classes here to avoid circular imports
        from .middleware import ValidationMiddleware, LoggingMiddleware, PerformanceMiddleware

        # Add default middleware
        self.add_middleware(ValidationMiddleware())
        self.add_middleware(LoggingMiddleware())
        self.add_middleware(PerformanceMiddleware())

        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("mcp_sdk")

    def set_gateway(self, gateway_client):
        """Set gateway client for API integrations"""
        self.gateway_client = gateway_client
        return self

    def add_middleware(self, middleware: 'Middleware'):
        """Add middleware to the stack"""
        self.middleware.append(middleware)
        self.middleware.sort(key=lambda m: m.priority)
        return self

    def add_error_handler(self, error_type: Type[Exception], handler: Callable[..., Any]):
        """Add custom error handler"""
        self.error_handlers[error_type] = handler
        return self

    def tool(self,
             name: Optional[str] = None,
             description: Optional[str] = None,
             tool_type: ToolType = ToolType.SIMPLE,
             tags: Optional[List[str]] = None,
             examples: Optional[List[Dict[str, Any]]] = None,
             author: Optional[str] = None) -> Callable[..., Any]:
        """Decorator to register MCP tools"""

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            tool_name = name or func.__name__
            tool_description = description or func.__doc__ or f"Tool: {tool_name}"

            # Import here to avoid circular imports
            from .schema import SchemaExtractor

            # Extract input parameters
            input_parameters = SchemaExtractor.extract_input_parameters(func)

            # Create tool metadata
            metadata = ToolMetadata(
                name=tool_name,
                description=tool_description,
                tool_type=tool_type,
                tags=tags or [],
                examples=examples or [],
                author=author
            )

            # Create tool schema
            tool_schema = ToolSchema(
                metadata=metadata,
                input_parameters=input_parameters,
                handler_function=func
            )

            # Wrap function with middleware
            wrapped_func = self._wrap_function(func, tool_schema)

            # Register tool
            self.tools[tool_name] = tool_schema

            self.logger.info(f"Registered tool: {tool_name}")

            return wrapped_func

        return decorator

    def _wrap_function(self, func: Callable[..., Any], tool_schema: ToolSchema) -> Callable[..., Any]:
        """Wrap function with middleware execution"""

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Inject gateway if function expects it
            if 'gateway' in inspect.signature(func).parameters:
                kwargs['gateway'] = self.gateway_client

            try:
                # Pre-execution middleware
                for middleware in self.middleware:
                    result = await middleware.process_pre(tool_schema, args, kwargs)
                    if result is not None:
                        args, kwargs = result

                # Execute function
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)

                # Post-execution middleware
                for middleware in reversed(self.middleware):
                    processed_result = await middleware.process_post(tool_schema, result)
                    if processed_result is not None:
                        result = processed_result

                return result

            except Exception as error:
                # Error handling middleware
                for middleware in self.middleware:
                    handled_result = await middleware.process_error(tool_schema, error, args, kwargs)
                    if handled_result is not None:
                        return handled_result

                # Custom error handlers
                for error_type, handler in self.error_handlers.items():
                    if isinstance(error, error_type):
                        return await handler(error, tool_schema, args, kwargs)

                # Re-raise if no handler found
                raise

        return wrapper

    def integration(self, service: str, endpoint: Optional[str] = None) -> Callable[..., Any]:
        """Decorator for API integrations"""

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:

            @functools.wraps(func)
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                # Auto-inject gateway
                kwargs['gateway'] = self.gateway_client
                kwargs['service'] = service
                kwargs['endpoint'] = endpoint

                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    return {
                        "error": str(e),
                        "service": service,
                        "endpoint": endpoint,
                        "timestamp": datetime.now().isoformat()
                    }

            return wrapper

        return decorator

    def get_tool_schemas(self) -> Dict[str, Dict[str, Any]]:
        """Get all tool schemas in JSON format"""
        # Import here to avoid circular imports
        from .schema import SchemaExtractor
        
        schemas = {}
        for tool_name, tool_schema in self.tools.items():
            json_schema = SchemaExtractor.generate_json_schema(tool_schema.input_parameters)
            schemas[tool_name] = {
                "metadata": asdict(tool_schema.metadata),
                "input_schema": json_schema,
                "output_schema": tool_schema.output_schema
            }
        return schemas

    def generate_mcp_server(self, output_dir: str = ".", server_name: Optional[str] = None) -> str:
        """Generate complete MCP server"""
        try:
            from .generators import MCPServerGenerator

            actual_server_name = server_name or self.name
            return MCPServerGenerator.generate(
                server_name=actual_server_name,
                tools=self.tools,
                output_dir=output_dir
            )
        except ImportError:
            raise ImportError("Code generation requires full dependencies. Run: pip install mcp-dev-toolkit[full]")

    def generate_openapi_spec(self) -> Dict[str, Any]:
        """Generate OpenAPI specification"""
        try:
            from .generators import OpenAPIGenerator

            return OpenAPIGenerator.generate(self.tools, self.name, self.version)
        except ImportError:
            raise ImportError("Code generation requires full dependencies. Run: pip install mcp-dev-toolkit[full]")

    def create_mcp_app(self) -> Server:
        """Create MCP server application"""
        app = Server(self.name)

        @app.list_tools()
        async def list_tools() -> List[types.Tool]:
            tools_list = []
            for tool_name, tool_schema in self.tools.items():
                json_schema = SchemaExtractor.generate_json_schema(tool_schema.input_parameters)

                tools_list.append(types.Tool(
                    name=tool_name,
                    description=tool_schema.metadata.description,
                    inputSchema=json_schema
                ))

            return tools_list

        @app.call_tool()
        async def call_tool(name: str, arguments: dict) -> List[types.TextContent]:
            try:
                if name not in self.tools:
                    return [types.TextContent(
                        type="text",
                        text=f"❌ Unknown tool: {name}"
                    )]

                tool_schema = self.tools[name]
                handler = tool_schema.handler_function

                # Execute tool with middleware
                wrapped_handler = self._wrap_function(handler, tool_schema)
                result = await wrapped_handler(**arguments)

                return [types.TextContent(
                    type="text",
                    text=json.dumps(result, indent=2, default=str)
                )]

            except Exception as e:
                self.logger.error(f"Tool execution failed: {e}")
                return [types.TextContent(
                    type="text",
                    text=f"❌ Error: {str(e)}"
                )]

        return app

    async def run_server(self, app: Optional[Server] = None):
        """Run MCP server"""
        if app is None:
            app = self.create_mcp_app()

        from mcp.server.stdio import stdio_server

        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name=self.name,
                    server_version=self.version,
                    capabilities=app.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )


def create_sdk(name: str = "mcp-tools", version: str = "1.0.0") -> MCPDevelopmentSDK:
    """Create a new SDK instance"""
    return MCPDevelopmentSDK(name, version)
