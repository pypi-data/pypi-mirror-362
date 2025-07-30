from mcp_server_solotodo import schemas
import textwrap



def format_product_card(product_entry: schemas.NotebookSearchResponse.ProductBucket.ProductEntry) -> str:
    """
    Create a plain text card representation of a notebook product.
    
    Args:
        product_entry: ProductEntry instance from the API response
        
    Returns:
        Formatted plain text card string
    """
    product = product_entry.product
    specs = product.specs
    price_usd = product_entry.metadata.offer_price_usd
    
    # Format price (convert to display format)
    formatted_price = f"${price_usd}"
    
    # Build the card with nice indentation in code
    card = textwrap.dedent(f"""
        {product.name}
        🔗 https://www.solotodo.cl/products/{product.id}

        {formatted_price}

        Procesador  {specs.processor_unicode} ({specs.processor_frequency_unicode} - {specs.processor_frequency_value} MHz)
        Núcleos     {specs.processor_thread_count_name} / {specs.processor_thread_count_value} hilos
        RAM         {specs.ram_quantity_unicode} {specs.ram_type_unicode} ({specs.ram_frequency_unicode})
        Pantalla    {specs.screen_size_unicode} ({specs.screen_resolution_unicode}) / {specs.screen_refresh_rate_unicode}
        Almacenamiento  {specs.largest_storage_drive.drive_type_unicode} {specs.largest_storage_drive.capacity_unicode}
        Tarjetas de video  {specs.main_gpu.unicode}
    """).strip()
    
    return card
