import streamlit as st
from langchain_groq import ChatGroq  # Import ChatGroq from langchain_groq
from langchain_core.prompts import ChatPromptTemplate

# Load GROQ_API_KEY from Streamlit secrets
groq_api_key = st.secrets["GROQ_API_KEY"]

# Replace 'verified-model-name' with the actual name of a valid Groq model
llm = ChatGroq(groq_api_key=groq_api_key, model="Gemma2-9b-It")

# Prompt Template
generic_template = "Translate the following into {language}:"
prompt = ChatPromptTemplate.from_messages(
    [("system", generic_template), ("user", "{text}")]
)

# Streamlit UI
st.title("Language Translator with ChatGroq")

# Dropdown for selecting language
language = st.selectbox(
    "Select a language to translate into:",
    ["French", "Spanish", "German", "Chinese", "Italian", "Japanese"]
)

# Text input for user text
text_to_translate = st.text_input("Enter text to translate:")

# Translate button
if st.button("Translate"):
    if not text_to_translate.strip():
        st.error("Please enter some text to translate!")
    else:
        try:
            # Generate the formatted prompt as a list of BaseMessages
            formatted_prompt = prompt.format_messages(language=language, text=text_to_translate)
            
            # Use ChatGroq to generate a response
            response = llm.invoke(formatted_prompt)  # Pass formatted_prompt directly
            
            # Display the translation
            st.success(f"Translation in {language}:")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
