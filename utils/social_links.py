"""
Module for managing and rendering social media links in the Streamlit application.
This module provides functionality to define, store, and display social media links
with their associated icons in a consistent and visually appealing format.
"""

# Import required libraries
import streamlit as st
from dataclasses import dataclass
from typing import List

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

def render_social_links():
    """
    Renders social links in a clean, consistent format.
    
    This function:
    1. Displays a "Let's Connect!" header
    2. Applies custom CSS to control spacing between icons and text
    3. Creates a two-column layout for each social link:
       - Left column: Social media icon
       - Right column: Clickable link text
    4. Applies negative margins to reduce spacing between elements
    """
    # Display the section header
    st.markdown("### Let's Connect!")
    
    # Add custom CSS to reduce spacing between icon and text
    st.markdown("""
        <style>
        .stImage > img {
            margin-right: -25px;  /* Increase negative margin to pull text closer */
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Iterate through social links and render each with icon and text
    for link in get_social_links():
        # Create a two-column layout for each social link
        icon_col, link_col = st.columns([1, 6])  # Create two columns with 1:6 ratio
        
        # Left column: Display the social media icon
        with icon_col:
            st.image(f"assets/images/{link.icon_path}", width=30)
        
        # Right column: Display the link with custom styling
        with link_col:
            st.markdown(
                f'<a href="{link.url}" target="_blank" style="text-decoration: none; color: #0066cc; margin-left: -20px;">{link.name}</a>',
                unsafe_allow_html=True
            )