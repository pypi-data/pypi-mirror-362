"""
Code generators for MCP Development Toolkit
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import jinja2
    import yaml
except ImportError:
    raise ImportError("Code generation requires full dependencies. Run: pip install mcp-dev-toolkit[full]")


class MCPServerGenerator:
    """Generate complete MCP server applications"""

    SERVER_TEMPLATE = '''#!/usr/bin/env python3
"""
{{ server_name }} - Generated MCP Server
Generated on: {{ generation_date }}
"""

import asyncio
import json
import logging
from typing import Any, Dict, List

import mcp.types as types
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.server import NotificationOptions

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("{{ server_name }}")

# Create the server
app = Server("{{ server_name }}")

{% for tool_name, tool_schema in tools.items() %}
# Tool: {{ tool_name }}
async def {{ tool_name }}_handler(**kwargs) -> Any:
    """{{ tool_schema.metadata.description }}"""
    # TODO: Implement your tool logic here
    return {
        "message": "Tool {{ tool_name }} executed successfully",
        "inputs": kwargs,
        "timestamp": "{{ generation_date }}"
    }

{% endfor %}

@app.list_tools()
async def list_tools() -> List[types.Tool]:
    """List available tools"""
    return [
{% for tool_name, tool_schema in tools.items() %}
        types.Tool(
            name="{{ tool_name }}",
            description="{{ tool_schema.metadata.description }}",
            inputSchema={{ tool_schema.input_schema | tojson }}
        ),
{% endfor %}
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> List[types.TextContent]:
    """Handle tool calls"""
    try:
{% for tool_name, tool_schema in tools.items() %}
        if name == "{{ tool_name }}":
            result = await {{ tool_name }}_handler(**arguments)
            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
            )]
{% endfor %}
        
        return [types.TextContent(
            type="text",
            text=f"❌ Unknown tool: {name}"
        )]
        
    except Exception as e:
        logger.error(f"Tool execution failed: {e}")
        return [types.TextContent(
            type="text",
            text=f"❌ Error: {str(e)}"
        )]

async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="{{ server_name }}",
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
'''

    CONFIG_TEMPLATE = '''# {{ server_name }} Configuration

server:
  name: "{{ server_name }}"
  version: "1.0.0"
  description: "Generated MCP server with {{ tools | length }} tools"

tools:
{% for tool_name, tool_schema in tools.items() %}
  {{ tool_name }}:
    type: "{{ tool_schema.metadata.tool_type.value }}"
    description: "{{ tool_schema.metadata.description }}"
    tags: {{ tool_schema.metadata.tags | tojson }}
    examples: {{ tool_schema.metadata.examples | tojson }}
{% endfor %}

generated:
  timestamp: "{{ generation_date }}"
  generator: "mcp-dev-toolkit"
'''

    @classmethod
    def generate(cls, server_name: str, tools: Dict[str, Any], output_dir: str = ".") -> str:
        """Generate complete MCP server"""
        from .schema import SchemaExtractor
        
        # Create output directory
        output_path = Path(output_dir) / f"{server_name}_server"
        output_path.mkdir(parents=True, exist_ok=True)

        # Prepare template data
        tools_data = {}
        for tool_name, tool_schema in tools.items():
            input_schema = SchemaExtractor.generate_json_schema(tool_schema.input_parameters)
            tools_data[tool_name] = {
                "metadata": tool_schema.metadata,
                "input_schema": input_schema
            }

        template_data = {
            "server_name": server_name,
            "tools": tools_data,
            "generation_date": datetime.now().isoformat()
        }

        # Setup Jinja2
        template_env = jinja2.Environment(
            loader=jinja2.BaseLoader(),
            autoescape=False
        )

        # Generate server file
        server_template = template_env.from_string(cls.SERVER_TEMPLATE)
        server_code = server_template.render(**template_data)
        
        server_file = output_path / f"{server_name}_server.py"
        server_file.write_text(server_code, encoding='utf-8')

        # Generate configuration file
        config_template = template_env.from_string(cls.CONFIG_TEMPLATE)
        config_content = config_template.render(**template_data)
        
        config_file = output_path / "config.yml"
        config_file.write_text(config_content, encoding='utf-8')

        # Generate README
        readme_content = cls._generate_readme(server_name, tools_data)
        readme_file = output_path / "README.md"
        readme_file.write_text(readme_content, encoding='utf-8')

        # Generate requirements.txt
        requirements_content = cls._generate_requirements()
        requirements_file = output_path / "requirements.txt"
        requirements_file.write_text(requirements_content, encoding='utf-8')

        return str(output_path)

    @classmethod
    def _generate_readme(cls, server_name: str, tools: Dict[str, Any]) -> str:
        """Generate README file for the server"""
        content = f"""# {server_name} MCP Server

