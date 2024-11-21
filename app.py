import os
import streamlit as st
from langchain_groq import GroqModel  # Import Groq integration for LangChain
from langchain_core.prompts import ChatPromptTemplate

# Load GROQ_API_KEY from Streamlit secrets
groq_api_key = st.secrets["GROQ_API_KEY"]

# Initialize the Groq Model
llm = GroqModel(api_key=groq_api_key, model="groq-translate")  # Replace 'groq-translate' with the actual model name

# Prompt Template
generic_template = "Translate the following into {language}:"
prompt = ChatPromptTemplate.from_messages(
    [("system", generic_template), ("user", "{text}")]
)

# Streamlit UI
st.title("Language Translator with Groq")

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
            # Generate the prompt dynamically
            generated_prompt = prompt.invoke({"language": language, "text": text_to_translate})
            
            # Use Groq model to generate a response
            response = llm.predict(generated_prompt)
            
            # Display the translation
            st.success(f"Translation in {language}:")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
