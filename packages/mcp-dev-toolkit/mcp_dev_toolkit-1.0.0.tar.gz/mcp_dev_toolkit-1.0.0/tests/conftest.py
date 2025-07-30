"""
Test configuration and fixtures for MCP Development Toolkit
"""

import pytest
import asyncio
from pathlib import Path
from typing import Dict, Any

from mcp_dev_toolkit import create_sdk, ToolType


@pytest.fixture
def sample_sdk():
    """Create a sample SDK for testing"""
    return create_sdk("test-sdk", "1.0.0")


@pytest.fixture
def sample_tool_function():
    """Sample tool function for testing"""
    async def test_tool(name: str, count: int = 1) -> Dict[str, Any]:
        """A sample tool for testing"""
        return {
            "message": f"Hello {name}",
            "count": count,
            "success": True
        }
    return test_tool


@pytest.fixture
def registered_sdk(sample_sdk):
    """SDK with a registered tool"""
    
    @sample_sdk.tool(
        name="test_tool",
        description="A test tool",
        tool_type=ToolType.SIMPLE,
        tags=["test"]
    )
    async def test_tool(name: str, count: int = 1) -> Dict[str, Any]:
        return {"message": f"Hello {name}", "count": count}
    
    return sample_sdk


@pytest.fixture
def temp_dir(tmp_path):
    """Temporary directory for test files"""
    return tmp_path


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


class MockGateway:
    """Mock gateway for testing integrations"""
    
    def __init__(self):
        self.requests = []
    
    async def get(self, url: str, **kwargs):
        self.requests.append({"method": "GET", "url": url, "kwargs": kwargs})
        return MockResponse({"data": "mock_data"})
    
    async def post(self, url: str, data=None, **kwargs):
        self.requests.append({"method": "POST", "url": url, "data": data, "kwargs": kwargs})
        return MockResponse({"success": True})


class MockResponse:
    """Mock HTTP response"""
    
    def __init__(self, data: Dict[str, Any], status_code: int = 200):
        self._data = data
        self.status_code = status_code
    
    def json(self):
        return self._data
    
    async def json_async(self):
        return self._data


@pytest.fixture
def mock_gateway():
    """Mock gateway for testing"""
    return MockGateway()


# Test data fixtures
@pytest.fixture
def sample_tool_metadata():
    """Sample tool metadata"""
    return {
        "name": "test_tool",
        "description": "A test tool",
        "tool_type": ToolType.SIMPLE,
        "tags": ["test", "sample"],
        "examples": [{
            "input": {"name": "world"},
            "output": {"message": "Hello world"}
        }]
    }


@pytest.fixture
def sample_openapi_spec():
    """Sample OpenAPI specification"""
    return {
        "openapi": "3.0.3",
        "info": {
            "title": "Test API",
            "version": "1.0.0"
        },
        "paths": {
            "/tools/test_tool": {
                "post": {
                    "summary": "Test tool",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
