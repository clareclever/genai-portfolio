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
    
    # Create all columns at once - two columns per link (icon and text)
    links = get_social_links()
    cols = st.columns(len(links) * 2)
    
    # Fill the columns with content
    for idx, link in enumerate(links):
        icon_col = cols[idx * 2]
        link_col = cols[idx * 2 + 1]
        
        with icon_col:
            st.image(link.icon_path, width=30)
        with link_col:
            st.markdown(f"[{link.name}]({link.url})") 