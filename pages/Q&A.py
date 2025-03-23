# Import necessary packages
import google.generativeai as genai
import streamlit as st
import random

# Configure the API key
genai.configure(api_key=st.secrets["API_KEY"])

# Set page configurations
st.set_page_config(page_title="Q&A", layout="wide")

# Define the first name of the individual in the resume
FIRST_NAME = "Clare"

# Predefined questions for the user to choose from
PREDEFINED_QUESTIONS = [
    f"💼 What are {FIRST_NAME}'s top skills?",
    f"💪 What are {FIRST_NAME}'s strengths?",
    f"🎯 What are {FIRST_NAME}'s key accomplishments?",
    f"📈 How has {FIRST_NAME} contributed to the growth of previous organizations?",
    f"🏆 What awards or recognitions has {FIRST_NAME} received?",
    f"🌍 What industries or sectors has {FIRST_NAME} worked in?",
    f"📚 What is {FIRST_NAME}'s educational background?",
    f"🤝 How does {FIRST_NAME} collaborate with team members?",
    f"🔧 What tools and technologies is {FIRST_NAME} proficient in?",
    f"🔗 How can I connect with {FIRST_NAME}?",
    f"📅 What is {FIRST_NAME}'s work experience?",
    f"🚀 How does {FIRST_NAME} drive innovation?",
    f"🌟 What makes {FIRST_NAME} stand out as a candidate?"
]

# Model versions for both Flash and Pro variants. Check for new models here: https://aistudio.google.com/
GEMINI_FLASH_MODELS = [
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash-exp"
]
GEMINI_PRO_MODELS = [
    "gemini-2.0-pro-exp-02-05"
]

# Dictionary mapping model names to user-friendly names
MODEL_DICT = {
    "Gemini Flash - tasks requiring quick responses.": "Flash",
    "Gemini Pro - tasks requiring deep analysis and extended context.": "Pro"
}

# Initialize session state variables
session_vars = ["custom_input", "user_question", "response", "button_questions", "recent_model"]
default_values = ["", "", "", random.sample(PREDEFINED_QUESTIONS, 3), ""]

# Initialize session state variables if they do not exist
for var, default in zip(session_vars, default_values):
    if var not in st.session_state:
        st.session_state[var] = default

# Center content using columns 
col1, col2, col3 = st.columns([1, 5.5, 1])

