"""
Template Registry - Single source of truth for all template definitions and logic
"""

from typing import Dict, Any, Optional, List
import os
import json
import re
from pathlib import Path
from PIL import Image

from dolze_image_templates.core.template_engine import Template
from dolze_image_templates.core.font_manager import get_font_manager
from dolze_image_templates.core.template_samples import get_sample_url


class TemplateRegistry:
    """
    Registry for managing and accessing all available templates.
    Acts as a single point of contact for template-related operations.
    """

    def __init__(self, templates_dir: Optional[str] = None):
        """
        Initialize the template registry.

        Args:
            templates_dir: Directory containing template definition files
        """
        self.templates: Dict[str, Dict[str, Any]] = {}
        self.templates_dir = templates_dir or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates"
        )
        self._load_templates()

    def _load_templates(self) -> None:
        """Load all templates from the templates directory."""
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir, exist_ok=True)
            return

        # Load all JSON files in the templates directory
        for file_path in Path(self.templates_dir).glob("*.json"):
            try:
                with open(file_path, "r") as f:
                    template_data = json.load(f)
                    if isinstance(template_data, dict) and "name" in template_data:
                        self.templates[template_data["name"]] = template_data
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading template from {file_path}: {e}")

    def _has_image_upload(self, config: Any) -> bool:
        """Check if the template configuration contains any image upload fields.

        Args:
            config: Template configuration or part of it

        Returns:
            bool: True if any field value is "${image_url}", False otherwise
        """
        if isinstance(config, str):
            return config == "${image_url}"

        if not isinstance(config, (dict, list)):
            return False

        if isinstance(config, dict):
            for value in config.values():
                if value == "${image_url}":
                    return True
                if isinstance(value, (dict, list)) and self._has_image_upload(value):
                    return True
        elif isinstance(config, list):
            for item in config:
                if item == "${image_url}":
                    return True
                if isinstance(item, (dict, list)) and self._has_image_upload(item):
                    return True

        return False

    def get_all_templates(self) -> List[Dict[str, Any]]:
        """
        Get information about all available templates.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing template information with keys:
                - template_name: str - Name of the template
                - isImageUploadPresent: bool - True if template contains any image upload fields
                - sample_url: str - Placeholder for future sample URL (currently empty string)
        """
        return [
    {
        "template_name": "calendar_app_promo",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('calendar_app_promo'),
        "formValues": {
            "image_url": { "field": "image_url", "type": "image", "minLength": 0, "maxLength": 1000,"isTransparentImage": True },
            "heading": { "field": "heading", "type": "text", "minLength": 1, "maxLength": 50 },
            "cta_text": { "field": "cta_text", "type": "text", "minLength": 1, "maxLength": 20 },
            "subheading": { "field": "subheading", "type": "text", "minLength": 1, "maxLength": 100 }
        }
    },
    {
        "template_name": "testimonials_template",
        "isImageUploadPresent": False,
        "sample_url": get_sample_url('testimonials_template'),
        "formValues": {
            "user_name": { "field": "user_name", "type": "text", "minLength": 1, "maxLength": 50 },
            "user_title": { "field": "user_title", "type": "text", "minLength": 1, "maxLength": 100 },
            "testimonial_text": { "field": "testimonial_text", "type": "text", "minLength": 1, "maxLength": 189 }
        }
    },
    {
        "template_name": "coming_soon_post_2",
        "isImageUploadPresent": False,
        "sample_url": get_sample_url('coming_soon_post_2'),
        "formValues": {
            "text": { "field": "text", "type": "text", "minLength": 50, "maxLength": 84 },
            "cta_text": { "field": "cta_text", "type": "text", "minLength": 15, "maxLength": 28 }
        }
    },
    {
        "template_name": "blog_post",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('blog_post'),
        "formValues": {
            "title": { "field": "title", "type": "text", "minLength": 1, "maxLength": 100 },
            "author": { "field": "author", "type": "text", "minLength": 1, "maxLength": 50 },
            "read_time": { "field": "read_time", "type": "number", "minLength": 1, "maxLength": 3 },
            "image_url": { "field": "image_url", "type": "image", "minLength": 0, "maxLength": 1000 },
            "website_url": { "field": "website_url", "type": "url", "minLength": 1, "maxLength": 200 },
            "publish_date": { "field": "publish_date", "type": "text", "minLength": 10, "maxLength": 10 },
            "excerpt": { "field": "excerpt", "type": "text", "minLength": 1, "maxLength": 200 }
        }
    },
    {
        "template_name": "blog_post_2",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('blog_post_2'),
        "formValues": {
            "title": { "field": "title", "type": "text", "minLength": 1, "maxLength": 100 },
            "author": { "field": "author", "type": "text", "minLength": 1, "maxLength": 50 },
            "read_time": { "field": "read_time", "type": "number", "minLength": 1, "maxLength": 3 },
            "image_url": { "field": "image_url", "type": "image", "minLength": 0, "maxLength": 1000 },
            "publish_date": { "field": "publish_date", "type": "text", "minLength": 10, "maxLength": 10 },
            "excerpt": { "field": "excerpt", "type": "text", "minLength": 1, "maxLength": 200 }
        }
    },
    {
        "template_name": "qa_template",
        "isImageUploadPresent": False,
        "sample_url": get_sample_url('qa_template'),
        "formValues": {
            "question": { "field": "question", "type": "text", "minLength": 1, "maxLength": 28 },
            "answer": { "field": "answer", "type": "text", "minLength": 1, "maxLength": 200 },
            "username": { "field": "username", "type": "text", "minLength": 1, "maxLength": 50 },
            "website_url": { "field": "website_url", "type": "url", "minLength": 1, "maxLength": 200 },
        }
    },
    {
        "template_name": "qa_template_2",
        "isImageUploadPresent": False,
        "sample_url": get_sample_url('qa_template_2'),
        "formValues": {
            "question": { "field": "question", "type": "text", "minLength": 1, "maxLength": 28 },
            "answer": { "field": "answer", "type": "text", "minLength": 150, "maxLength": 280 },
            "username": { "field": "username", "type": "text", "minLength": 1, "maxLength": 50 },
            "website_url": { "field": "website_url", "type": "url", "minLength": 1, "maxLength": 200 },

        }
    },
    
    {
        "template_name": "quote_template",
        "isImageUploadPresent": False,
        "sample_url": get_sample_url('quote_template'),
        "formValues": {
            "quote": { "field": "quote", "type": "text", "minLength": 70, "maxLength": 126 },
          
            "username": { "field": "username", "type": "text", "minLength": 1, "maxLength": 50 }
        }
    },
    {
        "template_name": "quote_template_2",
        "isImageUploadPresent": False,
        "sample_url": get_sample_url('quote_template_2'),
        "formValues": {
            "quote1": { "field": "quote1", "type": "text", "minLength": 175, "maxLength": 280 },
            "quote2": { "field": "quote2", "type": "text", "minLength": 1, "maxLength": 200 },
            "username": { "field": "username", "type": "text", "minLength": 1, "maxLength": 50 }
        }
    },
    {
        "template_name": "education_info",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('education_info'),
        "formValues": {
            "product_info": { "field": "product_info", "type": "text", "min ironLength": 1, "maxLength": 600 },
            "product_name": { "field": "product_name", "type": "text", "minLength": 1, "maxLength": 50 },
            "author": { "field": "author", "type": "text", "minLength": 1, "maxLength": 50 },
            "read_time": { "field": "read_time", "type": "number", "minLength": 1, "maxLength": 3 },
            "image_url": { "field": "image_url", "type": "image", "minLength": 0, "maxLength": 1000 }
        }
    },
    {
        "template_name": "education_info_2",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('education_info_2'),
        "formValues": {
            "product_info": { "field": "product_info", "type": "text", "minLength": 1, "maxLength": 300 },
            "author": { "field": "author", "type": "text", "minLength": 1, "maxLength": 50 },
            "read_time": { "field": "read_time", "type": "number", "minLength": 1, "maxLength": 3 },
            "image_url": { "field": "image_url", "type": "image", "minLength": 0, "maxLength": 1000 }
        }
    },
    {
        "template_name": "product_promotion",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('product_promotion'),
        "formValues": {
            "image_url": { "field": "image_url", "type": "image", "minLength": 0, "maxLength": 1000 },
            "heading": { "field": "heading", "type": "text", "minLength": 1, "maxLength": 21 },
            "subheading": { "field": "subheading", "type": "text", "minLength": 150, "maxLength": 280 },
            "cta_text": { "field": "cta_text", "type": "text", "minLength": 1, "maxLength": 14 },
            "website_url": { "field": "website_url", "type": "url", "minLength": 1, "maxLength": 14 },
            "logo_url": { "field": "logo_url", "type": "image", "minLength": 0, "maxLength": 1000 }
        }
    },
    {
        "template_name": "product_promotion_2",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('product_promotion_2'),
        "formValues": {
            "image_url": { "field": "image_url", "type": "image", "minLength": 0, "maxLength": 1000 ,"isTransparentImage": True},
            "quote1": { "field": "quote1", "type": "text", "minLength": 15, "maxLength": 28 },
            "quote2": { "field": "quote2", "type": "text", "minLength": 1, "maxLength": 50 }
        }
    },
    {
        "template_name": "product_showcase",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('product_showcase'),
        "formValues": {
            "product_image": { "field": "product_image", "type": "image", "minLength": 0, "maxLength": 1000 },
            "product_name": { "field": "product_name", "type": "text", "minLength": 1, "maxLength": 50 },
            "product_price": { "field": "product_price", "type": "text", "minLength": 1, "maxLength": 20 },
            "product_description": { "field": "product_description", "type": "text", "minLength": 1, "maxLength": 100 },
            "badge_text": { "field": "badge_text", "type": "text", "minLength": 1, "maxLength": 20 }
        }
    },
    {
        "template_name": "product_showcase_2",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('product_showcase_2'),
        "formValues": {
            "product_image": { "field": "product_image", "type": "image", "minLength": 0, "maxLength": 1000 },
            "product_name": { "field": "product_name", "type": "text", "minLength": 1, "maxLength": 50 },
            "product_price": { "field": "product_price", "type": "text", "minLength": 1, "maxLength": 20 },
            "product_description": { "field": "product_description", "type": "text", "minLength": 90, "maxLength": 147 },
            "badge_text": { "field": "badge_text", "type": "text", "minLength": 10, "maxLength": 10 }
        }
    },
    {
        "template_name": "coming_soon_page",
        "isImageUploadPresent": False,
        "sample_url": get_sample_url('coming_soon_page'),
        "formValues": {
            "header_text": { "field": "header_text", "type": "text", "minLength": 1, "maxLength": 21 },
            "contact_email": { "field": "contact_email", "type": "email", "minLength": 5, "maxLength": 100 },
            "website_url": { "field": "website_url", "type": "url", "minLength": 1, "maxLength": 200 },
            "contact_details": { "field": "contact_details", "type": "text", "minLength": 1, "maxLength": 200 }
        }
    },
    {
        "template_name": "product_showcase_3",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('product_showcase_3'),
        "formValues": {
            "product_image": { "field": "product_image", "type": "image", "minLength": 0, "maxLength": 1000,"isTransparentImage": True },
            "product_name": { "field": "product_name", "type": "text", "minLength": 1, "maxLength": 21 },
            "product_price": { "field": "product_price", "type": "text", "minLength": 1, "maxLength": 20 },
            "product_description": { "field": "product_description", "type": "text", "minLength": 30, "maxLength": 49 },
            "cta_text": { "field": "cta_text", "type": "text", "minLength": 1, "maxLength": 14 }
        }
    },
    {
        "template_name": "coming_soon",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('coming_soon'),
        "formValues": {
            "background_image_url": { "field": "background_image_url", "type": "image", "minLength": 0, "maxLength": 1000 },
            "business_name": { "field": "business_name", "type": "text", "minLength": 1, "maxLength": 50 },
            "text": { "field": "text", "type": "text", "minLength": 1, "maxLength": 21 },
            "website_url": { "field": "website_url", "type": "url", "minLength": 1, "maxLength": 200 },
            "heading": { "field": "heading", "type": "text", "minLength": 1, "maxLength": 50 },
            "subheading": { "field": "subheading", "type": "text", "minLength": 1, "maxLength": 100 }
        }
    },
    {
        "template_name": "event_day",
        "isImageUploadPresent": False,
        "sample_url": get_sample_url('event_day'),
        "formValues": {
            "celebration_name": { "field": "celebration_name", "type": "text", "minLength": 1, "maxLength": 21 },
            "celebration_text": { "field": "celebration_text", "type": "text", "minLength": 1, "maxLength": 21 },
            "celebration_description": { "field": "celebration_description", "type": "text", "minLength": 40, "maxLength": 70 },
            "theme_color": { "field": "theme_color", "type": "text", "minLength": 4, "maxLength": 7 }
        }
    },
    {
        "template_name": "hiring_post",
        "isImageUploadPresent": False,
        "sample_url": get_sample_url('hiring_post'),
        "formValues": {
            "heading": { "field": "heading", "type": "text", "minLength": 1, "maxLength": 21 },
            "subheading": { "field": "subheading", "type": "text", "minLength": 1, "maxLength": 100 },
            "theme_color": { "field": "theme_color", "type": "text", "minLength": 4, "maxLength": 7 },
            "cta_text": { "field": "cta_text", "type": "text", "minLength": 1, "maxLength": 14 },
            "job_title": { "field": "job_title", "type": "text", "minLength": 1, "maxLength": 21 },
            "company_name": { "field": "company_name", "type": "text", "minLength": 1, "maxLength": 50 }
        }
    },
    {
        "template_name": "product_sale",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('product_sale'),
        "formValues": {
            "cta_text": { "field": "cta_text", "type": "text", "minLength": 1, "maxLength": 14 },
            "sale_end_text": { "field": "sale_end_text", "type": "text", "minLength": 1, "maxLength": 20 },
            "product_name": { "field": "product_name", "type": "text", "minLength": 1, "maxLength": 50 },
            "product_description": { "field": "product_description", "type": "text", "minLength": 20, "maxLength": 35 },
            "sale_heading": { "field": "sale_heading", "type": "text", "minLength": 1, "maxLength": 21 },
            "sale_text": { "field": "sale_text", "type": "text", "minLength": 15, "maxLength": 28 },
            "background_image_url": { "field": "background_image_url", "type": "image", "minLength": 0, "maxLength": 1000 },
            "theme_color": { "field": "theme_color", "type": "text", "minLength": 4, "maxLength": 7 },
            "product_image": { "field": "product_image", "type": "image", "minLength": 0, "maxLength": 1000 ,"isTransparentImage": True}
        }
    },
    {
        "template_name": "product_service_minimal",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('product_service_minimal'),
        "formValues": {
            "text": { "field": "text", "type": "text", "minLength": 40, "maxLength": 70 },
            "website_url": { "field": "website_url", "type": "url", "minLength": 1, "maxLength": 200 },
            "product_image": { "field": "product_image", "type": "image", "minLength": 0, "maxLength": 1000 },
            "theme_color": { "field": "theme_color", "type": "text", "minLength": 4, "maxLength": 7 }
        }
    },
    {
        "template_name": "product_showcase_4",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('product_showcase_4'),
        "formValues": {
            "product_image": { "field": "product_image", "type": "image", "minLength": 0, "maxLength": 1000,"isTransparentImage": True },
            "offer_text": { "field": "offer_text", "type": "text", "minLength": 1, "maxLength": 21 },
            "website_url": { "field": "website_url", "type": "url", "minLength": 1, "maxLength": 200 },
            "theme_color": { "field": "theme_color", "type": "text", "minLength": 4, "maxLength": 7 }
        }
    },
    {
        "template_name": "summer_sale_promotion",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('summer_sale_promotion'),
        "formValues": {
            "background_image_url": { "field": "background_image_url", "type": "image", "minLength": 0, "maxLength": 1000 },
            "brand_name": { "field": "brand_name", "type": "text", "minLength": 1, "maxLength": 50 },
            "sale_heading": { "field": "sale_heading", "type": "text", "minLength": 1, "maxLength": 50 },
            "sale_description": { "field": "sale_description", "type": "text", "minLength": 1, "maxLength": 56 },
            "theme_color": { "field": "theme_color", "type": "text", "minLength": 4, "maxLength": 7 },
            "discount_text": { "field": "discount_text", "type": "text", "minLength": 15, "maxLength": 28 },
            "social_handle": { "field": "social_handle", "type": "text", "minLength": 1, "maxLength": 50 },
            "contact_number": { "field": "contact_number", "type": "tel", "minLength": 10, "maxLength": 15 }
        }
    },
    {
        "template_name": "testimonials_template_2",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('testimonials_template_2'),
        "formValues": {
            "testimonial_text": { "field": "testimonial_text", "type": "text", "minLength": 20, "maxLength": 200 },
            "user_avatar": { "field": "user_avatar", "type": "image", "minLength": 0, "maxLength": 1000 },
            "user_name": { "field": "user_name", "type": "text", "minLength": 1, "maxLength": 50 },
            "user_title": { "field": "user_title", "type": "text", "minLength": 1, "maxLength": 100 },
            "website_url": { "field": "website_url", "type": "url", "minLength": 1, "maxLength": 200 },
            "theme_color": { "field": "theme_color", "type": "text", "minLength": 4, "maxLength": 7 }
        }
    },
    {
        "template_name": "product_showcase_5",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('product_showcase_5'),
        "formValues": {
            "heading": { "field": "heading", "type": "text", "minLength": 1, "maxLength": 28 },
            "subheading": { "field": "subheading", "type": "text", "minLength": 1, "maxLength": 280 },
            "cta_text": { "field": "cta_text", "type": "text", "minLength": 1, "maxLength": 20 },
            "contact_number": { "field": "contact_number", "type": "tel", "minLength": 10, "maxLength": 15 },
            "website_url": { "field": "website_url", "type": "url", "minLength": 1, "maxLength": 200 },
            "product_image": { "field": "product_image", "type": "image", "minLength": 0, "maxLength": 1000 ,"isTransparentImage": True}
        }
    },
    {
        "template_name": "brand_info",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('brand_info'),
        "formValues": {
            "product_image": { "field": "product_image", "type": "image", "minLength": 0, "maxLength": 1000 },
            "heading": { "field": "heading", "type": "text", "minLength": 1, "maxLength": 35 },
            "subheading": { "field": "subheading", "type": "text", "minLength": 100, "maxLength": 175 },
            "cta_text": { "field": "cta_text", "type": "text", "minLength": 10, "maxLength": 28 }
        }
    },
    {
    "template_name": "product_marketing",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('product_marketing'),
        "formValues": {
            "social_handle": "@dolze.ai",
            "heading": { "field": "heading", "type": "text", "minLength": 1, "maxLength": 26 },
            "subheading":{ "field": "subheading", "type": "text", "minLength": 100, "maxLength": 175 },
            "background_image_url": { "field": "background_image_url", "type": "image", "minLength": 0, "maxLength": 1000 },
        }        
    },
    {
    "template_name": "brand_info_2",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('brand_info_2'),
        "formValues": {
            "service_hook": {"field": "service_hook", "type": "text", "minLength": 1, "maxLength": 23 },
            "service_hook": {"field": "service_hook", "type": "text", "minLength": 1, "maxLength": 12 },
            "content":{"field": "content", "type": "text", "minLength": 1, "maxLength": 50 },
            "contact_number": {"field": "contact_number", "type": "text", "minLength": 1, "maxLength": 12 },
            "website_url":{"field": "website_url", "type": "text", "minLength": 1, "maxLength": 35 },
            "product_image": { "field": "product_image", "type": "image", "minLength": 0, "maxLength": 1000 },
            "contact_email": {"field": "contact_email", "type": "text", "minLength": 1, "maxLength": 25 },     
        }        
    },
    {
        "template_name": "product_sale_2",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('product_sale_2'),
        "formValues": {
            "theme_color": { "field": "theme_color", "type": "text", "minLength": 4, "maxLength": 7 },
            "product_image": { "field": "product_image", "type": "image", "minLength": 0, "maxLength": 1000, "isTransparentImage": True },
            "heading": { "field": "heading", "type": "text", "minLength": 1, "maxLength": 26 },
            "usp1": { "field": "usp1", "type": "text", "minLength": 1, "maxLength": 16 },
            "usp2": { "field": "usp2", "type": "text", "minLength": 1, "maxLength": 16 },
            "cta_text": { "field": "cta_text", "type": "text", "minLength": 1, "maxLength": 10 },
            "product_highlights": { "field": "product_highlights", "type": "text", "minLength": 1, "maxLength": 14 },
            "social_handle": { "field": "social_handle", "type": "text", "minLength": 1, "maxLength": 25 },
            "business_name": { "field": "business_name", "type": "text", "minLength": 1, "maxLength": 25 }
        }        
    },
    {
        "template_name": "product_feature",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('product_feature'),
        "formValues": {
            "product_image": { "field": "product_image", "type": "image", "minLength": 0, "maxLength": 1000,"isTransparentImage": True },
            "feature1": { "field": "feature1", "type": "text", "minLength": 1, "maxLength": 50 },
            "feature2": { "field": "feature2", "type": "text", "minLength": 1, "maxLength": 50 },
            "feature3": { "field": "feature3", "type": "text", "minLength": 1, "maxLength": 50 },
            "feature4": { "field": "feature4", "type": "text", "minLength": 1, "maxLength": 50 },
            "feature_title": { "field": "feature_title", "type": "text", "minLength": 1, "maxLength": 10 },
            "product_name": { "field": "product_name", "type": "text", "minLength": 1, "maxLength": 10 }
        }
    },
    {
        "template_name": "event_alert",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('event_alert'),
        "formValues": {
            "company_name": { "field": "company_name", "type": "text", "minLength": 1, "maxLength": 50 },
            "event_type": { "field": "event_type", "type": "text", "minLength": 1, "maxLength": 20 },
            "event_date": { "field": "event_date", "type": "text", "minLength": 1, "maxLength": 20 },
            "event_time": { "field": "event_time", "type": "text", "minLength": 1, "maxLength": 22 },
            "event_highlight": { "field": "event_highlight", "type": "text", "minLength": 1, "maxLength": 200 },
            "register_details": { "field": "register_details", "type": "text", "minLength": 1, "maxLength": 100 },
            "product_image": { "field": "product_image", "type": "image", "minLength": 0, "maxLength": 1000,"isTransparentImage": True }
        }
    },
    {
        "template_name": "sale_alert",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('sale_alert'),
        "formValues": {
            "sale_heading": { "field": "sale_heading", "type": "text", "minLength": 1, "maxLength": 16 },
            "sale_description": { "field": "sale_description", "type": "text", "minLength": 1, "maxLength": 35 },
            "cta_text": { "field": "cta_text", "type": "text", "minLength": 1, "maxLength": 20 },
            "website_url": { "field": "website_url", "type": "url", "minLength": 1, "maxLength": 100 },
            "sale_text": { "field": "sale_text", "type": "text", "minLength": 1, "maxLength": 14 },
            "product_image": { "field": "product_image", "type": "image", "minLength": 0, "maxLength": 1000,"isTransparentImage": True },
        }
    },
    {
        "template_name": "testimonials",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('testimonials'),
        "formValues": {
            "product_image": { "field": "product_image", "type": "image", "minLength": 0, "maxLength": 1000 },
            "name": { "field": "name", "type": "text", "minLength": 1, "maxLength": 15 },
            "greeting": { "field": "greeting", "type": "text", "minLength": 1, "maxLength": 20 },
            "designation": { "field": "designation", "type": "text", "minLength": 1, "maxLength": 500 },
            "social_handle": { "field": "social_handle", "type": "text", "minLength": 1, "maxLength": 50 }
        }
    },
    {
        "template_name": "event_announcement",
        "isImageUploadPresent": True,
        "sample_url": get_sample_url('event_announcement'),
        "formValues": {
            "event_image": { "field": "event_image", "type": "image", "minLength": 0, "maxLength": 1000 },
            "event_name": { "field": "event_name", "type": "text", "minLength": 1, "maxLength": 10 },
            "event_description": { "field": "event_description", "type": "text", "minLength": 1, "maxLength": 150 },
            "company_name": { "field": "company_name", "type": "text", "minLength": 1, "maxLength": 30 }
        }
    }
]

    def register_template(self, name: str, config: Dict[str, Any]) -> None:
        """
        Register a new template.

        Args:
            name: Name of the template
            config: Template configuration dictionary
        """
        if not name:
            raise ValueError("Template name cannot be empty")

        # Ensure required fields are present
        required_fields = ["components"]
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Template config is missing required field: {field}")

        # Set default values
        config.setdefault("name", name)
        config.setdefault("size", {"width": 1080, "height": 1080})
        config.setdefault("background_color", [255, 255, 255])
        config.setdefault("use_base_image", False)

        self.templates[name] = config

        # Save to file
        self._save_template(name, config)

    def _save_template(self, name: str, config: Dict[str, Any]) -> None:
        """
        Save a template to a JSON file.

        Args:
            name: Name of the template
            config: Template configuration
        """
        try:
            os.makedirs(self.templates_dir, exist_ok=True)
            file_path = os.path.join(self.templates_dir, f"{name}.json")
            with open(file_path, "w") as f:
                json.dump(config, f, indent=2)
        except IOError as e:
            print(f"Error saving template {name}: {e}")

    def get_template(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a template configuration by name.

        Args:
            name: Name of the template

        Returns:
            Template configuration dictionary or None if not found
        """
        return self.templates.get(name)

    def get_template_names(self) -> List[str]:
        """
        Get a list of all available template names.

        Returns:
            List of template names
        """
        return list(self.templates.keys())

    def create_template_instance(
        self, name: str, variables: Optional[Dict[str, Any]] = None
    ) -> Optional[Template]:
        """
        Create a template instance with the given variables.

        Args:
            name: Name of the template
            variables: Dictionary of variables to substitute in the template

        Returns:
            A Template instance or None if the template is not found
        """
        template_config = self.get_template(name)
        if not template_config:
            return None

        # Create a deep copy of the config to avoid modifying the original
        config = json.loads(json.dumps(template_config))

        # Apply variable substitution if variables are provided
        if variables:
            config = self._substitute_variables(config, variables)

        return Template.from_config(config)

    def _substitute_variables(self, config: Any, variables: Dict[str, Any]) -> Any:
        """
        Recursively substitute variables in the template configuration.

        Args:
            config: Template configuration or part of it
            variables: Dictionary of variables to substitute

        Returns:
            Configuration with variables substituted
        """
        if isinstance(config, dict):
            result = {}
            for key, value in config.items():
                result[key] = self._substitute_variables(value, variables)
            return result
        elif isinstance(config, list):
            return [self._substitute_variables(item, variables) for item in config]
        elif isinstance(config, str):
            # Replace ${variable} with the corresponding value
            def replace_match(match):
                var_name = match.group(1)
                return str(variables.get(var_name, match.group(0)))

            return re.sub(r"\${([^}]+)}", replace_match, config)
        else:
            return config

    def render_template(
        self,
        template_name: str,
        variables: Dict[str, Any],
        output_path: Optional[str] = None,
    ) -> Optional[Image.Image]:
        """
        Render a template with the given variables.

        Args:
            template_name: Name of the template to render
            variables: Dictionary of variables to substitute in the template
            output_path: Optional path to save the rendered image

        Returns:
            Rendered PIL Image or None if rendering fails
        """
        template = self.create_template_instance(template_name, variables)
        if not template:
            return None

        # Render the template
        rendered_image = template.render()

        # Save to file if output path is provided
        if output_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            rendered_image.save(output_path)

        return rendered_image


# Singleton instance for easy access
_instance = None


def get_template_registry(templates_dir: Optional[str] = None) -> TemplateRegistry:
    """
    Get the singleton instance of the template registry.

    Args:
        templates_dir: Optional directory containing template definitions

    Returns:
        TemplateRegistry instance
    """
    global _instance
    if _instance is None:
        _instance = TemplateRegistry(templates_dir)
    return _instance
