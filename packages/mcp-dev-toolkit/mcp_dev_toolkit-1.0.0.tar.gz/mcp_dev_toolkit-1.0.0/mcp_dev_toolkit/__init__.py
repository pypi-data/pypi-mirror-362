#!/usr/bin/env python3
"""
MCP Development Toolkit - A comprehensive SDK for building MCP tools and servers

This package provides a complete development toolkit for creating Model Context Protocol (MCP) 
tools and servers with built-in middleware, validation, schema extraction, and code generation.

Key Features:
- Decorator-based tool registration
- Automatic schema extraction from Python functions
- Built-in middleware system (validation, logging, performance)
- Code generation for MCP servers and OpenAPI specs
- Integration support with external APIs
- Comprehensive error handling and validation

Quick Start:
    >>> from mcp_dev_toolkit import create_sdk, ToolType
    >>> 
    >>> # Create SDK instance
    >>> sdk = create_sdk("my-tools", "1.0.0")
    >>> 
    >>> # Register a tool
    >>> @sdk.tool(
    ...     name="greet_user",
    ...     description="Greet a user with a personalized message",
    ...     tool_type=ToolType.SIMPLE,
    ...     tags=["greeting", "utility"]
    ... )
    >>> async def greet_user(name: str, greeting: str = "Hello") -> dict:
    ...     return {"message": f"{greeting}, {name}!"}
    >>> 
    >>> # Generate MCP server
    >>> server_path = sdk.generate_mcp_server("./my_server")
    >>> print(f"Server generated at: {server_path}")

For more examples and documentation, visit: https://github.com/mcp-toolkit/mcp-dev-toolkit
"""

__version__ = "1.0.0"
__author__ = "MCP Development Community"
__email__ = "mcp-dev-toolkit@proton.me"
__license__ = "MIT"
__description__ = "A comprehensive development toolkit for building Model Context Protocol (MCP) tools and servers"

# Core imports for easy access
from .core import (
    MCPDevelopmentSDK,
    create_sdk,
    ToolType,
    MiddlewarePhase,
    ToolMetadata,
    InputParameter,
    ToolSchema,
)

from .middleware import (
    Middleware,
    LoggingMiddleware,
    ValidationMiddleware,
    PerformanceMiddleware,
)

from .schema import SchemaExtractor

# Optional imports (fail gracefully)
try:
    from .generators import (
        MCPServerGenerator,
        OpenAPIGenerator,
        ClientGenerator,
    )
except ImportError:
    # Generators require full dependencies
    pass

# Version info tuple
VERSION_INFO = tuple(map(int, __version__.split('.')))

# Export main symbols
__all__ = [
    # Core SDK
    "MCPDevelopmentSDK",
    "create_sdk",
    
    # Types and Enums
    "ToolType",
    "MiddlewarePhase", 
    "ToolMetadata",
    "InputParameter",
    "ToolSchema",
    
    # Middleware
    "Middleware",
    "LoggingMiddleware",
    "ValidationMiddleware", 
    "PerformanceMiddleware",
    
    # Schema utilities
    "SchemaExtractor",
    
    # Version info
    "__version__",
    "VERSION_INFO",
]

# Package metadata
PACKAGE_INFO = {
    "name": "mcp-dev-toolkit",
    "version": __version__,
    "description": __description__,
    "author": __author__,
    "author_email": __email__,
    "license": __license__,
    "python_requires": ">=3.8",
    "keywords": ["mcp", "model-context-protocol", "ai-tools", "development-toolkit", "sdk"],
}

def get_version():
    """Get the current version of the package."""
    return __version__

def get_package_info():
    """Get comprehensive package information."""
    return PACKAGE_INFO.copy()

# Runtime dependency checks
def check_dependencies():
    """Check if required dependencies are available."""
    missing_deps = []
    
    # Check core dependencies
    try:
        import mcp
    except ImportError:
        missing_deps.append("mcp")
    
    try:
        import pydantic
    except ImportError:
        missing_deps.append("pydantic")
    
    # Check optional dependencies
    optional_deps = []
    try:
        import aiohttp
    except ImportError:
        optional_deps.append("aiohttp")
    
    try:
        import jinja2
    except ImportError:
        optional_deps.append("jinja2")
    
    try:
        import yaml
    except ImportError:
        optional_deps.append("yaml")
    
    return {
        "missing_required": missing_deps,
        "missing_optional": optional_deps,
        "has_full_features": len(optional_deps) == 0
    }

# Perform dependency check on import
_DEPENDENCY_STATUS = check_dependencies()

if _DEPENDENCY_STATUS["missing_required"]:
    import warnings
    warnings.warn(
        f"Missing required dependencies: {', '.join(_DEPENDENCY_STATUS['missing_required'])}. "
        f"Install with: pip install mcp-dev-toolkit[full]",
        ImportWarning
    )
