"""
Middleware system for MCP Development Toolkit
"""

import logging
import traceback
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Optional, Type, Dict, List
from enum import Enum

from .schema import SchemaExtractor


class Middleware(ABC):
    """Base class for middleware"""

    def __init__(self, priority: int = 50):
        self.priority = priority

    @abstractmethod
    async def process_pre(self, tool_schema: 'ToolSchema', args: tuple, kwargs: dict) -> Optional[tuple]:
        """Process before tool execution"""
        pass

    @abstractmethod
    async def process_post(self, tool_schema: 'ToolSchema', result: Any) -> Optional[Any]:
        """Process after tool execution"""
        pass

    @abstractmethod
    async def process_error(self, tool_schema: 'ToolSchema', error: Exception, args: tuple, kwargs: dict) -> Optional[Any]:
        """Process errors"""
        pass


class LoggingMiddleware(Middleware):
    """Built-in logging middleware"""

    def __init__(self, priority: int = 10):
        super().__init__(priority)
        self.logger = logging.getLogger("mcp_sdk")

    async def process_pre(self, tool_schema: 'ToolSchema', args: tuple, kwargs: dict) -> Optional[tuple]:
        self.logger.info(f"Executing tool: {tool_schema.metadata.name}")
        self.logger.debug(f"Args: {args}, Kwargs: {kwargs}")
        return None

    async def process_post(self, tool_schema: 'ToolSchema', result: Any) -> Optional[Any]:
        self.logger.info(f"Tool {tool_schema.metadata.name} completed successfully")
        return None

    async def process_error(self, tool_schema: 'ToolSchema', error: Exception, args: tuple, kwargs: dict) -> Optional[Any]:
        self.logger.error(f"Tool {tool_schema.metadata.name} failed: {error}")
        self.logger.debug(traceback.format_exc())
        return None


class ValidationMiddleware(Middleware):
    """Input validation middleware"""

    def __init__(self, priority: int = 5):
        super().__init__(priority)

    async def process_pre(self, tool_schema: 'ToolSchema', args: tuple, kwargs: dict) -> Optional[tuple]:
        # Validate inputs against schema
        self._validate_inputs(tool_schema, kwargs)
        return None

    async def process_post(self, tool_schema: 'ToolSchema', result: Any) -> Optional[Any]:
        return None

    async def process_error(self, tool_schema: 'ToolSchema', error: Exception, args: tuple, kwargs: dict) -> Optional[Any]:
        return None

    def _validate_inputs(self, tool_schema: 'ToolSchema', kwargs: dict):
        """Validate input parameters"""
        for param in tool_schema.input_parameters:
            if param.required and param.name not in kwargs:
                raise ValueError(f"Missing required parameter: {param.name}")

            if param.name in kwargs:
                value = kwargs[param.name]
                # Type checking
                if param.param_type and not isinstance(value, param.param_type):
                    # Handle basic type conversions
                    try:
                        if param.param_type == int:
                            kwargs[param.name] = int(value)
                        elif param.param_type == float:
                            kwargs[param.name] = float(value)
                        elif param.param_type == str:
                            kwargs[param.name] = str(value)
                        elif param.param_type == bool:
                            kwargs[param.name] = bool(value)
                    except (ValueError, TypeError):
                        raise ValueError(f"Parameter {param.name} must be of type {param.param_type.__name__}")

                # Enum validation
                if param.enum_values and value not in param.enum_values:
                    raise ValueError(f"Parameter {param.name} must be one of: {param.enum_values}")


class PerformanceMiddleware(Middleware):
    """Performance monitoring middleware"""

    def __init__(self, priority: int = 15):
        super().__init__(priority)
        self.start_time = None

    async def process_pre(self, tool_schema: 'ToolSchema', args: tuple, kwargs: dict) -> Optional[tuple]:
        self.start_time = datetime.now()
        return None

    async def process_post(self, tool_schema: 'ToolSchema', result: Any) -> Optional[Any]:
        if self.start_time:
            duration = (datetime.now() - self.start_time).total_seconds()
            logging.getLogger("mcp_sdk.performance").info(
                f"Tool {tool_schema.metadata.name} executed in {duration:.3f}s"
            )
        return None

    async def process_error(self, tool_schema: 'ToolSchema', error: Exception, args: tuple, kwargs: dict) -> Optional[Any]:
        return None


