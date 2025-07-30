"""
SoloTodo API client and search functionality.

This module provides functions for searching laptops on SoloTodo.cl using both
ID-based and unicode-based schemas, plus utility functions for converting between them.
"""

import functools
from mcp_server_solotodo import schemas, mappings
import httpx


async def _call_search_notebooks_api(parameters: schemas.NotebookSearchIdQueryParams) -> list[schemas.NotebookSearchResponse.ProductBucket.ProductEntry]:
    """
    Make a raw API call to SoloTodo with ID-based parameters.
    
    Args:
        parameters: Search parameters using numeric IDs expected by SoloTodo API
        
    Returns:
        List of product entries from the API response
    """
    # Convert parameters to dict, excluding None values
    # Note: Filtering None values is required by httpx (but not in requests)
    # See: https://www.python-httpx.org/compatibility/#requests-compatibility
    query_params = {k: v for k, v in parameters.model_dump().items() if v is not None}
    
    # Make the API request
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://publicapi.solotodo.com/categories/1/browse/",
            params=query_params
        )
        response.raise_for_status()
    
    # Parse JSON response and validate using our schema
    search_response = schemas.NotebookSearchResponse(**response.json())
    
    # Generate and return product entries
    return [entry for bucket in search_response.results for entry in bucket.product_entries]


async def search_laptops(parameters: schemas.NotebookSearchUnicodeQueryParams) -> list[schemas.NotebookSearchResponse.ProductBucket.ProductEntry]:
    """
    Search laptops using human-readable parameters.
    
    Args:
        parameters: Search parameters using human-readable strings
        
    Returns:
        List of product entries from the API response
    """
    # Convert unicode parameters to ID parameters
    id_parameters = unicode_to_id(parameters)
    
    # Use the raw API call with converted parameters
    return await _call_search_notebooks_api(id_parameters)


def unicode_to_id(
    unicode: schemas.NotebookSearchUnicodeQueryParams,
) -> schemas.NotebookSearchIdQueryParams:
    """
    Convert unicode strings in the NotebookSearchUnicodeQueryParams to IDs.
    
    Args:
        unicode: Search parameters with human-readable strings
        
    Returns:
        Search parameters with numeric IDs for the API
    """

    id_dump = {
        attribute: _convert_attribute(value, attribute) if attribute in mappings.TABLE else value
        for attribute, value in unicode.model_dump().items()
    }
    return schemas.NotebookSearchIdQueryParams(**id_dump)  # type: ignore[arg-type]


@functools.singledispatch
def _convert_attribute(
    value: None| str | list, attribute_name: str
) -> None | schemas.Id | list[schemas.Id]:
    raise ValueError(
        f"Unsupported value type: {type(value)} for attribute {attribute_name}"
    )


@_convert_attribute.register
def _(value: None, attribute_name: str) -> None:
    return None

@_convert_attribute.register
def _(value: str, attribute_name: str) -> schemas.Id:
    return mappings.TABLE[attribute_name][value]


@_convert_attribute.register
def _(value: list, attribute_name: str) -> list[schemas.Id]:
    return [mappings.TABLE[attribute_name][item] for item in value]