# Import necessary packages
import google.generativeai as genai
import streamlit as st
import random

# Configure the API key
genai.configure(api_key=st.secrets["API_KEY"])

# Set page configurations
st.set_page_config(page_title="Q&A", layout="wide")

# Import prompt config
from assets.prompt_config import build_system_prompt, get_predefined_questions

# Predefined questions for the user to choose from
PREDEFINED_QUESTIONS = get_predefined_questions()

# Model versions for both Flash and Pro variants. Check for new models here: https://aistudio.google.com/ & https://ai.google.dev/gemini-api/docs/models
GEMINI_FLASH_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash"
]
GEMINI_PRO_MODELS = [
    "gemini-2.5-pro",
    "gemini-1.5-pro"
]

# Dictionary mapping model names to user-friendly names
MODEL_DICT = {
    "Gemini Flash - tasks requiring quick responses.": "Flash",
    "Gemini Pro - tasks requiring deep analysis and extended context.": "Pro"
}

# Debug mode variable
DEBUG_MODE = False

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
            # Populate the text input when a button is clicked, removing the emoji
            if input_question is not None and ' ' in input_question:  # Check if there's a space (to split emoji and text)
                st.session_state.custom_input = input_question.split(' ', 1)[1]
            else:
                st.session_state.custom_input = input_question # Fallback if no space
            st.session_state.user_question = input_question # Keep original question with emoji for the prompt
        else:
            st.session_state.user_question = st.session_state.custom_input

        # Return early if the user question is empty
        if not st.session_state.user_question:
            return

        # Generate the prompt for the model
        prompt = build_system_prompt(st.session_state.user_question)
        
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
                    # Show the response for debugging purposes (optional)
                    if DEBUG_MODE:
                        print(f"Response from {model_name}:\n {response.text}")
                    st.session_state.response = response
                    st.session_state.recent_model = model_name.split("/")[-1]  # Store only model name
                    break
            
            # Handle exceptions and continue to the next model
            except Exception as e:
                if DEBUG_MODE:
                    print(f"Error with model {model_name}:\n {e}")
        
        # Display a warning if no response is available
        if not st.session_state.response:
            st.warning("Sorry, but it seems we've reached the chat limit for all models. Please try again later.")

    # Display three randomized questions as buttons in columns (centered)
    col_q1, col_q2, col_q3 = st.columns(3)
    
    # Display the buttons for the predefined questions
    for i, col in enumerate([col_q1, col_q2, col_q3]):
        question_text = st.session_state.button_questions[i]
        col.button(question_text, on_click=send_prompt, args=(question_text, "button"), key=f"q{i+1}_button")

    # Text input for custom questions (centered)
    custom_input = st.text_input("Type your question here:", key="custom_input", on_change=send_prompt, args=(None, "custom"))

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