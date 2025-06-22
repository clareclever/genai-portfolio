# Description: This file contains the code for the Home page of the Streamlit app.
import streamlit as st
from utils.social_links import render_social_links

# Set page configurations
st.set_page_config(page_title="Home", layout="wide")

# Path to the local PDF file and images
PDF_FILE_PATH = "./assets/data/Resume.pdf"
HEADSHOT_PATH = "./assets/images/Headshot.png"

# --- MAIN CONTENT ---
# Create columns for layout: [left margin, main content, profile photo, right margin]
left_margin, main_content, profile_photo, right_margin = st.columns([0.5, 2.5, 2, 0.5])

# --- LEFT SECTION (Bio and Resume Download) ---
with main_content:
    # Introduction with emphasis
    st.title("Hi, I'm Clare Clever!")
    st.markdown("### **Lead Software Engineer at Leidos**")
    st.markdown(
        """
        I am passionate about leveraging :green-background[technology] to drive innovation in :green-background[AI/ML], :green-background[cybersecurity], and :green-background[automation], building :green-background[impactful] solutions and collaborating on :green-background[cutting-edge] projects.
        \n\nPlease check out my resume below or visit the Q&A tab to learn more!
        """
    )

    # Open the resume PDF in binary mode
    with open(PDF_FILE_PATH, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()

    # Display download button for the resume
    st.download_button(
        label="📄 Download Resume",
        data=pdf_bytes,
        file_name="Clare's Resume.pdf",
        mime="application/pdf"
    )

    # Button to navigate to the Q&A page
    if st.button("🗨️ Resume Q&A"):
        st.switch_page("pages/Q&A.py")

    st.divider()

    # --- CONNECT SECTION ---
    render_social_links()

# --- RIGHT SECTION (Headshot Image) ---
with profile_photo:
    st.image(HEADSHOT_PATH, width=350)  # Adjust width as needed
