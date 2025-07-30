"""
Page Manager Module

This module provides functionality for managing pages within templates,
including creating new pages and managing page configurations.
"""

import json
import os
import pkgutil
from typing import Dict, Any, Optional, List

from .template_registry import TemplateRegistry

class PageManager:
    """
    Class for managing pages within templates.
    
    This class provides methods for creating new pages, retrieving page configurations,
    and managing page-related operations including navigation and section variants.
    """
    
    def __init__(self):
        """Initialize the PageManager with a TemplateRegistry instance."""
        self.registry = TemplateRegistry()
        
        # Define standard page types with their default configurations
        self._standard_page_types = {
            "index": {
                "title": "Home",
                "sections": ["navigation", "hero", "about", "features", "footer"],
                "template_path": "templates/layouts/standard_home.html"
            },
            "shop": {
                "title": "Shop",
                "sections": ["navigation", "product_grid", "footer"],
                "template_path": "templates/layouts/shops/standard_shop.html"
            },
            "privacy": {
                "title": "Privacy Policy",
                "sections": ["navigation", "content", "footer"],
                "template_path": "templates/layouts/standard_content.html"
            },
            "about": {
                "title": "About Us",
                "sections": ["navigation", "content", "team", "footer"],
                "template_path": "templates/layouts/standard_content.html"
            },
            "contact": {
                "title": "Contact Us",
                "sections": ["navigation", "contact_form", "footer"],
                "template_path": "templates/layouts/standard_content.html"
            }
        }
    
    def get_available_page_types(self) -> List[str]:
        """
        Get a list of available standard page types.
        
        Returns:
            List[str]: List of available page type slugs.
        """
        return list(self._standard_page_types.keys())
    
    def get_page_config(self, template_id: str, page_type: str) -> Optional[Dict[str, Any]]:
        """
        Get the configuration for a page in a template.
        
        Args:
            template_id (str): The ID of the template.
            page_type (str): The type of page.
            
        Returns:
            Optional[Dict[str, Any]]: The page configuration, or None if not found.
        """
        template_config = self.registry.get_template_config(template_id)
        if not template_config:
            return None
            
        pages = template_config.get("pages", {})
        return pages.get(page_type)
    
    def get_required_sections_for_page(self, page_type: str) -> List[str]:
        """
        Get the required sections for a standard page type.
        
        Args:
            page_type (str): The type of page.
            
        Returns:
            List[str]: List of required section names.
            
        Raises:
            ValueError: If the page type is not recognized.
        """
        if page_type not in self._standard_page_types:
            raise ValueError(f"Unknown page type: {page_type}")
            
        return self._standard_page_types[page_type]["sections"]
    
    def get_default_variants_for_page(self, template_id: str, page_type: str) -> Dict[str, str]:
        """
        Get the default section variants for a page type in a template.
        
        Args:
            template_id (str): The ID of the template.
            page_type (str): The type of page.
            
        Returns:
            Dict[str, str]: Dictionary mapping section names to variant IDs.
        """
        # Get required sections for this page type
        required_sections = self.get_required_sections_for_page(page_type)
        
        # Start with empty variants
        variants = {}
        
        # Try to get variants from an existing page in the template
        template_config = self.registry.get_template_config(template_id)
        if template_config and "section_variants" in template_config:
            # First check if this page type already has variants defined
            if page_type in template_config["section_variants"]:
                return template_config["section_variants"][page_type]
                
            # Otherwise, try to get variants from the index page
            if "index" in template_config["section_variants"]:
                index_variants = template_config["section_variants"]["index"]
                for section in required_sections:
                    if section in index_variants:
                        variants[section] = index_variants[section]
        
        # Fill in any missing variants with "v1"
        for section in required_sections:
            if section not in variants:
                variants[section] = "v1"
                
        return variants
    
    def create_page(self, template_id: str, page_type: str, content: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Create a new page configuration for a template.
        
        This is a placeholder for future implementation. Currently, it just
        returns a standard page configuration based on the page type.
        
        Args:
            template_id (str): The ID of the template.
            page_type (str): The type of page to create.
            content (Dict[str, Any], optional): Custom content for the page. Defaults to None.
            
        Returns:
            Dict[str, Any]: Configuration for the new page.
            
        Raises:
            ValueError: If the page type is not recognized or the template doesn't exist.
        """
        # Check if the template exists
        if not self.registry.template_exists(template_id):
            raise ValueError(f"Template '{template_id}' not found")
            
        # Check if the page type is valid
        if page_type not in self._standard_page_types:
            raise ValueError(f"Unknown page type: {page_type}")
            
        # Get the standard page configuration
        page_config = self._standard_page_types[page_type].copy()
        
        # Merge with custom content if provided
        if content:
            for key, value in content.items():
                page_config[key] = value
                
        return page_config
    
    def add_page_to_navigation(self, template_id: str, page_type: str, page_title: str = None) -> Dict[str, Any]:
        """
        Add a page to the navigation configuration of a template.
        
        This is a placeholder for future implementation. Currently, it just
        returns a standard navigation item for the page.
        
        Args:
            template_id (str): The ID of the template.
            page_type (str): The type of page.
            page_title (str, optional): Custom title for the page. Defaults to None.
            
        Returns:
            Dict[str, Any]: The navigation item for the page.
            
        Raises:
            ValueError: If the page type is not recognized or the template doesn't exist.
        """
        # Check if the template exists
        if not self.registry.template_exists(template_id):
            raise ValueError(f"Template '{template_id}' not found")
            
        # Check if the page type is valid
        if page_type not in self._standard_page_types:
            raise ValueError(f"Unknown page type: {page_type}")
            
        # Use standard title if not provided
        if not page_title:
            page_title = self._standard_page_types[page_type]["title"]
            
        # Create navigation item
        if page_type == "index":
            # Home page is usually linked with "#" or "/"
            nav_item = {
                "url": "/",
                "label": page_title,
                "type": "navitem"
            }
        else:
            # Other pages are linked with their slug
            nav_item = {
                "url": f"/{page_type}.html",
                "label": page_title,
                "type": "cta" if page_type == "shop" else "navitem"
            }
            
        return nav_item
        
    def remove_page(self, template_id: str, page_type: str) -> bool:
        """
        Remove a page configuration from a template.
        
        Args:
            template_id (str): The ID of the template.
            page_type (str): The type of page to remove.
            
        Returns:
            bool: True if the page was removed successfully, False otherwise.
            
        Raises:
            ValueError: If the template doesn't exist or the page type is not found.
        """
        # Check if the template exists
        if not self.registry.template_exists(template_id):
            raise ValueError(f"Template '{template_id}' not found")
            
        # Check if the page exists in the template
        template_config = self.registry.get_template_config(template_id)
        if not template_config or "pages" not in template_config or page_type not in template_config["pages"]:
            raise ValueError(f"Page '{page_type}' not found in template '{template_id}'")
            
        # In a real implementation, we would remove the page from the registry
        # For now, just return True to indicate success
        return True
        
    def remove_page_from_navigation(self, template_id: str, page_type: str) -> bool:
        """
        Remove a page from the navigation configuration of a template.
        
        Args:
            template_id (str): The ID of the template.
            page_type (str): The type of page to remove.
            
        Returns:
            bool: True if the page was removed from navigation successfully, False otherwise.
            
        Raises:
            ValueError: If the template doesn't exist.
        """
        # Check if the template exists
        if not self.registry.template_exists(template_id):
            raise ValueError(f"Template '{template_id}' not found")
            
        # In a real implementation, we would remove the page from the navigation
        # For now, just return True to indicate success
        return True
        
    def update_page(self, template_id: str, page_type: str, content: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Update a page configuration in a template.
        
        Args:
            template_id (str): The ID of the template.
            page_type (str): The type of page to update.
            content (Dict[str, Any], optional): Custom content for the page. Defaults to None.
            
        Returns:
            Dict[str, Any]: The updated page configuration.
            
        Raises:
            ValueError: If the template doesn't exist or the page type is not found.
        """
        # Check if the template exists
        if not self.registry.template_exists(template_id):
            raise ValueError(f"Template '{template_id}' not found")
            
        # Check if the page exists in the template
        template_config = self.registry.get_template_config(template_id)
        if not template_config or "pages" not in template_config or page_type not in template_config["pages"]:
            raise ValueError(f"Page '{page_type}' not found in template '{template_id}'")
            
        # Get the current page configuration
        page_config = template_config["pages"][page_type].copy()
        
        # Update with custom content if provided
        if content:
            for key, value in content.items():
                page_config[key] = value
                
        return page_config
        
    def update_page_in_navigation(self, template_id: str, page_type: str, page_title: str = None) -> Dict[str, Any]:
        """
        Update a page in the navigation configuration of a template.
        
        Args:
            template_id (str): The ID of the template.
            page_type (str): The type of page to update.
            page_title (str, optional): Custom title for the page. Defaults to None.
            
        Returns:
            Dict[str, Any]: The updated navigation item for the page.
            
        Raises:
            ValueError: If the template doesn't exist or the page type is not found.
        """
        # Check if the template exists
        if not self.registry.template_exists(template_id):
            raise ValueError(f"Template '{template_id}' not found")
            
        # Create an updated navigation item
        # In a real implementation, we would update the existing navigation item
        # For now, just create a new one with the updated title
        if not page_title:
            page_title = self._standard_page_types.get(page_type, {}).get("title", page_type.capitalize())
            
        if page_type == "index":
            nav_item = {
                "url": "/",
                "label": page_title,
                "type": "navitem"
            }
        else:
            nav_item = {
                "url": f"/{page_type}.html",
                "label": page_title,
                "type": "cta" if page_type == "shop" else "navitem"
            }
            
        return nav_item
