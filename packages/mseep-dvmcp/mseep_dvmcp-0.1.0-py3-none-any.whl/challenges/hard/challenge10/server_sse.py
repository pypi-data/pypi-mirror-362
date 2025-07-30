from mcp.server.fastmcp import FastMCP, Context
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from fastapi import FastAPI

# Create a vulnerable MCP server for Challenge 10: Multi-Vector Attack with SSE support
class Challenge10Server:
    def __init__(self):
        self.name = "Challenge 10 - Multi-Vector Attack"
        self.port = 9010  # Changed from 8010 to avoid conflicts
        self.mcp = FastMCP(self.name)
        self.app = FastAPI()
        
        # Add a configuration management tool
        @self.mcp.tool()
        def get_config(config_name: str) -> str:
            """Get a configuration value from the system
            
            Args:
                config_name: The name of the configuration to retrieve
            """
            import os
            import json
            
            # Vulnerable: doesn't properly validate config_name
            # Allows path traversal and access to sensitive files
            
            config_dir = "/tmp/dvmcp_challenge10/config"
            
            # Attempt to read the requested configuration
            try:
                if config_name.endswith('.json'):
                    # Read JSON config
                    with open(os.path.join(config_dir, config_name), 'r') as f:
                        config_data = json.load(f)
                    return f"Configuration '{config_name}':\n{json.dumps(config_data, indent=2)}"
                else:
                    # Read text config
                    with open(os.path.join(config_dir, config_name), 'r') as f:
                        config_data = f.read()
                    return f"Configuration '{config_name}':\n{config_data}"
            except Exception as e:
                return f"Error retrieving configuration '{config_name}': {str(e)}"
        
        # Add a tool that processes user input
        @self.mcp.tool()
        def process_user_input(input_text: str) -> str:
            """Process user input and return a formatted response
            
            Args:
                input_text: The user input to process
            """
            # Vulnerable: multiple vectors - template injection, command injection, etc.
            
            # Format the response using a template
            template = f"""
            PROCESSED USER INPUT:
            
            {input_text}
            
            ANALYSIS:
            
            Length: {len(input_text)} characters
            Word count: {len(input_text.split())} words
            
            SYSTEM INFO:
            
            This request was processed by the Multi-Vector Challenge Server.
            """
            
            return template
        
        # Add a resource that provides system information
        @self.mcp.resource("system://info")
        def get_system_info() -> str:
            """Get information about the system"""
            import platform
            
            # Vulnerable: leaks sensitive system information
            system_info = f"""
            SYSTEM INFORMATION:
            
            Operating System: {platform.system()} {platform.release()}
            Python Version: {platform.python_version()}
            Machine: {platform.machine()}
            Node: {platform.node()}
            
            This server is running in a Docker container with multiple vulnerabilities.
            """
            
            return system_info
        
        # Mount the SSE server
        self.mount_sse_server()
    
    def mount_sse_server(self):
        """Mount the SSE server to the FastAPI app"""
        self.app.mount("/", self.create_sse_server())
        
    def create_sse_server(self):
        """Create a Starlette app that handles SSE connections and message handling"""
        transport = SseServerTransport("/messages/")
        
        # Define handler functions
        async def handle_sse(request):
            async with transport.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await self.mcp._mcp_server.run(
                    streams[0], streams[1], self.mcp._mcp_server.create_initialization_options()
                )
        
        # Create Starlette routes for SSE and message handling
        routes = [
            Route("/sse", endpoint=handle_sse),
            Mount("/messages", app=transport.handle_post_message),
        ]
        
        # Create a Starlette app
        return Starlette(routes=routes)
    
    def run(self):
        """Run the server with uvicorn"""
        import uvicorn
        print(f"Starting {self.name} MCP Server")
        print("Connect to this server using an MCP client (e.g., Claude Desktop or Cursor)")
        print(f"Server running at http://localhost:{self.port}")
        print(f"SSE endpoint available at http://localhost:{self.port}/sse")
        uvicorn.run(self.app, host="0.0.0.0", port=self.port)

# Run the server
if __name__ == "__main__":
    server = Challenge10Server()
    server.run()
