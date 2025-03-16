"""
Module for managing and rendering social media links in the Streamlit application.
This module provides functionality to define, store, and display social media links
with their associated icons in a consistent and visually appealing format.
"""

# Import required libraries
import streamlit as st
from dataclasses import dataclass
from typing import List
import os
from PIL import Image

# Define the data structure for social media links
@dataclass
class SocialLink:
    """
    Data class representing a social media link with its associated metadata.
    
    Attributes:
        name (str): Display name of the social platform
        url (str): URL to the social profile or contact method
        icon_path (str): Path to the icon image file relative to assets/images/
    """
    name: str
    url: str
    icon_path: str

# Function to get social links
def get_social_links() -> List[SocialLink]:
    """
    Returns a list of social links with their configurations.
    
    The function uses Streamlit secrets to store sensitive URLs securely.
    Each social link is configured with a name, URL (from secrets), and
    corresponding icon path.
    
    Returns:
        List[SocialLink]: List of configured social media links
    """
    # Define all social media links with their respective configurations
    return [
        # Professional network profile
        SocialLink(
            name="LinkedIn",
            url=st.secrets["linkedin_url"],
            icon_path="LinkedIn.png"
        ),
        # Contact email link
        SocialLink(
            name="Email",
            url=st.secrets["email"],
            icon_path="Email.png"
        ),
        # Code repository profile
        SocialLink(
            name="GitHub",
            url=st.secrets["github_url"],
            icon_path="GitHub.png"
        ),
        # Professional platform profile
        SocialLink(
            name="Salesforce",
            url=st.secrets["salesforce_url"],
            icon_path="Salesforce.png"
        )
    ]

# Function to render social links
def render_social_links():
    """
    Renders social links in a clean, consistent format.
    
    This function:
    1. Displays a "Let's Connect!" header
    2. Applies custom CSS to control spacing between icons and text
    3. Creates a two-column layout for each social link:
       - Left column: Social media icon (clickable)
       - Right column: Clickable link text
    4. Applies negative margins to reduce spacing between elements
    """
    # Get the absolute path to the assets directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(os.path.dirname(current_dir), "assets", "images")
    
    # Display the section header
    st.markdown("### Let's Connect!")
    
    # Add custom CSS for styling
    st.markdown("""
        <style>
        div.row-widget.stHorizontal {
            align-items: center;
        }
        .text-link {
            text-decoration: none !important;
            color: #0066cc;
            margin-left: -20px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Iterate through social links and render each with icon and text
    for link in get_social_links():
        icon_column, text_column = st.columns([1, 6])
        
        # Display icon in first column
        with icon_column:
            # Load and display the image
            image_path = os.path.join(assets_dir, link.icon_path)
            if os.path.exists(image_path):
                image = Image.open(image_path)
                st.image(image, width=30)
                st.link_button("", link.url, use_container_width=True)
            else:
                st.write(f"Image not found: {link.icon_path}")
        
        # Display text in second column
        with text_column:
            st.markdown(
                f'<a href="{link.url}" target="_blank" class="text-link">{link.name}</a>',
                unsafe_allow_html=True
            )