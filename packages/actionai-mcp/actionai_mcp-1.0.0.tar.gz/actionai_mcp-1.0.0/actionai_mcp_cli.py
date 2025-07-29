#!/usr/bin/env python3
"""
ActionAI MCP HTTP Client - Standalone Script for uvx

This is a standalone script that can be run with uvx without needing a package installation.

Usage:
  uvx actionai_mcp_cli.py [options]

Environment Variables:
  MCP_SERVER_URL - URL of the ActionAI MCP HTTP service (default: http://localhost:8089/mcp)
  MCP_TIMEOUT - Request timeout in seconds (default: 30)
  ACTIONAI_API_KEY - API key for ActionAI service authentication (default: client-access-key-2024)
"""

import json
import os
import sys
import asyncio
import argparse
from typing import Dict, Any, Optional
import logging

# Configuration
MCP_SERVER_URL = os.getenv('MCP_SERVER_URL', 'http://localhost:8089/mcp')
MCP_TIMEOUT = int(os.getenv('MCP_TIMEOUT', '30'))
ACTIONAI_API_KEY = os.getenv('ACTIONAI_API_KEY', 'client-access-key-2024')

# Setup logging to stderr
logging.basicConfig(
    level=logging.ERROR,
    format='[DEBUG] %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

try:
    import aiohttp
except ImportError:
    print("Error: aiohttp is required. Install with: pip install aiohttp", file=sys.stderr)
    sys.exit(1)


class ActionAIMCPClient:
    def __init__(self, server_url: str = MCP_SERVER_URL):
        self.server_url = server_url
        self.request_id = 1
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=MCP_TIMEOUT),
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'ActionAI-MCP-Client-Python/1.0.0',
                'X-MCP-Client-Key': ACTIONAI_API_KEY
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a JSON-RPC request to the ActionAI MCP HTTP service"""
        if params is None:
            params = {}
            
        request_data = {
            'jsonrpc': '2.0',
            'id': self.request_id,
            'method': method,
            'params': params
        }
        self.request_id += 1

        if not self.session:
            raise RuntimeError("Client session not initialized. Use 'async with' context manager.")

        try:
            async with self.session.post(self.server_url, json=request_data) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"HTTP {response.status}: {error_text}")
                
                response_data = await response.json()
                return response_data
                
        except asyncio.TimeoutError:
            raise Exception(f"Request timeout after {MCP_TIMEOUT}s")
        except aiohttp.ClientError as e:
            raise Exception(f"Request failed: {str(e)}")

    async def handle_stdio(self):
        """Handle MCP protocol communication via stdin/stdout"""
        
        async def process_line(line: str):
            if line.strip():
                request = None
                try:
                    request = json.loads(line.strip())
                    response = await self.send_request(request['method'], request.get('params', {}))
                    print(json.dumps(response), flush=True)

                except Exception as error:
                    error_response = {
                        'jsonrpc': '2.0',
                        'id': request.get('id') if request else None,
                        'error': {
                            'code': -32603,
                            'message': str(error)
                        }
                    }
                    print(json.dumps(error_response), flush=True)

        # Read from stdin line by line
        try:
            for line in sys.stdin:
                await process_line(line)
        except KeyboardInterrupt:
            pass
        except EOFError:
            pass

    async def test_connection(self) -> bool:
        """Test connection to the MCP server"""
        try:
            print(f"Testing connection to {self.server_url}...")
            
            response = await self.send_request('initialize', {})
            
            if 'error' in response and response['error']:
                print(f"❌ Connection test failed: {response['error']['message']}")
                return False
            
            print("✅ Connection successful!")
            server_info = response.get('result', {}).get('serverInfo', 'Unknown')
            print(f"Server info: {server_info}")
            return True
            
        except Exception as error:
            print(f"❌ Connection test failed: {str(error)}")
            return False


async def main():
    parser = argparse.ArgumentParser(
        description='ActionAI MCP HTTP Client',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables:
  MCP_SERVER_URL      URL of the ActionAI MCP HTTP service (default: http://localhost:8089/mcp)
  MCP_TIMEOUT         Request timeout in seconds (default: 30)
  ACTIONAI_API_KEY    API key for ActionAI service authentication (default: client-access-key-2024)

Examples:
  # Test connection:
  uvx --with aiohttp actionai_mcp_cli.py --test
  
  # Use with Claude Desktop:
  {
    "mcpServers": {
      "actionai-mcp": {
        "command": "uvx",
        "args": ["--with", "aiohttp", "actionai_mcp_cli.py"],
        "env": {
          "MCP_SERVER_URL": "http://localhost:8089/mcp"
        }
      }
    }
  }
        """
    )
    
    parser.add_argument('url', nargs='?', default=MCP_SERVER_URL,
                       help='URL of the ActionAI MCP HTTP service')
    parser.add_argument('--test', '-t', action='store_true',
                       help='Test connection to MCP server')
    parser.add_argument('--version', '-v', action='store_true',
                       help='Show version information')
    
    args = parser.parse_args()
    
    if args.version:
        print("ActionAI MCP Client v1.0.0")
        return
    
    async with ActionAIMCPClient(args.url) as client:
        if args.test:
            success = await client.test_connection()
            sys.exit(0 if success else 1)
        else:
            # Default: Handle MCP protocol via stdio
            await client.handle_stdio()


if __name__ == '__main__':
    asyncio.run(main())
