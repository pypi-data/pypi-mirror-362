"""
Dolze Templates Package

This package provides templates for Dolze landing pages.
"""

import json
import os
import pkgutil
from typing import Dict, Any, Optional, List

# Import new classes
from .template_manager import TemplateManager
from .template_registry import TemplateRegistry

# Create singleton instances for backward compatibility
_template_manager = TemplateManager()
_template_registry = TemplateRegistry()

# Cache for template registry and content (for backward compatibility)
_registry_cache = None
_template_content_cache = {}

def get_template_registry() -> Dict[str, Any]:
    """
    Get the template registry configuration.

    Returns:
        Dict[str, Any]: The template registry configuration.
    """
    global _registry_cache

    if _registry_cache is not None:
        return _registry_cache

    try:
        # Use the new TemplateRegistry class
        _registry_cache = _template_registry.get_all_templates()
        return _registry_cache
    except Exception as e:
        raise ValueError(f"Failed to load template registry: {e}")

def get_template_content(template_path: str) -> str:
    """
    Get the content of a template file.

    Args:
        template_path (str): The path to the template file.

    Returns:
        str: The content of the template file.
    """
    global _template_content_cache

    if template_path in _template_content_cache:
        return _template_content_cache[template_path]

    try:
        # Use the new TemplateManager class
        content = _template_manager.get_template_content(template_path)
        _template_content_cache[template_path] = content
        return content
    except Exception as e:
        raise ValueError(f"Failed to load template: {template_path}, error: {e}")

def check_section_variant_exists(section_name: str, variant: str) -> bool:
    """
    Check if a section variant exists in the package.

    Args:
        section_name (str): The name of the section.
        variant (str): The variant ID (e.g., "v1", "v2").

    Returns:
        bool: True if the variant exists, False otherwise.
    """
    # Use the new TemplateManager class
    return _template_manager.check_section_variant_exists(section_name, variant)

def get_section_variants_from_registry(template_id: str, page: str = "index") -> Optional[Dict[str, str]]:
    """
    Fetch the section_variants mapping for a given template_id and page from the template registry.

    Args:
        template_id (str): The ID of the template.
        page (str, optional): The page slug (e.g., "index", "shop"). Defaults to "index".

    Returns:
        Optional[Dict[str, str]]: A dictionary mapping section names to variant IDs, or None if not found.
    """
    try:
        # Use the new TemplateManager class
        return _template_manager.get_section_variants(template_id, page)
    except Exception as e:
        print(f"Error reading section_variants from registry: {e}")
        return None

def get_sample_json() -> Dict[str, Any]:
    """
    Get the sample JSON data.

    Returns:
        Dict[str, Any]: The sample JSON data.
    """
    try:
        # Use the new TemplateManager class
        return _template_manager.get_sample_json()
    except Exception as e:
        raise ValueError(f"Failed to load sample JSON: {e}")

# New API functions for enhanced functionality

def initialize_website(business_config: Dict[str, Any]) -> str:
    """
    Initialize a website based on business configuration.
    
    Args:
        business_config (Dict[str, Any]): The business configuration.
        
    Returns:
        str: The template ID for the new website.
    """
    return _template_manager.derive_template_id(business_config)

def get_available_pages(template_id: str) -> List[str]:
    """
    Get available pages for a template.
    
    Args:
        template_id (str): The ID of the template.
        
    Returns:
        List[str]: List of available page slugs.
    """
    return _template_manager.get_available_pages_for_template(template_id)

# Page Management API

def add_page_to_template(template_id: str, page_type: str, page_title: str = None, content: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Add a page to a template.
    
    Args:
        template_id (str): The ID of the template.
        page_type (str): The type of page to add (e.g., "shop", "privacy").
        page_title (str, optional): Custom title for the page. Defaults to None.
        content (Dict[str, Any], optional): Custom content for the page. Defaults to None.
        
    Returns:
        Dict[str, Any]: The configuration for the new page.
    """
    return _template_manager.add_page_to_template(template_id, page_type, page_title, content)

def get_available_page_types() -> List[str]:
    """
    Get a list of available standard page types that can be added to templates.
    
    Returns:
        List[str]: List of available page type slugs.
    """
    return _template_manager.page_manager.get_available_page_types()

# Navigation Management API

def get_navigation_items(template_id: str) -> List[Dict[str, Any]]:
    """
    Get the navigation items for a template.
    
    Args:
        template_id (str): The ID of the template.
        
    Returns:
        List[Dict[str, Any]]: List of navigation items.
    """
    return _template_manager.get_navigation_items(template_id)

def generate_navigation(template_id: str, pages: List[str] = None) -> Dict[str, Any]:
    """
    Generate a navigation configuration for a template.
    
    Args:
        template_id (str): The ID of the template.
        pages (List[str], optional): List of page slugs to include in the navigation.
                                    If None, all available pages will be included.
        
    Returns:
        Dict[str, Any]: The generated navigation configuration.
    """
    return _template_manager.generate_navigation(template_id, pages)

# UI Component Management API

def create_button(label: str, url: str, variant: str = "primary", 
                 additional_classes: str = "", attributes: Dict[str, str] = None) -> Dict[str, Any]:
    """
    Create a button configuration.
    
    Args:
        label (str): The button label text.
        url (str): The URL the button links to.
        variant (str, optional): The button variant. Defaults to "primary".
        additional_classes (str, optional): Additional CSS classes. Defaults to "".
        attributes (Dict[str, str], optional): Additional HTML attributes. Defaults to None.
        
    Returns:
        Dict[str, Any]: The button configuration.
    """
    return _template_manager.create_button(label, url, variant, additional_classes, attributes)

def create_cta(label: str, url: str, variant: str = "primary", 
              additional_classes: str = "", attributes: Dict[str, str] = None) -> Dict[str, Any]:
    """
    Create a CTA (Call to Action) configuration.
    
    Args:
        label (str): The CTA label text.
        url (str): The URL the CTA links to.
        variant (str, optional): The CTA variant. Defaults to "primary".
        additional_classes (str, optional): Additional CSS classes. Defaults to "".
        attributes (Dict[str, str], optional): Additional HTML attributes. Defaults to None.
        
    Returns:
        Dict[str, Any]: The CTA configuration.
    """
    return _template_manager.create_cta(label, url, variant, additional_classes, attributes)

__all__ = [
    # Legacy API
    'get_template_registry',
    'get_template_content',
    'check_section_variant_exists',
    'get_section_variants_from_registry',
    'get_sample_json',
    
    # Core API
    'TemplateManager',
    'TemplateRegistry',
    'initialize_website',
    'get_available_pages',
    
    # Page Management API
    'add_page_to_template',
    'get_available_page_types',
    
    # Navigation Management API
    'get_navigation_items',
    'generate_navigation',
    
    # UI Component Management API
    'create_button',
    'create_cta',
]
