#!/usr/bin/env python3
"""
SoloTodo MCP Server
A Model Context Protocol server for searching laptops on SoloTodo.cl
"""

import sys

from mcp.server.fastmcp import FastMCP

from mcp_server_solotodo import schemas, utils, solotodo


mcp = FastMCP("solotodo")

@mcp.tool()
async def search_notebooks(
    search_params: schemas.NotebookSearchUnicodeQueryParams
) -> list[str]:
    """
    Search for notebooks on SoloTodo.cl with various filter options.
    
    This tool allows you to search and filter laptops based on specifications like:
    - Brand, processor, RAM, storage, screen size
    - Price range, operating system, video card
    - And many other technical specifications
    
    Args:
        search_params: NotebookSearchUnicodeQueryParams object containing all search filters
    
    Returns:
        A list of matching notebooks with their details and prices.
    """
    
    print(search_params, file=sys.stderr)
    
    products = await solotodo.search_laptops(search_params)
    cards = [utils.format_product_card(product) for product in products]
    return cards


def run():
    """Main entry point for the MCP server"""
    mcp.run(transport='stdio')