import streamlit as st
import base64

# Set page configurations
st.set_page_config(page_title="Home", layout="wide")

# Function to encode an image to Base64
def encode_image_to_base64(image_path):
    """Encodes an image file into Base64 format."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Path to the local PDF file and images
PDF_FILE_PATH = "./assets/Resume.pdf"  # Replace with your local PDF path
HEADSHOT_PATH = "./assets/Headshot.png"
LINKEDIN_ICON_PATH = "assets/LinkedIn.png"
GITHUB_ICON_PATH = "assets/GitHub.png"
EMAIL_ICON_PATH = "assets/Email.png"

# Links to LinkedIn, Email, and GitHub accounts
LINKEDIN_LINK = "https://www.linkedin.com/in/clareclever/"
EMAIL_LINK = "mailto:boinest312@gmail.com"
GITHUB_LINK = "https://github.com/ClareClever99"

# --- MAIN CONTENT ---
# Create columns for layout
col1, col2, col3, col4 = st.columns([0.5, 2.5, 2, 0.5])

# --- LEFT SECTION (Bio and Resume Download) ---
with col2:
    # Introduction with emphasis
    st.title("Hi, I'm Clare Clever!")
    st.markdown("### **Systems Engineer**")
    st.markdown(
        """
        UPDATE SUB-HEADING
        """
    )

    # Open the resume PDF in binary mode
    with open(PDF_FILE_PATH, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()

    # Display download button for the resume
    st.download_button(
        label="📄 Download Resume",  # You can replace the emoji with text or another icon
        data=pdf_bytes,
        file_name="Clare's Resume.pdf",
        mime="application/pdf"
    )

    # Button to navigate to the Q&A page
    if st.button("🗨️ Resume Q&A"):
        st.switch_page("pages/Q&A.py")

    st.divider()

# --- RIGHT SECTION (Headshot Image) ---
with col3:
    st.image(HEADSHOT_PATH, width=350)  # Adjust width as needed

# --- CONNECT SECTION (LinkedIn, Email, GitHub) ---
# Create columns for layout (again for Connect section)
col1, col2, col3, col4 = st.columns([0.5, 2.5, 2, 0.5])

with col2:
    # Encode icons to Base64 for embedding in HTML
    linkedin_icon_base64 = encode_image_to_base64(LINKEDIN_ICON_PATH)
    github_icon_base64 = encode_image_to_base64(GITHUB_ICON_PATH)
    email_icon_base64 = encode_image_to_base64(EMAIL_ICON_PATH)

    # Add links for LinkedIn, Email, and GitHub with icons
    st.markdown(
        """
        <h3>Let's Connect!</h3>
        <p style="margin-bottom: 15px;">
            <a href="{linkedin_link}" target="_blank" style="text-decoration: none;">
                <img src="data:image/png;base64,{linkedin_icon}" width="30" height="30" style="vertical-align: middle; margin-right: 8px;" />
            </a>
            <span>LinkedIn</span>
        </p>
        <p style="margin-bottom: 15px;">
            <a href="{email_link}" style="text-decoration: none;">
                <img src="data:image/png;base64,{email_icon}" width="30" height="30" style="vertical-align: middle; margin-right: 8px;" />
            </a>
            <span>Email</span>
        </p>
        <p style="margin-bottom: 15px;">
            <a href="{github_link}" target="_blank" style="text-decoration: none;">
                <img src="data:image/png;base64,{github_icon}" width="30" height="30" style="vertical-align: middle; margin-right: 8px;" />
            </a>
            <span>GitHub</span>
        </p>
        """.format(
            linkedin_link=LINKEDIN_LINK,
            linkedin_icon=linkedin_icon_base64,
            email_link=EMAIL_LINK,
            email_icon=email_icon_base64,
            github_link=GITHUB_LINK,
            github_icon=github_icon_base64,
        ),
        unsafe_allow_html=True,
    )