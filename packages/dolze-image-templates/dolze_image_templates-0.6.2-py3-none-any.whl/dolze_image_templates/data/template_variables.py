"""
Template Variables Registry

This module provides a registry of template variables for different template types.
Each template type has its own set of required and optional variables with example values.
"""

from typing import Dict, Any, TypedDict, Optional
from typing_extensions import NotRequired


class TemplateVariables(TypedDict, total=False):
    """Base class for template variables with common fields."""

    website_url: NotRequired[str]


class CalendarAppPromoVars(TemplateVariables):
    """Variables for calendar app promotion template."""

    cta_text: str
    image_url: str
    cta_image: str
    heading: str
    subheading: str
    contact_email: str
    contact_phone: str
    quote: str
    user_avatar: str
    user_name: str
    user_title: str
    testimonial_text: str


class TestimonialVars(TemplateVariables):
    """Variables for testimonial template."""

    user_avatar: str
    user_name: str
    user_title: str
    testimonial_text: str


class EventAnnouncementVars(TemplateVariables):
    """Variables for event announcement template."""

    event_image: str
    event_name: str
    event_description: str
    company_name: str


class BlogPostVars(TemplateVariables):
    """Variables for blog post template."""

    title: str
    author: str
    read_time: str
    image_url: str


class QATemplateVars(TemplateVariables):
    """Variables for Q&A template."""

    question: str
    answer: str
    username: str


class QuoteTemplateVars(TemplateVariables):
    """Variables for quote template."""

    quote1: str
    quote2: str
    username: str


class EducationInfoVars(TemplateVariables):
    """Variables for education info template."""

    testimonial_text: str
    author: str
    read_time: str
    image_url: str


class ProductPromotionVars(TemplateVariables):
    """Variables for product promotion template."""

    image_url: str
    quote1: str
    quote2: str


class ProductShowcaseVars(TemplateVariables):
    """Variables for product showcase template."""

    product_image: str
    product_name: str
    product_price: str
    product_description: str
    badge_text: str


