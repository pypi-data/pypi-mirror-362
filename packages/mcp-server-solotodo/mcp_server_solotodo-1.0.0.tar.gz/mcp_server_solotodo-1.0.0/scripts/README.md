# Product Data Analysis Script

This script downloads product data, extracts and flattens nested product information, and creates lookup tables for ID-based relationships.

## What it does

1. **Downloads product data** from an API endpoint
2. **Extracts product entries** from the nested JSON structure
3. **Flattens the data** using `pd.json_normalize()` to create a DataFrame with dot-notation columns
4. **Identifies ID relationships** in the data (e.g., `processor_id` → `processor_name`, `processor_unicode`, etc.)
5. **Creates lookup tables** for each ID-based entity and saves them as CSV files

## Output

The script generates:
- `results.json` - Raw product data downloaded from the API
- A flattened DataFrame with all product information
- Individual lookup tables in the `lookup/` directory for entities like:
  - `processor.csv` - Processor information
  - `ram_type.csv` - RAM type details
  - `screen.csv` - Screen specifications
  - `brand.csv` - Brand information
  - And many more...

## Requirements

```bash
pip install pandas requests
```

## Usage

Run the Jupyter notebook:

```
get_mappings.ipynb
```

## Notes

- The script automatically creates the `lookup/` directory if it doesn't exist
- All CSV files are saved without index columns for clean importing
- The flattened DataFrame contains columns like `product.name`, `product.specs.processor_id`, `metadata.offer_price_usd`, etc.