Generated MCP server with {len(tools)} tools.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python {server_name}_server.py
```

## Available Tools

"""
        
        for tool_name, tool_data in tools.items():
            content += f"### {tool_name}\n\n"
            content += f"{tool_data['metadata'].description}\n\n"
            content += f"**Type:** {tool_data['metadata'].tool_type.value}\n\n"
            if tool_data['metadata'].tags:
                content += f"**Tags:** {', '.join(tool_data['metadata'].tags)}\n\n"
            
            # Add input schema
            content += "**Input Schema:**\n\n```json\n"
            content += json.dumps(tool_data['input_schema'], indent=2)
            content += "\n```\n\n"

        content += f"\n## Generated\n\nGenerated on: {datetime.now().isoformat()}\nGenerator: mcp-dev-toolkit\n"
        return content

    @classmethod
    def _generate_requirements(cls) -> str:
        """Generate requirements.txt file"""
        return """mcp>=1.0.0
pydantic>=2.0.0
asyncio-mqtt>=0.11.0
"""


class OpenAPIGenerator:
    """Generate OpenAPI specifications"""

    @classmethod
    def generate(cls, tools: Dict[str, Any], server_name: str, version: str) -> Dict[str, Any]:
        """Generate OpenAPI specification from tools"""
        from .schema import SchemaExtractor
        
        spec = {
            "openapi": "3.0.3",
            "info": {
                "title": f"{server_name} API",
                "description": f"Generated API for {server_name} MCP server",
                "version": version,
                "contact": {
                    "name": "Generated by mcp-dev-toolkit"
                }
            },
            "servers": [
                {
                    "url": "http://localhost:8000",
                    "description": "Development server"
                }
            ],
            "paths": {},
            "components": {
                "schemas": {}
            }
        }

        # Generate paths for each tool
        for tool_name, tool_schema in tools.items():
            input_schema = SchemaExtractor.generate_json_schema(tool_schema.input_parameters)
            
            # Create path
            path = f"/tools/{tool_name}"
            spec["paths"][path] = {
                "post": {
                    "summary": tool_schema.metadata.description,
                    "description": tool_schema.metadata.description,
                    "tags": tool_schema.metadata.tags or ["tools"],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": input_schema
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Successful response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "result": {
                                                "type": "object",
                                                "description": "Tool execution result"
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Bad request"
                        },
                        "500": {
                            "description": "Internal server error"
                        }
                    }
                }
            }

            # Add schema to components
            schema_name = f"{tool_name.title()}Input"
            spec["components"]["schemas"][schema_name] = input_schema

        return spec


class ClientGenerator:
    """Generate client SDKs in various languages"""

    PYTHON_CLIENT_TEMPLATE = '''"""
Generated Python client for {{ server_name }}
"""

import asyncio
import json
from typing import Any, Dict, Optional
import aiohttp

class {{ server_name.title().replace('_', '').replace('-', '') }}Client:
    """Generated client for {{ server_name }} MCP server"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
{% for tool_name, tool_schema in tools.items() %}
    async def {{ tool_name }}(self{% for param in tool_schema.input_parameters %}, {{ param.name }}: {{ param.param_type.__name__ }}{% if not param.required %} = None{% endif %}{% endfor %}) -> Dict[str, Any]:
        """{{ tool_schema.metadata.description }}"""
        data = {
{% for param in tool_schema.input_parameters %}
            "{{ param.name }}": {{ param.name }},
{% endfor %}
        }
        
        async with self.session.post(
            f"{self.base_url}/tools/{{ tool_name }}",
            json=data
        ) as response:
            response.raise_for_status()
            return await response.json()

{% endfor %}

# Example usage
async def main():
    async with {{ server_name.title().replace('_', '').replace('-', '') }}Client() as client:
{% for tool_name, tool_schema in tools.items() %}
        # Example call to {{ tool_name }}
        # result = await client.{{ tool_name }}(...)
        # print(result)
{% endfor %}
        pass

if __name__ == "__main__":
    asyncio.run(main())
'''

    @classmethod
    def generate_python_client(cls, server_name: str, tools: Dict[str, Any], output_dir: str = ".") -> str:
        """Generate Python client"""
        output_path = Path(output_dir) / f"{server_name}_client.py"
        
        template_env = jinja2.Environment(
            loader=jinja2.BaseLoader(),
            autoescape=False
        )
        
        template = template_env.from_string(cls.PYTHON_CLIENT_TEMPLATE)
        client_code = template.render(
            server_name=server_name,
            tools=tools
        )
        
        output_path.write_text(client_code, encoding='utf-8')
        return str(output_path)