# Registry mapping template names to their variable types and example values
TEMPLATE_VARIABLES_REGISTRY: Dict[str, Dict[str, Any]] = {
    "calendar_app_promo": {
        "type": "promotional",
        "description": "Calendar app promotion template",
        "variables": {
            "image_url": "Generate a prompt for  product image which has transparent background as a png image. Make sure just the product is visible and the background is transparent. Also dont keep any text in the image. Make sure it has transparent background makes sure it has transparent background (alpha PNG) and also has isolated object cut-out Isolated object cut-out on a completely transparent background (alpha PNG). No floor, no shadows, no reflections, no props, no text—only the product, perfectly lit",
            "heading": "Plan your day in a snap",
            
        },
        "required": ["cta_text", "image_url", "heading", "subheading"],
    },
    "testimonials_template": {
        "type": "testimonial",
        "description": "Customer testimonial template",
        "variables": {
            "user_name": "Sarah Johnson",
            "user_title": "Verified Buyer",
            "testimonial_text": "This product has transformed how we work in under 27 words",
        },
        "required": ["user_name", "testimonial_text"],
    },
    "coming_soon_post_2": {
        "type": "coming_soon",
        "description": "Coming soon post template with featured image",
        "variables": {
            "text": "a text in 10-12 words telling users that one of thier new product will be launch in few days",
            "cta_text": "A Good cta text in 3-4 words ",
        },
        "required": ["text", "cta_text"],
    },
    "blog_post": {
        "type": "blog",
        "description": "Blog post template with featured image",
        "variables": {
            "title": "How to be environment conscious without being weird",
            "author": "@username",
            "read_time": "4",
            "image_url": "Generate a prompt for an image of an eco-friendly scene with sustainable practices like recycling, solar panels, and greenery, in a bright, inviting style",
            "website_url": "example.com",
            "publish_date": "2025-06-22",
            "excerpt": "This is a short description of the blog post. This will be used to display the blog post in the feed.",
            
        },
        "required": [
            "title",
            "author",
            "read_time",
            "image_url",
            "website_url",
        ],
    },
    "blog_post_2": {
        "type": "blog",
        "description": "Blog post template with featured image",
        "variables": {
            "title": "How to be environment conscious without being weird",
            "author": "@username",
            "read_time": "4",
            "image_url": "Generate a prompt for a vibrant image of green living practices, featuring reusable items, plants, and a modern eco-home, in a clean, aesthetic style",
            "publish_date": "2025-06-22",
            "excerpt": "This si a short description of the blog post. this is to be inserted by db and will be used to display the blog post in the feed",
            
        },
        "required": ["title", "author", "read_time", "image_url"],
    },
    "qa_template": {
        "type": "qna",
        "description": "Question and answer template",
        "variables": {
            "question": "A question in under 3-4 words",
            "answer": "One wind turbine can produce enough electricity to power around 1,500 homes annually!",
            "username": "@username",
            
        },
        "required": ["question", "answer", "username"],
    },
    "qa_template_2": {
        "type": "qna",
        "description": "Question and answer template",
        "variables": {
            "question": "a question in under 3-4 words",
            "answer": "a 30-40 words answer for the above question",
            "username": "@username",
            
        },
        "required": ["question", "answer", "username"],
    },
    "quote_template": {
        "type": "quote",
        "description": "Inspirational quote template",
        "variables": {
            "quote": "a quote for the wbesite in around 14-18 words",
        },
        "required": ["quote"],
    },
    "quote_template_2": {
        "type": "quote",
        "description": "Inspirational quote template",
        "variables": {
            "quote1": "genereate a phrase in about 35-40 words about this business/problem its solving or the industry it operates in",
            "username": "@stevejobs",
            
        },
        "required": ["quote1", "quote2", "username"],
    },
    "education_info": {
        "type": "education",
        "description": "Educational information template",
        "variables": {
            "product_info": "Write a brief text in under 600 chars which is a fact related to company or domain they operate in",
            "product_name": "Product Name",
            "author": "@username",
            "read_time": "4",
            "image_url": "Generate a prompt for an image of a wind turbine in a scenic landscape with clear skies and rolling hills, in a realistic style",
            
        },
        "required": ["testimonial_text", "author", "read_time", "image_url"],
    },
    "education_info_2": {
        "type": "education",
        "description": "Educational information template",
        "variables": {
            "product_info": "a faq regarding the product or company or the domain they operate in, in under 300 chars",
            "author": "@username",
            "read_time": "4",
            "image_url": "Generate a prompt for an image of a clean energy scene with multiple wind turbines in a modern, eco-friendly landscape",
            
        },
        "required": ["testimonial_text", "author", "read_time", "image_url"],
    },
    "product_promotion": {
        "type": "promotional",
        "description": "Product promotion template",
        "variables": {
            "image_url": "Generate a prompt for a visually appealing portrait image of the product. The image should be in a clean, modern style and in portrait format",
            "heading": "a simple 2-3 word heading related to the product",
            "subheading": "a simple 30-40 word subheading related to the product",
            "cta_text": "a simple 1-2 word CTA text related to the product",
            
            "website_url": "a simple 1-2 word website url related to the product",
        },
        "required": [
            "image_url",
            "heading",
            "subheading",
            "logo_url",
            "cta_text",
            "website_url",
        ],
    },
    "product_promotion_2": {
        "type": "promotional",
        "description": "Product promotion template",
        "variables": {
            "image_url": "Generate a prompt for a visually appealing image of a kanban board interface with colorful task cards and a modern, user-friendly layout",
            "quote1": "the first line of quote in 3-4 words to be shown in white color",
            "quote2": "the continued quote to be shown in next line for few words",
            
        },
        "required": ["image_url", "quote1", "quote2"],
    },
    "product_showcase": {
        "type": "product",
        "description": "Product showcase template",
        "variables": {
            "product_image": "Generate a prompt for a high-quality image for this product based on context you have",
            "product_name": "Product Name",
            "product_price": "a price for this product in INR",
            "product_description": "crisp and brief product description in under 100 chars ",
            "badge_text": "Bestseller",
            
        },
        "required": ["product_image", "product_name", "product_price"],
    },
    "product_showcase_2": {
        "type": "product",
        "description": "Product showcase template",
        "variables": {
            "product_image": "Generate a prompt for a high-quality image for this product based on context you have",
            "product_name": "Product Name",
            "product_price": "a price for this product in INR",
            "product_description": "Detailed product description in aroudn 18-21 words",
            "badge_text": "Bestseller, Dont change it keep it bestseller always",
            
        },
        "required": ["product_image", "product_name", "product_price"],
    },
    "coming_soon_page": {
        "type": "coming_soon",
        "description": "Coming soon page template",
        "variables": {
            "header_text": "a 2-3 word text for the coming soon page which would be placed above the coming soon text in the coming soon post for social media",
            "contact_email": "contact email "
        },
        "required": ["website_url", "contact_details"],
    },
    "product_showcase_3": {
        "type": "product",
        "description": "Product showcase template",
        "variables": {
            "product_image": "Generate a prompt for  product image which has transparent background as a png image. Make sure just the product is visible and the background is transparent. Also dont keep any text in the image. Make sure it has transparent background makes sure it has transparent background (alpha PNG) and also has isolated object cut-out Isolated object cut-out on a completely transparent background (alpha PNG). No floor, no shadows, no reflections, no props, no text—only the product, perfectly lit",
            "product_name": "Product Name in under 2-3 words",
            "product_price": "$99.99",
            "product_description": "Detailed product description in 6-7 words",
            "cta_text": "book now / get started or somethign similar in 2 words ",
        },
        "required": ["product_image", "product_name", "product_price"],
    },
    "cafe_post": {
        "type": "social",
        "description": "Cafe social media post template",
        "variables": {
            "business_name": "The name of the busienss",
            "product_tagline": "a prompting business tagline in under 4-5 words telling more about the business",
            "social_handle": "@dolze_ai",
        },
        "required": ["image_url", "heading", "subheading"]
    },
    "coming_soon": {
        "type": "coming_soon",
        "description": "Coming soon announcement template",
        "variables": {
            "background_image_url": "Generate a prompt for 1080 * 1080 backgroung image related to product/ service which can be used as a background image ",
            "business_name": "business name",
            "text": "Notify Me or something similar in 2-3 words",
            "website_url": "website_url"
        },
        "required": ["heading", "subheading"]
    },
    "event_day": {
        "type": "event",
        "description": "Event day announcement template",
        "variables": {
            "celebration_name": "Event Name in 2-3 words",
            "celebration_text": "Special Day in 2-3 words",
            "celebration_description": "Join us for a special celebration or something similar in 8-10 words",
            "theme_color": "#FF5733",
        },
        "required": ["celebration_name", "celebration_text", "celebration_description"]
    },
    "hiring_post": {
        "type": "careers",
        "description": "Job opening announcement template",
        "variables": {
            "heading": "We're Hiring! or somethign similar in under 2-3 words",
            "subheading": "Join our amazing team. We're looking for talented individuals.",
            "theme_color": "#7d00eb",
            "cta_text":"cta text in under 1-2 words",
            "job_title":"in under 2-3 words",
            "company_name":"name of company"
        },
        "required": ["heading", "subheading"]
    },
    "product_sale": {
        "type": "promotional",
        "description": "Product sale announcement template",
        "variables": {
            "cta_text":"cta text in 1-2 words",
            "sale_end_text":"date at which sale ends",
            "product_name": "Product Name",
            "product_description": "Amazing product that solves your problems in under 4-5 words",
            "sale_heading": "flat 50% OFF in under 2-3 words",
            "sale_text": "Limited Time Offer or similar in under 3-4 words",
            "background_image_url": "Generate a prompt for an attractive product image on a clean background",
            "theme_color": "#4A90E2",
            "product_image":"a prompt for image of the product with transparent background just the product",
        },
        "required": ["product_name", "product_description", "sale_heading"]
    },
    "product_service_minimal": {
        "type": "product",
        "description": "Minimal product/service showcase template",
        "variables": {
            "text": "Product/Service description in 8-10 words",
            "website_url": "example.com",
            "product_image": "Generate a prompt for a clean, minimal product image",
            "theme_color": "#FF5733",
            
        },
        "required": ["text", "website_url", "product_image"]
    },
    "product_showcase_4": {
        "type": "product",
        "description": "Product showcase template with offer",
        "variables": {
            "product_image": "Generate a prompt for a professional product image which has transparent background as a png image. Make sure just the product is visible and the background is transparent. Also dont keep any text in the image. Make sure it has transparent background makes sure it has transparent background (alpha PNG) and also has isolated object cut-out Isolated object cut-out on a completely transparent background (alpha PNG). No floor, no shadows, no reflections, no props, no text—only the product, perfectly lit",
            "offer_text": "Special Offer\n50% OFF or something similar strictly in under 2-3 words",
            "website_url": "example.com/shop",
            "theme_color": "#4A90E2",
        },
        "required": ["product_image", "offer_text", "website_url"]
    },
    "summer_sale_promotion": {
        "type": "promotional",
        "description": "Seasonal summer sale promotion template",
        "variables": {
            "background_image_url": "Generate a prompt to generate an image for a vibrant summer-themed background related to the product",
            "brand_name": "YOUR BRAND name",
            "sale_heading": "SUMMER SALE or similar",
            "sale_description": "A biref intro to the sale in under 7-8 words",
            "theme_color": "#FF6B6B",
            "discount_text": "upto 50% off or similar in under 3-4 words",
            "social_handle":"@dolze_ai",
            "contact_number": "random contact number"
        },
        "required": ["background_image_url", "brand_name", "sale_heading"]
    },
    "testimonials_template_2": {
        "type": "testimonial",
        "description": "Elegant testimonial card with gradient background and star rating",
        "variables": {
            "testimonial_text": "Share what customers are saying about your product/service (2-3 sentences)",
            "user_avatar": "URL to customer's profile picture mostly use some working stock images",
            "user_name": "Customer Name",
            "user_title": "Customer Title/Company",
            "website_url": "dolze.ai/download",
            "theme_color": "#4A90E2",
        },
        "required": ["testimonial_text", "user_avatar", "customer_name"]
    },
    "product_showcase_5":{
                "type": "product_showcase",
        "description": "Elegant testimonial card with gradient background and star rating",
        "variables": {
            "heading":"a heading like 'Healthy living happy living' in strictly under 4 words",
            "subheading":"a description in under 40 words",
            "cta_text":"Book Now",
            "contact_number": "+09876543211",
            "website_url": "dolze.ai",
            "product_image":"Generate a prompt for  product image which has transparent background as a png image. Make sure just the product is visible and the background is transparent. Also dont keep any text in the image. Make sure it has transparent background makes sure it has transparent background (alpha PNG) and also has isolated object cut-out Isolated object cut-out on a completely transparent background (alpha PNG). No floor, no shadows, no reflections, no props, no text—only the product, perfectly lit",
        },
    },
    "brand_info":{
        "type": "brand_info",
        "description": "Elegant testimonial card with gradient background and star rating",
        "variables":  {
            "product_image":"generate a prompt for a sqwuare image for background image of the post for a post showing things about comanpy culture and bonding",
            "heading":"a heading for the post in under 4-5 words",
            "subheading": "a subheading for the psot in under 20-25 words",
            "cta_text":"a cta for the text in 2-4 words",
        }
    },
    "product_marketing":{
         "type": "product_marketing",
        "description": "Elegant testimonial card with gradient background and star rating",
        "variables":  {
            "social_handle": "@dolze.ai",
            "heading":"Improve your business marketing or something similar in under 26-27 characters",
            "description":"a description matching the above headign in under 200 chars",
            "background_image_url": "a prompt for a bg image for the above idea. it should be a portrait image with aspect ratio of 1920 by 1080",
        }
    },
    "brand_info_2":{
      "type": "brand_info_2",
        "description": "Elegant testimonial card with gradient background and star rating",
        "variables":  {
            "service_hook":"A hook similar to 'do you need a brand new' or somethign similar in under 5-6 words, dont add the product name to any of them it will be added in the product_name field",
            "service_name":"The service name eg: 'website ?'. maek sure to add soemthing that completes the sentence in service_hook . keep it strictly under 12 characters",
            "content":"our team of expert devlopers will make sure you will get the best website available in the market",
            "contact_number": "+123-456-7890",
            "website_url":"www.dolze.ai/careers",
            "product_image": "a prompt for a produce image for the above idea. it should be a portrait image with aspect ratio of 1920 by 1080",
            "contact_email": "contact@dolze.ai"        
        }
    },
    "product_sale_2":{
        "type": "product_sale_2",
        "description": "Elegant testimonial card with gradient background and star rating",
        "variables":  {
            "product_image":"https://images.pexels.com/photos/1181677/pexels-photo-1181677.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
            "heading":"Digital planner or something similar in under 17 characters",
            "usp1": "Undated Planner or something similar in under 16 characters",
            "usp2": "Hyperlinked Pages or something similar in under 16 characters",
            "cta_text":"Book Now or something similar in under 10 characters",
            "product_highlights":"highlight of product in under 14 characters",
            "business_name":"name of the business"
        }
    },
    "product_feature": {
        "type": "product_feature",
        "description": "Product feature showcase with multiple feature points",
        "variables": {
            "product_image": "generate a prompt for a product image for the above idea. it should be a portrait image with aspect ratio of 1920 by 1080",
            "feature1": "Main feature 1 (e.g., 'This nasal drop is good') in under 50 chars",
            "feature2": "Main feature 2 (e.g., 'This nasal drop is really great product') in under 50 chars",
            "feature3": "Main feature 3 (e.g., 'Clears nose with ease') in under 50 chars",
            "feature4": "Additional feature (e.g., 'Long lasting effect') in under 50 chars",
            "feature_title": "Section title (e.g., 'Features') in under 10 chars",
            "product_name": "Name of the product (e.g., 'Nasal Drops') in under 10 chars"
        }
    },
    "event_alert": {
        "type": "event_alert",
        "description": "Event announcement with key details",
        "variables": {
            "company_name": "Name of the company (e.g., 'Dolze AI')",
            "event_type": "Type of event (e.g., 'FREE WEBINAR') in under 20 chars",
            "event_date": "Date of the event (e.g., 'July 16') in under 20 chars",
            "event_time": "Time of the event (e.g., '10:00 AM - 12:00 PM') in under 20 chars",
            "event_highlight": "Main highlight of the event in under 200 chars",
            "register_details": "Registration information (e.g., 'Registration Link in bio') in under 100 chars",
            "product_image": "generate a prompt for a product image for the above idea. it should be a portrait image with aspect ratio of 1920 by 1080"
        }
    },
    "sale_alert": {
        "type": "sale_alert",
        "description": "Sale announcement with promotional details",
        "variables": {
            "sale_heading": "Sale title (e.g., 'Technology Sale') in 2 words",
            "sale_description": "Sale description (e.g., 'Special Sale Only in August') in under 35 chars",
            "cta_text": "Call to action text (e.g., 'Shop Now!') in under 20 chars",
            "website_url": "Website URL (e.g., 'www.dolze.ai')",
            "sale_text": "Sale details (e.g., '30% off') in under 14 chars",
            "product_image": "generate a prompt for a product image for the above idea. it should be a portrait image with aspect ratio of 1080 by 1920",
        }
    },
    "testimonials": {
        "type": "testimonials",
        "description": "Customer testimonial with profile and quote",
        "variables": {
            "product_image": "generate a prompt for a product image for the above idea. it should be a portrait image with aspect ratio of 1920 by 1080",
            "name": "Full name of the person (e.g., 'Sagar Giri') in under 15 chars",
            "greeting": "Introduction text (e.g., 'Meet our developers') in under 20 chars",
            "designation": "Testimonial quote in quotes (e.g., 'I have had a passion...') in under 500 chars",
            "social_handle": "Social media handle (e.g., '@dolze_ai') in under 50 chars"
        }
    },
    "event_announcement": {
        "type": "event_announcement",
        "description": "Event announcement template with circular image and elegant design",
        "variables": {
            "event_image": "generate a prompt for an event-related image that will be displayed in a circular format",
            "event_name": "Name of the event (e.g., 'Sale alert') in under 10 chars",
            "event_description": "Brief description of the event in under 100 chars",
            "company_name": "Name of the company hosting the event in under 50 chars"
        },
        "required": ["event_image", "event_name", "event_description", "company_name"]
    }
}
           


def get_template_variables(template_name: str) -> Dict[str, Any]:
    """
    Get the variable structure for a specific template.

    Args:
        template_name: Name of the template to get variables for

    Returns:
        Dictionary containing variable structure and example values

    Raises:
        ValueError: If template_name is not found in the registry
    """
    if template_name not in TEMPLATE_VARIABLES_REGISTRY:
        return TEMPLATE_VARIABLES_REGISTRY["default"]["variables"]
    return TEMPLATE_VARIABLES_REGISTRY[template_name]["variables"]


def get_required_variables(template_name: str) -> list[str]:
    """
    Get the list of required variables for a template.

    Args:
        template_name: Name of the template

    Returns:
        List of required variable names
    """
    template = get_template_variables(template_name)
    return template.get("required", [])


def get_available_templates() -> list[str]:
    """
    Get a list of all available template names.

    Returns:
        List of template names
    """
    return list(TEMPLATE_VARIABLES_REGISTRY.keys())
