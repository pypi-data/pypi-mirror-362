# Dolze Templates

A Python package containing templates for Dolze landing pages.

## Installation

```bash
pip install dolze-templates
```

## Usage

```python
from dolze_templates import get_template_registry, get_template_content

# Get the template registry
registry = get_template_registry()

# Get template content
template_html = get_template_content("templates/layouts/brand_product_physical.html")
```

## Template Structure

The package includes:

- Template registry configuration
- Layout templates
- Section templates with variants
- Sample JSON data

## Development

To build the package locally:

```bash
pip install -e .
```
