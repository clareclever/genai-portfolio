# Import necessary packages
import google.generativeai as genai
import streamlit as st
import random

# Configure the API key
genai.configure(api_key=st.secrets["API_KEY"])

# Set page configurations
st.set_page_config(page_title="Q&A", layout="wide")

# Predefined questions for the user to select from
FIRST_NAME = "Clare"
PREDEFINED_QUESTIONS = [
    # f"💼 What are {FIRST_NAME}'s top skills?",
    # f"💪 What are {FIRST_NAME}'s strengths?",
    # f"🎯 What are {FIRST_NAME}'s key accomplishments?",
    # f"📈 How has {FIRST_NAME} contributed to the growth of previous organizations?",
    # f"🏆 What awards or recognitions has {FIRST_NAME} received?",
    # f"🌍 What industries or sectors has {FIRST_NAME} worked in?",
    # f"📚 What is {FIRST_NAME}'s educational background?",
    f"🤝 How does {FIRST_NAME} collaborate with team members?",
    f"🔧 What tools and technologies is {FIRST_NAME} proficient in?",
    f"🔗 How can I connect with {FIRST_NAME}?"
]

# Model versions for both Flash and Pro variants
# Check for new models at https://aistudio.google.com/
GEMINI_FLASH_MODELS = [
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash-exp"
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b"

    # Old 1.5 Flash models
        # "gemini-1.5-flash-exp-0827", 
        # "gemini-1.5-flash-002", 
        # "gemini-1.5-flash-8b-exp-0924"
]
GEMINI_PRO_MODELS = [
    "gemini-2.0-pro-exp-02-05",
    "gemini-1.5-pro"

    # Old 1.5 Pro models
        # "gemini-1.5-pro-exp-0827",
        # "gemini-1.5-pro-002",
]

MODEL_DICT = {
    "Gemini Flash - tasks requiring quick responses.": "Flash",
    "Gemini Pro - tasks requiring deep analysis and extended context.": "Pro"
}

# Initialize session state variables
if "custom_input" not in st.session_state:
    st.session_state.custom_input = ""
if "user_question" not in st.session_state:
    st.session_state.user_question = ""
if "response" not in st.session_state:
    st.session_state.response = ""
if "button_questions" not in st.session_state:
    st.session_state.button_questions = random.sample(PREDEFINED_QUESTIONS, 3)
if "recent_model" not in st.session_state:
    st.session_state.recent_model = ""

# Center content using columns 
col1, col2, col3 = st.columns([1, 5.5, 1])

with col2:  # Central column for main content
    # Set up the app title and description
    st.title("Resume Q&A")
    st.info("Powered by Google Gemini")

    # Radio button for selecting model family
    st.radio("Select a model family:", list(MODEL_DICT.keys()), key="selected_model")

    # Custom CSS for button styling
    st.markdown(
        """
        <style>
            div.stButton > button:first-child {
                font-size: 1em;
                padding: 1em;
                border-radius: 8px;
                text-align: left;
                display: block;
                width: 95%;
                margin: 10px 0;
                cursor: pointer;
                transition-duration: 0.3s;
                height: auto;
                min-height: 110px;
            }
            div.stButton > button:first-child:hover {
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Section for predefined questions
    st.subheader("Choose a preset question or input your own below!")

    # Load resume content from file
    with open("./assets/Resume.txt", "r") as file:
        resume_text = file.read()

    def send_prompt(input_question=None, question_type="button"):
        """Handles sending the prompt to the generative model."""
        
        # Set user question based on button or input field
        if question_type == "button":
            st.session_state.user_question = input_question
        else:
            st.session_state.user_question = st.session_state.custom_input

        prompt = f"""
            As an advocate for the professional, please focus exclusively on the following resume details:
            {resume_text}

            Answer the question for the individual's network, keeping the response professional, positive, and emphasizing the candidate's strengths, experiences, and suitability.

            Please refrain from discussing any topics not directly related to the resume content.

            Question: {st.session_state.user_question}
            """

        # Determine model version (Flash or Pro)
        model_version = MODEL_DICT[st.session_state.selected_model]
        
        # Select appropriate model list based on version
        model_list = GEMINI_FLASH_MODELS if model_version == "Flash" else GEMINI_PRO_MODELS
        
        # Try each model until a successful response is obtained
        for model_name in model_list:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                
                if response:
                    st.session_state.response = response
                    st.session_state.recent_model = model_name.split("/")[-1]  # Store only model name
                    break

            except Exception as e:
                print(f"Error with model {model_name}: {e}")
        
        if not st.session_state.response:
            st.warning("Sorry, but it seems we've reached the chat limit for all models. Please try again later.")

    # Display three randomized questions as buttons in columns (centered)
    col_q1, col_q2, col_q3 = st.columns(3)
    
    for i, col in enumerate([col_q1, col_q2, col_q3]):
        question_text = st.session_state.button_questions[i]
        col.button(question_text, on_click=send_prompt, args=(question_text,), key=f"q{i+1}_button")

    # Text input for custom questions (centered)
    custom_input = st.text_input("Type your question here:", key="custom_input", on_change=send_prompt, args=(None, 'input'))

# Display response if available (centered within col2)
if st.session_state.user_question and st.session_state.response:
    
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