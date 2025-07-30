"""
UI Component Manager Module

This module provides functionality for managing UI components within templates,
including buttons, CTAs, and other interactive elements.
"""

import json
import pkgutil
from typing import Dict, Any, List, Optional

from .template_registry import TemplateRegistry

class UIComponentManager:
    """
    Class for managing UI components within templates.
    
    This class provides methods for creating, updating, and retrieving
    UI component configurations for templates, including buttons, CTAs,
    and other interactive elements.
    """
    
    def __init__(self):
        """Initialize the UIComponentManager with a TemplateRegistry instance."""
        self.registry = TemplateRegistry()
        
        # Define standard UI component types with their default configurations
        self._standard_components = {
            "button": {
                "primary": {
                    "class": "btn btn-primary",
                    "hover_class": "btn-hover",
                    "style": "rounded"
                },
                "secondary": {
                    "class": "btn btn-secondary",
                    "hover_class": "btn-hover",
                    "style": "rounded-sm"
                },
                "tertiary": {
                    "class": "btn btn-tertiary",
                    "hover_class": "btn-hover",
                    "style": "flat"
                }
            },
            "cta": {
                "primary": {
                    "class": "cta cta-primary",
                    "hover_class": "cta-hover",
                    "style": "rounded-lg"
                },
                "secondary": {
                    "class": "cta cta-secondary",
                    "hover_class": "cta-hover",
                    "style": "rounded"
                }
            },
            "card": {
                "default": {
                    "class": "card",
                    "hover_class": "card-hover",
                    "style": "shadow-sm"
                },
                "featured": {
                    "class": "card card-featured",
                    "hover_class": "card-hover",
                    "style": "shadow-md"
                }
            }
        }
    
    def get_component_config(self, component_type: str, variant: str = "default") -> Dict[str, Any]:
        """
        Get the configuration for a UI component.
        
        Args:
            component_type (str): The type of component (e.g., "button", "cta").
            variant (str, optional): The variant of the component. Defaults to "default".
            
        Returns:
            Dict[str, Any]: The component configuration.
            
        Raises:
            ValueError: If the component type or variant is not recognized.
        """
        if component_type not in self._standard_components:
            raise ValueError(f"Unknown component type: {component_type}")
            
        # If variant is not specified or not found, use the first available variant
        if variant not in self._standard_components[component_type]:
            # Get the first variant as default
            variant = next(iter(self._standard_components[component_type]))
            
        return self._standard_components[component_type][variant].copy()
    
    def get_available_component_types(self) -> List[str]:
        """
        Get a list of available UI component types.
        
        Returns:
            List[str]: List of available component type names.
        """
        return list(self._standard_components.keys())
    
    def get_available_variants(self, component_type: str) -> List[str]:
        """
        Get a list of available variants for a UI component type.
        
        Args:
            component_type (str): The type of component.
            
        Returns:
            List[str]: List of available variant names.
            
        Raises:
            ValueError: If the component type is not recognized.
        """
        if component_type not in self._standard_components:
            raise ValueError(f"Unknown component type: {component_type}")
            
        return list(self._standard_components[component_type].keys())
    
    def create_button(self, label: str, url: str, variant: str = "primary", 
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
        # Get the base button configuration
        button_config = self.get_component_config("button", variant)
        
        # Add button-specific properties
        button_config.update({
            "label": label,
            "url": url,
            "type": "button"
        })
        
        # Add additional classes if provided
        if additional_classes:
            button_config["class"] = f"{button_config['class']} {additional_classes}"
            
        # Add additional attributes if provided
        if attributes:
            button_config["attributes"] = attributes
            
        return button_config
    
    def create_cta(self, label: str, url: str, variant: str = "primary", 
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
        # Get the base CTA configuration
        cta_config = self.get_component_config("cta", variant)
        
        # Add CTA-specific properties
        cta_config.update({
            "label": label,
            "url": url,
            "type": "cta"
        })
        
        # Add additional classes if provided
        if additional_classes:
            cta_config["class"] = f"{cta_config['class']} {additional_classes}"
            
        # Add additional attributes if provided
        if attributes:
            cta_config["attributes"] = attributes
            
        return cta_config
    
    def create_card(self, title: str, content: str, image_url: str = None, 
                   link_url: str = None, variant: str = "default", 
                   additional_classes: str = "") -> Dict[str, Any]:
        """
        Create a card configuration.
        
        Args:
            title (str): The card title.
            content (str): The card content text.
            image_url (str, optional): URL to the card image. Defaults to None.
            link_url (str, optional): URL the card links to. Defaults to None.
            variant (str, optional): The card variant. Defaults to "default".
            additional_classes (str, optional): Additional CSS classes. Defaults to "".
            
        Returns:
            Dict[str, Any]: The card configuration.
        """
        # Get the base card configuration
        card_config = self.get_component_config("card", variant)
        
        # Add card-specific properties
        card_config.update({
            "title": title,
            "content": content,
            "type": "card"
        })
        
        # Add optional properties if provided
        if image_url:
            card_config["image_url"] = image_url
            
        if link_url:
            card_config["link_url"] = link_url
            
        # Add additional classes if provided
        if additional_classes:
            card_config["class"] = f"{card_config['class']} {additional_classes}"
            
        return card_config
    
    def get_template_components(self, template_id: str) -> Dict[str, Any]:
        """
        Get all UI components defined for a template.
        
        Args:
            template_id (str): The ID of the template.
            
        Returns:
            Dict[str, Any]: Dictionary of UI components defined for the template.
        """
        template_config = self.registry.get_template_config(template_id)
        if not template_config:
            return {}
            
        return template_config.get("components", {})
    
    def get_component_for_template(self, template_id: str, component_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific UI component defined for a template.
        
        Args:
            template_id (str): The ID of the template.
            component_id (str): The ID of the component.
            
        Returns:
            Optional[Dict[str, Any]]: The component configuration, or None if not found.
        """
        components = self.get_template_components(template_id)
        return components.get(component_id)