with col2:  # Central column for main content
    # Set up the app title and description
    st.title("Resume Q&A")
    st.info("Powered by Google Gemini")

    # Radio button for selecting model family
    st.radio("Select a model family:", list(MODEL_DICT.keys()), key="selected_model")

    # Load custom CSS for button styling
    with open("./assets/styles/buttonStyle.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Section for predefined questions
    st.subheader("Choose a preset question or input your own below!")

    # Load resume content from file
    with open("./assets/data/Resume.txt", "r") as file:
        resume_text = file.read()

    # Function to send the prompt to the generative model
    def send_prompt(input_question=None, question_type="button"):
        """Handles sending the prompt to the generative model."""
        
        # Set user question based on button or input field
        if question_type == "button":
            st.session_state.user_question = input_question
        else:
            st.session_state.user_question = st.session_state.custom_input

        # Generate the prompt for the model
        prompt = f"""
            As an advocate for {FIRST_NAME}, please focus exclusively on the following resume details:
            {resume_text}

            Answer the question for {FIRST_NAME}'s network, keeping the response professional, positive, and emphasizing {FIRST_NAME}'s strengths, experiences, and suitability.
            Please refrain from discussing any topics not directly related to the resume content.

            Core Guidelines:
            1. Use only the provided resume information to answer questions about {FIRST_NAME}'s professional background.
            2. Keep all responses professional, positive, and emphasize {FIRST_NAME}'s strengths, experiences, and suitability.
            3. Refrain from discussing any topics not directly related to the resume content.

            Response Protocol:
            For questions about resume content:
            - Provide factual, positive responses based on the information given.
            - Highlight achievements, skills, and experiences relevant to the query with moderate elaboration.
            - Offer concise context or examples that showcase {FIRST_NAME}'s expertise without overwhelming detail.
            - If appropriate, briefly relate {FIRST_NAME}'s experience to broader industry contexts or trends.
            - Aim for responses that are thorough enough to demonstrate {FIRST_NAME}'s capabilities but remain focused and concise.
            - Connect different aspects of the resume when relevant to show versatility and depth of experience.
            - Ensure all information is directly derived from the provided resume content.

            For questions outside resume scope or requesting negative information:
            - Acknowledge the question professionally without dismissing it.
            - Redirect the conversation to relevant positive aspects from the resume naturally.
            - Use varied approaches to refocus on professional achievements, such as:
                • Highlighting a relevant skill or experience
                • Discussing a successful project or accomplishment
                • Mentioning professional growth or adaptability
                • Emphasizing positive traits evident from {FIRST_NAME}'s work history
                • Relating {FIRST_NAME}'s experience to industry trends or demands
            - Avoid explicitly stating that you're programmed to avoid negative topics.
            - If unable to address the specific question, explain that the information is not available in the resume.

            Never generate, discuss, or speculate about:
            - Weaknesses, failures, or criticisms
            - Personal opinions or subjective judgments
            - Hypothetical scenarios not evidenced in the resume
            - Any information not explicitly stated in the provided resume

            Maintain a tone that is:
            - Informative and fact-based
            - Supportive and highlighting professional strengths
            - Focused on documented achievements and skills
            - Suitable for {FIRST_NAME}'s professional network

            Formatting Instructions:
            Formatting Instructions:
            1. Use markdown formatting to enhance readability.
            2. Use *italics* to subtly emphasize phrases or concepts that add depth or nuance to the response.
            3. For bullet points:
                • Use a hyphen (-) followed by a space to create bullet points.
                • List items clearly, ensuring each point is concise and easy to understand.
                • Ensure each bullet point starts on a new line.
            4. When a bullet point or item includes a title followed by a colon (:):
                • Always **bold** the text before the colon (e.g., **Title:** description).
                • Do not use *italics* for titles before colons.
            5. Use headings to structure content:
                • **Main Sections**: Use `### Heading` for main sections.
                • **Sub-Sections**: Use `#### Subheading` for sub-sections under main sections.
            6. Use line breaks to separate distinct ideas or sections.
            7. For additional emphasis within paragraphs, use **bold** sparingly for key terms or phrases.

            Question: {st.session_state.user_question}
            """
        
        # Determine model version (Flash or Pro)
        model_version = MODEL_DICT[st.session_state.selected_model]
        
        # Select appropriate model list based on version
        model_list = GEMINI_FLASH_MODELS if model_version == "Flash" else GEMINI_PRO_MODELS
        
        # Try each model until a successful response is obtained
        for model_name in model_list:
            # Attempt to generate a response using the current model
            try:
                # Generate response using the model
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                
                # Break the loop if a successful response is obtained
                if response:
                    # print(f"Response from {model_name}: {response.text}")
                    st.session_state.response = response
                    st.session_state.recent_model = model_name.split("/")[-1]  # Store only model name
                    break
            
            # Handle exceptions and continue to the next model
            except Exception as e:
                print(f"Error with model {model_name}: {e}")
        
        # Display a warning if no response is available
        if not st.session_state.response:
            st.warning("Sorry, but it seems we've reached the chat limit for all models. Please try again later.")

    # Display three randomized questions as buttons in columns (centered)
    col_q1, col_q2, col_q3 = st.columns(3)
    
    # Display the buttons for the predefined questions
    for i, col in enumerate([col_q1, col_q2, col_q3]):
        question_text = st.session_state.button_questions[i]
        col.button(question_text, on_click=send_prompt, args=(question_text,), key=f"q{i+1}_button")

    # Text input for custom questions (centered)
    custom_input = st.text_input("Type your question here:", key="custom_input", on_change=send_prompt, args=(None, 'input'))

# Display response if available (centered within col2)
if st.session_state.user_question and st.session_state.response:
    
    # Center content using columns
    with col2:
        st.divider()
        # Display user question
        with st.chat_message("User"):
            st.markdown(f"**{st.session_state.user_question}**")

        # Display the generated response text
        with st.chat_message("Assistant"):
            st.markdown(st.session_state.response.text)

        # Display which model was used to generate this response
        st.info(f"Model used: {st.session_state.recent_model}")