"""
Schema extraction utilities for MCP Development Toolkit
"""

import inspect
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type, get_type_hints, TYPE_CHECKING

if TYPE_CHECKING:
    from .core import InputParameter


class SchemaExtractor:
    """Extracts JSON schema from Python function signatures"""

    TYPE_MAPPING = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        List: "array",
        Dict: "object",
        Any: "any"
    }

    @classmethod
    def extract_input_parameters(cls, func: Callable) -> List['InputParameter']:
        """Extract input parameters from function signature"""
        from .core import InputParameter  # Import here to avoid circular imports
        
        sig = inspect.signature(func)
        type_hints = get_type_hints(func)
        parameters = []

        for param_name, param in sig.parameters.items():
            # Skip special parameters
            if param_name in ['self', 'cls', 'gateway', 'context']:
                continue

            # Get type from hints or annotation
            param_type = type_hints.get(param_name, param.annotation)
            if param_type == inspect.Parameter.empty:
                param_type = str  # Default to string

            # Check if required (no default value)
            required = param.default == inspect.Parameter.empty
            default = param.default if not required else None

            # Extract enum values if it's a Literal or Enum
            enum_values = cls._extract_enum_values(param_type)

            parameters.append(InputParameter(
                name=param_name,
                param_type=param_type,
                required=required,
                default=default,
                enum_values=enum_values
            ))

        return parameters

    @classmethod
    def _extract_enum_values(cls, param_type: Type) -> Optional[List[Any]]:
        """Extract enum values from type annotation"""
        # Handle typing.Literal
        if hasattr(param_type, '__origin__') and hasattr(param_type, '__args__'):
            if str(param_type.__origin__) == 'typing.Literal':
                return list(param_type.__args__)

        # Handle Enum classes
        if inspect.isclass(param_type) and issubclass(param_type, Enum):
            return [e.value for e in param_type]

        return None

    @classmethod
    def generate_json_schema(cls, parameters: List['InputParameter']) -> Dict[str, Any]:
        """Generate JSON schema from parameters"""
        properties = {}
        required = []

        for param in parameters:
            json_type = cls.TYPE_MAPPING.get(param.param_type, "string")

            prop_schema = {
                "type": json_type,
                "description": param.description or f"Parameter {param.name}"
            }

            if param.enum_values:
                prop_schema["enum"] = param.enum_values

            if param.default is not None:
                prop_schema["default"] = param.default

            properties[param.name] = prop_schema

            if param.required:
                required.append(param.name)

        return {
            "type": "object",
            "properties": properties,
            "required": required
        }

    @classmethod
    def extract_return_type(cls, func: Callable) -> Optional[Type]:
        """Extract return type annotation from function"""
        type_hints = get_type_hints(func)
        return type_hints.get('return', None)

    @classmethod
    def generate_output_schema(cls, return_type: Optional[Type]) -> Optional[Dict[str, Any]]:
        """Generate output schema from return type annotation"""
        if return_type is None:
            return None

        json_type = cls.TYPE_MAPPING.get(return_type, "object")
        
        schema = {
            "type": json_type
        }

        # Add more specific schema for complex types
        if return_type == dict or return_type == Dict:
            schema["additionalProperties"] = True
        elif return_type == list or return_type == List:
            schema["items"] = {"type": "any"}

        return schema

    @classmethod
    def validate_function_signature(cls, func: Callable) -> Dict[str, Any]:
        """Validate that function signature is compatible with MCP tools"""
        sig = inspect.signature(func)
        issues = []
        
        # Check for unsupported parameter types
        for param_name, param in sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                issues.append(f"*args parameters not supported: {param_name}")
            elif param.kind == inspect.Parameter.VAR_KEYWORD:
                issues.append(f"**kwargs parameters not supported: {param_name}")
        
        # Check for missing type hints
        type_hints = get_type_hints(func)
        for param_name, param in sig.parameters.items():
            if param_name not in ['self', 'cls', 'gateway', 'context']:
                if param_name not in type_hints and param.annotation == inspect.Parameter.empty:
                    issues.append(f"Missing type hint for parameter: {param_name}")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "parameters_count": len(sig.parameters),
            "has_return_type": 'return' in type_hints
        }
