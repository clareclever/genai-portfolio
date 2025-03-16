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
    2. Creates a two-column layout for each social link:
       - Left column (10%): Social media icon
       - Right column (90%): Clickable link text
    """
    # Display the section header
    st.markdown("### Let's Connect!")
    
    # Iterate through social links and render each with icon and text
    for link in get_social_links():
        # Create a two-column layout with 0.1:0.9 ratio
        icon_col, link_col = st.columns([0.1, 0.9])
        with icon_col:
            st.image(f"assets/images/{link.icon_path}", width=30)
        with link_col:
            st.markdown(f"[{link.name}]({link.url})")