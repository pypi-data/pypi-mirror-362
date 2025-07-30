"""
Command Line Interface for MCP Development Toolkit
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, Any

def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for CLI"""
    parser = argparse.ArgumentParser(
        prog="mcp-toolkit",
        description="MCP Development Toolkit - Build and manage MCP tools and servers"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create new MCP project")
    create_parser.add_argument("name", help="Project name")
    create_parser.add_argument("--type", choices=["server", "tool", "integration"], default="server", help="Project type")
    create_parser.add_argument("--output", "-o", default=".", help="Output directory")
    
    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate code from existing tools")
    gen_parser.add_argument("input", help="Input Python file with tools")
    gen_parser.add_argument("--server", action="store_true", help="Generate MCP server")
    gen_parser.add_argument("--openapi", action="store_true", help="Generate OpenAPI spec")
    gen_parser.add_argument("--client", action="store_true", help="Generate client SDK")
    gen_parser.add_argument("--output", "-o", default=".", help="Output directory")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate MCP tools")
    validate_parser.add_argument("input", help="Input Python file with tools")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run MCP server")
    run_parser.add_argument("input", help="Input Python file or server script")
    run_parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    return parser


def create_project(name: str, project_type: str, output_dir: str):
    """Create a new MCP project"""
    from .generators import MCPServerGenerator
    
    output_path = Path(output_dir) / name
    output_path.mkdir(parents=True, exist_ok=True)
    
    if project_type == "server":
        # Create basic server structure
        server_content = f'''#!/usr/bin/env python3
"""
{name} - MCP Server
"""

from mcp_dev_toolkit import create_sdk, ToolType

# Create SDK instance
sdk = create_sdk("{name}", "1.0.0")

@sdk.tool(
    name="hello_world",
    description="A simple hello world tool",
    tool_type=ToolType.SIMPLE,
    tags=["example", "greeting"]
)
async def hello_world(name: str = "World") -> dict:
    """Say hello to someone"""
    return {{
        "message": f"Hello, {{name}}!",
        "timestamp": "2024-01-01T00:00:00Z"
    }}

if __name__ == "__main__":
    # Generate and run server
    app = sdk.create_mcp_app()
    asyncio.run(sdk.run_server(app))
'''
        
        server_file = output_path / f"{name}_server.py"
        server_file.write_text(server_content)
        
        # Create requirements.txt
        req_content = """mcp-dev-toolkit[full]
mcp>=1.0.0
"""
        req_file = output_path / "requirements.txt"
        req_file.write_text(req_content)
        
        # Create README
        readme_content = f"""# {name}

MCP Server created with mcp-dev-toolkit

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python {name}_server.py
```

## Development

Edit `{name}_server.py` to add your own tools.
"""
        readme_file = output_path / "README.md"
        readme_file.write_text(readme_content)
        
        print(f"✅ Created MCP server project at: {output_path}")
        print(f"📝 Edit {name}_server.py to add your tools")
        print(f"🚀 Run with: python {name}_server.py")


def generate_from_file(input_file: str, output_dir: str, server: bool, openapi: bool, client: bool):
    """Generate code from existing tools file"""
    import importlib.util
    import sys
    
    # Load the module
    spec = importlib.util.spec_from_file_location("user_tools", input_file)
    if spec is None or spec.loader is None:
        print(f"❌ Could not load {input_file}")
        sys.exit(1)
    
    module = importlib.util.module_from_spec(spec)
    sys.modules["user_tools"] = module
    spec.loader.exec_module(module)
    
    # Find SDK instance
    sdk = None
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if hasattr(attr, 'tools') and hasattr(attr, 'name'):
            sdk = attr
            break
    
    if sdk is None:
        print(f"❌ No SDK instance found in {input_file}")
        sys.exit(1)
    
    output_path = Path(output_dir)
    
    if server:
        server_path = sdk.generate_mcp_server(str(output_path))
        print(f"✅ Generated MCP server at: {server_path}")
    
    if openapi:
        spec = sdk.generate_openapi_spec()
        spec_file = output_path / f"{sdk.name}_openapi.json"
        spec_file.write_text(json.dumps(spec, indent=2))
        print(f"✅ Generated OpenAPI spec at: {spec_file}")
    
    if client:
        from .generators import ClientGenerator
        client_path = ClientGenerator.generate_python_client(sdk.name, sdk.tools, str(output_path))
        print(f"✅ Generated Python client at: {client_path}")


def validate_file(input_file: str):
    """Validate MCP tools in file"""
    import importlib.util
    import sys
    
    try:
        # Load the module
        spec = importlib.util.spec_from_file_location("user_tools", input_file)
        if spec is None or spec.loader is None:
            print(f"❌ Could not load {input_file}")
            return False
        
        module = importlib.util.module_from_spec(spec)
        sys.modules["user_tools"] = module
        spec.loader.exec_module(module)
        
        # Find SDK instance
        sdk = None
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if hasattr(attr, 'tools') and hasattr(attr, 'name'):
                sdk = attr
                break
        
        if sdk is None:
            print(f"❌ No SDK instance found in {input_file}")
            return False
        
        print(f"✅ Found SDK: {sdk.name} v{sdk.version}")
        print(f"📊 Tools found: {len(sdk.tools)}")
        
        from .schema import SchemaExtractor
        
        for tool_name, tool_schema in sdk.tools.items():
            print(f"  🔧 {tool_name}: {tool_schema.metadata.description}")
            
            # Validate function signature
            if tool_schema.handler_function:
                validation = SchemaExtractor.validate_function_signature(tool_schema.handler_function)
                if not validation["valid"]:
                    print(f"    ⚠️  Issues: {', '.join(validation['issues'])}")
                else:
                    print(f"    ✅ Signature valid")
        
        return True
        
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return False


async def run_server(input_file: str, debug: bool):
    """Run MCP server from file"""
    import importlib.util
    import sys
    import logging
    
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    
    try:
        # Load the module
        spec = importlib.util.spec_from_file_location("user_server", input_file)
        if spec is None or spec.loader is None:
            print(f"❌ Could not load {input_file}")
            return
        
        module = importlib.util.module_from_spec(spec)
        sys.modules["user_server"] = module
        spec.loader.exec_module(module)
        
        # Look for main function or SDK instance
        if hasattr(module, 'main'):
            await module.main()
        else:
            # Find SDK instance
            sdk = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if hasattr(attr, 'tools') and hasattr(attr, 'name'):
                    sdk = attr
                    break
            
            if sdk:
                app = sdk.create_mcp_app()
                await sdk.run_server(app)
            else:
                print(f"❌ No main() function or SDK instance found in {input_file}")
        
    except Exception as e:
        print(f"❌ Server failed: {e}")
        if debug:
            import traceback
            traceback.print_exc()


def main():
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == "create":
            create_project(args.name, args.type, args.output)
        
        elif args.command == "generate":
            generate_from_file(
                args.input,
                args.output,
                args.server,
                args.openapi,
                args.client
            )
        
        elif args.command == "validate":
            success = validate_file(args.input)
            sys.exit(0 if success else 1)
        
        elif args.command == "run":
            asyncio.run(run_server(args.input, args.debug))
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
