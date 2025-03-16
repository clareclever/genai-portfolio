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
            icon_path="assets/images/LinkedIn.png"
        ),
        SocialLink(
            name="Email",
            url=st.secrets["email"],
            icon_path="assets/images/Email.png"
        ),
        SocialLink(
            name="GitHub",
            url=st.secrets["github_url"],
            icon_path="assets/images/GitHub.png"
        ),
        SocialLink(
            name="Salesforce",
            url=st.secrets["salesforce_url"],
            icon_path="assets/images/Salesforce.png"
        )
    ]

def render_social_links():
    """Renders social links in a clean, consistent format."""
    st.markdown("### Let's Connect!")
    
    links_html = ""
    for link in get_social_links():
        links_html += f'<a href="{link.url}" target="_blank" style="text-decoration: none; margin-right: 20px;">'
        links_html += f'<img src="{link.icon_path}" style="width: 30px; vertical-align: middle; margin-right: 5px;">'
        links_html += f'<span style="color: #0066cc;">{link.name}</span></a>'
    
    st.markdown(links_html, unsafe_allow_html=True)