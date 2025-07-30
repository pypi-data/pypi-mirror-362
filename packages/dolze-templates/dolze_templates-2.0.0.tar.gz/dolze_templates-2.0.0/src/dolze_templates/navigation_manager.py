"""
Navigation Manager Module

This module provides functionality for managing navigation components within templates,
including creating, updating, and retrieving navigation configurations.
"""

import json
import pkgutil
from typing import Dict, Any, List, Optional

from .template_registry import TemplateRegistry

class NavigationManager:
    """
    Class for managing navigation components within templates.
    
    This class provides methods for creating, updating, and retrieving
    navigation configurations for templates.
    """
    
    def __init__(self):
        """Initialize the NavigationManager with a TemplateRegistry instance."""
        self.registry = TemplateRegistry()
    
    def get_navigation_config(self, template_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the navigation configuration for a template.
        
        Args:
            template_id (str): The ID of the template.
            
        Returns:
            Optional[Dict[str, Any]]: The navigation configuration, or None if not found.
        """
        template_config = self.registry.get_template_config(template_id)
        if not template_config:
            return None
            
        return template_config.get("navigation", {})
    
    def get_navigation_items(self, template_id: str) -> List[Dict[str, Any]]:
        """
        Get the navigation items for a template.
        
        Args:
            template_id (str): The ID of the template.
            
        Returns:
            List[Dict[str, Any]]: List of navigation items.
        """
        nav_config = self.get_navigation_config(template_id)
        if not nav_config:
            return []
            
        return nav_config.get("items", [])
    


    def generate_navigation_for_pages(self, template_id: str, pages: List[str]) -> Dict[str, Any]:
        """
        Generate a navigation configuration for a set of pages.
        
        Args:
            template_id (str): The ID of the template.
            pages (List[str]): List of page slugs to include in the navigation.
            
        Returns:
            Dict[str, Any]: The generated navigation configuration.
            
        Raises:
            ValueError: If the template doesn't exist.
        """
        # Check if the template exists
        if not self.registry.template_exists(template_id):
            raise ValueError(f"Template '{template_id}' not found")
            

        # If pages is an array with just one element that's 'index', return the full navigation config
        if pages and len(pages) == 1 and pages[0] == "index":
            return self.get_navigation_config(template_id)
            
        # Get the template configuration
        template_config = self.registry.get_template_config(template_id)
        if not template_config:
            raise ValueError(f"Template '{template_id}' has no configuration")
        
        # Use the navigation items directly from the template registry
        if "navigation" in template_config and "items" in template_config["navigation"]:
            return {"items": template_config["navigation"]["items"]}
        
        # If no navigation items are defined in the registry, generate them from pages
        if not template_config or "pages" not in template_config:
            raise ValueError(f"Template '{template_id}' has no pages configured")
            
        # Generate navigation items for each page as a fallback
        nav_items = []
        for page in pages:
            if page not in template_config["pages"]:
                continue
                
            page_config = template_config["pages"][page]
            title = page_config.get("title", page.capitalize())
            
            if page == "index":
                # Home page is usually linked with "#" or "/"
                nav_items.append({
                    "url": "/",
                    "label": title,
                    "type": "navitem"
                }) 
            else:
                # Other pages are linked with their slug
                nav_items.append({
                    "url": f"/{page}.html",
                    "label": title,
                    "type": "navitem"
                })
                
        return {"items": nav_items}
