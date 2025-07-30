"""
Tests for core SDK functionality
"""

import pytest
import asyncio
from typing import Dict, Any

from mcp_dev_toolkit import create_sdk, ToolType
from mcp_dev_toolkit.core import MCPDevelopmentSDK, ToolMetadata, InputParameter, ToolSchema


class TestMCPDevelopmentSDK:
    """Test the main SDK class"""

    def test_sdk_creation(self):
        """Test SDK instance creation"""
        sdk = create_sdk("test-sdk", "1.0.0")
        
        assert isinstance(sdk, MCPDevelopmentSDK)
        assert sdk.name == "test-sdk"
        assert sdk.version == "1.0.0"
        assert len(sdk.tools) == 0
        assert len(sdk.middleware) > 0  # Default middleware should be added

    def test_tool_registration(self, sample_sdk):
        """Test tool registration with decorator"""
        
        @sample_sdk.tool(
            name="test_tool",
            description="A test tool",
            tool_type=ToolType.SIMPLE,
            tags=["test"]
        )
        async def test_tool(name: str, count: int = 1) -> Dict[str, Any]:
            return {"message": f"Hello {name}", "count": count}
        
        assert "test_tool" in sample_sdk.tools
        tool_schema = sample_sdk.tools["test_tool"]
        
        assert isinstance(tool_schema, ToolSchema)
        assert tool_schema.metadata.name == "test_tool"
        assert tool_schema.metadata.description == "A test tool"
        assert tool_schema.metadata.tool_type == ToolType.SIMPLE
        assert "test" in tool_schema.metadata.tags

    def test_tool_registration_without_name(self, sample_sdk):
        """Test tool registration using function name"""
        
        @sample_sdk.tool(description="Auto-named tool")
        async def auto_named_tool(param: str) -> str:
            return param
        
        assert "auto_named_tool" in sample_sdk.tools

    def test_parameter_extraction(self, sample_sdk):
        """Test parameter extraction from function signature"""
        
        @sample_sdk.tool()
        async def complex_tool(
            required_str: str,
            optional_int: int = 42,
            optional_bool: bool = False
        ) -> Dict[str, Any]:
            return {"result": "ok"}
        
        tool_schema = sample_sdk.tools["complex_tool"]
        params = tool_schema.input_parameters
        
        assert len(params) == 3
        
        # Check required parameter
        required_param = next(p for p in params if p.name == "required_str")
        assert required_param.required is True
        assert required_param.param_type == str
        
        # Check optional parameters
        optional_int_param = next(p for p in params if p.name == "optional_int")
        assert optional_int_param.required is False
        assert optional_int_param.default == 42
        assert optional_int_param.param_type == int

    def test_middleware_addition(self, sample_sdk):
        """Test adding custom middleware"""
        from mcp_dev_toolkit.middleware import Middleware
        
        class TestMiddleware(Middleware):
            def __init__(self):
                super().__init__(priority=100)
                self.pre_called = False
                self.post_called = False
            
            async def process_pre(self, tool_schema, args, kwargs):
                self.pre_called = True
                return None
            
            async def process_post(self, tool_schema, result):
                self.post_called = True
                return None
            
            async def process_error(self, tool_schema, error, args, kwargs):
                return None
        
        test_middleware = TestMiddleware()
        initial_count = len(sample_sdk.middleware)
        
        sample_sdk.add_middleware(test_middleware)
        
        assert len(sample_sdk.middleware) == initial_count + 1
        assert test_middleware in sample_sdk.middleware

    @pytest.mark.asyncio
    async def test_tool_execution(self, registered_sdk):
        """Test tool execution with middleware"""
        tool_schema = registered_sdk.tools["test_tool"]
        handler = tool_schema.handler_function
        
        # Execute the wrapped function
        wrapped_handler = registered_sdk._wrap_function(handler, tool_schema)
        result = await wrapped_handler(name="test", count=5)
        
        assert result["message"] == "Hello test"
        assert result["count"] == 5

    def test_get_tool_schemas(self, registered_sdk):
        """Test getting tool schemas in JSON format"""
        schemas = registered_sdk.get_tool_schemas()
        
        assert "test_tool" in schemas
        tool_data = schemas["test_tool"]
        
        assert "metadata" in tool_data
        assert "input_schema" in tool_data
        assert tool_data["metadata"]["name"] == "test_tool"
        assert tool_data["input_schema"]["type"] == "object"

    @pytest.mark.asyncio
    async def test_mcp_app_creation(self, registered_sdk):
        """Test MCP application creation"""
        app = registered_sdk.create_mcp_app()
        
        # Test that the app has the expected structure
        assert hasattr(app, 'name')
        assert app.name == registered_sdk.name


