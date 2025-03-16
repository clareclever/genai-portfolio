import streamlit as st
from dataclasses import dataclass
from typing import List

@dataclass
class SocialLink:
    name: str
    url: str
    icon_path: str

def get_social_links() -> List[SocialLink]:
    """Returns a list of social links with their configurations."""
    return [
        SocialLink(
            name="LinkedIn",
            url=st.secrets["linkedin_url"],
            icon_path="LinkedIn.png"
        ),
        SocialLink(
            name="Email",
            url=st.secrets["email"],
            icon_path="Email.png"
        ),
        SocialLink(
            name="GitHub",
            url=st.secrets["github_url"],
            icon_path="GitHub.png"
        ),
        SocialLink(
            name="Salesforce",
            url=st.secrets["salesforce_url"],
            icon_path="Salesforce.png"
        )
    ]

def render_social_links():
    """Renders social links in a clean, consistent format."""
    st.markdown("### Let's Connect!")
    
    # Add custom CSS to reduce spacing
    st.markdown("""
        <style>
        .social-link-row {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 5px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    for link in get_social_links():
        # Use custom HTML/CSS for better control of spacing
        st.markdown(f"""
            <div class="social-link-row">
                <img src="assets/images/{link.icon_path}" style="width: 30px;">
                <a href="{link.url}" target="_blank" style="text-decoration: none; color: #0066cc;">{link.name}</a>
            </div>
        """, unsafe_allow_html=True)