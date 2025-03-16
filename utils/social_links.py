import streamlit as st
from dataclasses import dataclass
from typing import List

@dataclass
class SocialLink:
    name: str
    url: str
    icon_path: str

@st.cache_data
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
    
    for link in get_social_links():
        icon_col, link_col = st.columns([0.1, 0.9])
        with icon_col:
            st.image(link.icon_path, width=30)
        with link_col:
            st.markdown(f"[{link.name}]({link.url})") 