class TestToolMetadata:
    """Test ToolMetadata dataclass"""

    def test_tool_metadata_creation(self):
        """Test creating tool metadata"""
        metadata = ToolMetadata(
            name="test_tool",
            description="A test tool",
            tool_type=ToolType.SIMPLE,
            tags=["test", "example"],
            version="2.0.0",
            author="Test Author"
        )
        
        assert metadata.name == "test_tool"
        assert metadata.description == "A test tool"
        assert metadata.tool_type == ToolType.SIMPLE
        assert metadata.tags == ["test", "example"]
        assert metadata.version == "2.0.0"
        assert metadata.author == "Test Author"
        assert metadata.created_at is not None

    def test_tool_metadata_defaults(self):
        """Test tool metadata with default values"""
        metadata = ToolMetadata(
            name="simple_tool",
            description="Simple tool",
            tool_type=ToolType.UTILITY
        )
        
        assert metadata.tags == []
        assert metadata.examples == []
        assert metadata.version == "1.0.0"
        assert metadata.author is None


class TestInputParameter:
    """Test InputParameter dataclass"""

    def test_input_parameter_creation(self):
        """Test creating input parameter"""
        param = InputParameter(
            name="test_param",
            param_type=str,
            required=True,
            description="A test parameter"
        )
        
        assert param.name == "test_param"
        assert param.param_type == str
        assert param.required is True
        assert param.description == "A test parameter"
        assert param.default is None
        assert param.enum_values is None

    def test_input_parameter_with_enum(self):
        """Test input parameter with enum values"""
        param = InputParameter(
            name="choice_param",
            param_type=str,
            required=False,
            default="option1",
            enum_values=["option1", "option2", "option3"]
        )
        
        assert param.enum_values == ["option1", "option2", "option3"]
        assert param.default == "option1"
        assert param.required is False


class TestToolTypes:
    """Test ToolType enum"""

    def test_tool_type_values(self):
        """Test all tool type values"""
        assert ToolType.SIMPLE.value == "simple"
        assert ToolType.AGENTIC.value == "agentic"
        assert ToolType.WORKFLOW.value == "workflow"
        assert ToolType.INTEGRATION.value == "integration"
        assert ToolType.UTILITY.value == "utility"

    def test_tool_type_enum_usage(self, sample_sdk):
        """Test using tool types in registration"""
        for tool_type in ToolType:
            @sample_sdk.tool(tool_type=tool_type)
            async def test_func() -> str:
                return "test"
            
            # Clear for next iteration
            sample_sdk.tools.clear()


class TestErrorHandling:
    """Test error handling functionality"""

    def test_error_handler_registration(self, sample_sdk):
        """Test registering custom error handlers"""
        
        async def value_error_handler(error, tool_schema, args, kwargs):
            return {"error": "Custom value error", "original": str(error)}
        
        sample_sdk.add_error_handler(ValueError, value_error_handler)
        
        assert ValueError in sample_sdk.error_handlers
        assert sample_sdk.error_handlers[ValueError] == value_error_handler

    @pytest.mark.asyncio
    async def test_error_handling_in_execution(self, sample_sdk):
        """Test error handling during tool execution"""
        
        @sample_sdk.tool()
        async def failing_tool(should_fail: bool = True) -> str:
            if should_fail:
                raise ValueError("Test error")
            return "success"
        
        # Register error handler
        async def error_handler(error, tool_schema, args, kwargs):
            return {"handled": True, "error": str(error)}
        
        sample_sdk.add_error_handler(ValueError, error_handler)
        
        tool_schema = sample_sdk.tools["failing_tool"]
        wrapped_handler = sample_sdk._wrap_function(failing_tool, tool_schema)
        
        result = await wrapped_handler(should_fail=True)
        
        assert result["handled"] is True
        assert "Test error" in result["error"]
