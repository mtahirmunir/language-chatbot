import streamlit as st
from langchain_groq import ChatGroq  # Import ChatGroq from langchain_groq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser  # Import StrOutputParser

# Load GROQ_API_KEY from Streamlit secrets
groq_api_key = st.secrets["GROQ_API_KEY"]

# Initialize the ChatGroq model (replace with your actual Groq model)
llm = ChatGroq(groq_api_key=groq_api_key, model="Gemma2-9b-It")

# Prompt Template for Translation
generic_template = "Translate the following into {language}:"
prompt = ChatPromptTemplate.from_messages(
    [("system", generic_template), ("user", "{text}")]
)

# Streamlit UI
st.title("Language Translator with ChatGroq")

# Dropdown for selecting language
language = st.selectbox(
    "Select a language to translate into:",
    ["French", "Spanish", "German", "Chinese", "Italian", "Japanese", "English", "Urdu"]
)

# Initialize session state for the input box and button styling
if "text_to_translate" not in st.session_state:
    st.session_state.text_to_translate = ""
if "button_style" not in st.session_state:
    st.session_state.button_style = "gray"

# Text input for user text
text_to_translate = st.text_input(
    "Enter text to translate:", value=st.session_state.text_to_translate
)

# Apply the button style dynamically
button_style = f"border: 2px solid {st.session_state.button_style}; padding: 10px 20px;"

# Translate button
if st.button("Translate", key="translate_button", help="Click to translate the text"):
    if not text_to_translate.strip():
        st.error("Please enter some text to translate!")
    else:
        try:
            # Change the button border to red temporarily
            st.session_state.button_style = "red"
            
            # Generate the formatted prompt as a list of BaseMessages
            formatted_prompt = prompt.format_messages(language=language, text=text_to_translate)
            
            # Use ChatGroq to generate a response
            response = llm.invoke(formatted_prompt)
            
            # Access the content from the AIMessage object
            translation = response.content
            
            # Display the translation
            st.success(f"Translation in {language}:")
            st.write(translation)
            
            # Clear the text input box after translation
            st.session_state.text_to_translate = ""
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            # Reset the button border back to gray
            st.session_state.button_style = "gray"
