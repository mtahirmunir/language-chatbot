import openai
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate

# Load OpenAI API Key from Streamlit secrets or environment variable
openai_api_key = st.secrets["OPENAI_API_KEY"]  # or use: openai.api_key = "your-api-key"

# Initialize OpenAI API with your key
openai.api_key = openai_api_key

# Prompt Template for Translation
generic_template = "Translate the following into {language}:"
prompt = ChatPromptTemplate.from_messages(
    [("system", generic_template), ("user", "{text}")]
)

# Streamlit UI
st.title("Language Translator with OpenAI GPT")

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
            # Generate the formatted prompt as a string
            formatted_prompt = prompt.format(language=language, text=text_to_translate)
            
            # Use OpenAI GPT model to generate a translation
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # You can use "gpt-4" if you have access
                messages=[
                    {"role": "system", "content": f"Translate the following into {language}:"},
                    {"role": "user", "content": text_to_translate}
                ]
            )
            
            # Extract the model's response
            translated_text = response['choices'][0]['message']['content']
            
            # Display the translation
            st.success(f"Translation in {language}:")
            st.write(translated_text)
        
        except Exception as e:
            st.error(f"An error occurred: {e}")
