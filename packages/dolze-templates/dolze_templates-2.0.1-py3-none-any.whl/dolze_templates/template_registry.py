"""
Template Registry Module

This module provides functionality for managing the template registry,
which contains configuration for all available templates.
"""

import json
import pkgutil
from typing import Dict, Any, Optional, List

class TemplateRegistry:
    """
    Class for managing the template registry.
    
    The template registry contains configuration for all available templates,
    including page layouts, section variants, and navigation settings.
    """
    
    def __init__(self):
        """Initialize the TemplateRegistry with an empty cache."""
        self._registry_cache = None
    
    def get_all_templates(self) -> Dict[str, Any]:
        """
        Get the complete template registry.
        
        Returns:
            Dict[str, Any]: The template registry configuration.
            
        Raises:
            ValueError: If the template registry cannot be loaded.
        """
        if self._registry_cache is not None:
            return self._registry_cache
        
        try:
            # Use pkgutil to get the template registry
            data = pkgutil.get_data('dolze_templates', 'template-registry.json')
            if data:
                self._registry_cache = json.loads(data.decode('utf-8'))
                return self._registry_cache
            else:
                raise ValueError("Could not load template registry")
        except Exception as e:
            raise ValueError(f"Failed to load template registry: {e}")
    
    def get_template_config(self, template_id: str) -> Optional[Dict[str, Any]]:
        """
        Get configuration for a specific template.
        
        Args:
            template_id (str): The ID of the template.
            
        Returns:
            Optional[Dict[str, Any]]: The template configuration, or None if not found.
        """
        registry = self.get_all_templates()
        return registry.get(template_id)
    
    def template_exists(self, template_id: str) -> bool:
        """
        Check if a template exists in the registry.
        
        Args:
            template_id (str): The ID of the template.
            
        Returns:
            bool: True if the template exists, False otherwise.
        """
        registry = self.get_all_templates()
        return template_id in registry
    
    def get_template_pages(self, template_id: str) -> Optional[Dict[str, Any]]:
        """
        Get pages configuration for a specific template.
        
        Args:
            template_id (str): The ID of the template.
            
        Returns:
            Optional[Dict[str, Any]]: The pages configuration, or None if not found.
        """
        template_config = self.get_template_config(template_id)
        if template_config:
            return template_config.get("pages")
        return None
    
    def get_navigation_config(self, template_id: str) -> Optional[Dict[str, Any]]:
        """
        Get navigation configuration for a specific template.
        
        Args:
            template_id (str): The ID of the template.
            
        Returns:
            Optional[Dict[str, Any]]: The navigation configuration, or None if not found.
        """
        template_config = self.get_template_config(template_id)
        if template_config:
            return template_config.get("navigation")
        return None
    
    def get_section_variants_config(self, template_id: str) -> Optional[Dict[str, Any]]:
        """
        Get section variants configuration for a specific template.
        
        Args:
            template_id (str): The ID of the template.
            
        Returns:
            Optional[Dict[str, Any]]: The section variants configuration, or None if not found.
        """
        template_config = self.get_template_config(template_id)
        if template_config:
            return template_config.get("section_variants")
        return None
