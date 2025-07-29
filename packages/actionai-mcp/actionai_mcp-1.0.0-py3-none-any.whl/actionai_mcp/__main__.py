#!/usr/bin/env python3
"""
Entry point for actionai-mcp when run as a module
"""

import asyncio
from .client import main as async_main

def main():
    """Synchronous entry point that runs the async main function"""
    asyncio.run(async_main())

if __name__ == '__main__':
    main()