class CachingMiddleware(Middleware):
    """Simple in-memory caching middleware"""

    def __init__(self, priority: int = 20, cache_size: int = 100):
        super().__init__(priority)
        self.cache = {}
        self.cache_size = cache_size

    async def process_pre(self, tool_schema: 'ToolSchema', args: tuple, kwargs: dict) -> Optional[tuple]:
        # Create cache key from function name and arguments
        cache_key = self._create_cache_key(tool_schema.metadata.name, args, kwargs)
        
        if cache_key in self.cache:
            logging.getLogger("mcp_sdk.cache").info(f"Cache hit for {tool_schema.metadata.name}")
            # Return cached result by raising a special exception that will be caught
            return cache_key
        
        return None

    async def process_post(self, tool_schema: 'ToolSchema', result: Any) -> Optional[Any]:
        # Store result in cache if not already cached
        return None

    async def process_error(self, tool_schema: 'ToolSchema', error: Exception, args: tuple, kwargs: dict) -> Optional[Any]:
        return None

    def _create_cache_key(self, tool_name: str, args: tuple, kwargs: dict) -> str:
        """Create a cache key from tool name and arguments"""
        import hashlib
        import json
        
        # Create a deterministic string representation
        key_data = {
            "tool": tool_name,
            "args": args,
            "kwargs": sorted(kwargs.items())
        }
        
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_str.encode()).hexdigest()


class RateLimitingMiddleware(Middleware):
    """Rate limiting middleware"""

    def __init__(self, priority: int = 3, max_calls: int = 100, window_seconds: int = 60):
        super().__init__(priority)
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self.call_history = {}

    async def process_pre(self, tool_schema: 'ToolSchema', args: tuple, kwargs: dict) -> Optional[tuple]:
        tool_name = tool_schema.metadata.name
        current_time = datetime.now()
        
        # Initialize or clean up call history for this tool
        if tool_name not in self.call_history:
            self.call_history[tool_name] = []
        
        # Remove calls outside the current window
        cutoff_time = current_time.timestamp() - self.window_seconds
        self.call_history[tool_name] = [
            call_time for call_time in self.call_history[tool_name]
            if call_time > cutoff_time
        ]
        
        # Check rate limit
        if len(self.call_history[tool_name]) >= self.max_calls:
            raise ValueError(f"Rate limit exceeded for tool {tool_name}. Max {self.max_calls} calls per {self.window_seconds} seconds.")
        
        # Record this call
        self.call_history[tool_name].append(current_time.timestamp())
        
        return None

    async def process_post(self, tool_schema: 'ToolSchema', result: Any) -> Optional[Any]:
        return None

    async def process_error(self, tool_schema: 'ToolSchema', error: Exception, args: tuple, kwargs: dict) -> Optional[Any]:
        return None


class SecurityMiddleware(Middleware):
    """Basic security middleware for input sanitization"""

    def __init__(self, priority: int = 1):
        super().__init__(priority)
        self.blocked_patterns = [
            r'<script.*?>.*?</script>',  # Script tags
            r'javascript:',  # JavaScript URLs
            r'on\w+\s*=',  # Event handlers
            r'eval\s*\(',  # eval calls
            r'exec\s*\(',  # exec calls
        ]

    async def process_pre(self, tool_schema: 'ToolSchema', args: tuple, kwargs: dict) -> Optional[tuple]:
        import re
        
        # Check all string parameters for suspicious patterns
        for key, value in kwargs.items():
            if isinstance(value, str):
                for pattern in self.blocked_patterns:
                    if re.search(pattern, value, re.IGNORECASE):
                        raise ValueError(f"Potentially unsafe input detected in parameter '{key}'")
        
        return None

    async def process_post(self, tool_schema: 'ToolSchema', result: Any) -> Optional[Any]:
        return None

    async def process_error(self, tool_schema: 'ToolSchema', error: Exception, args: tuple, kwargs: dict) -> Optional[Any]:
        return None
