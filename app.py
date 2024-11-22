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

# Initialize session state for chat history and input field
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# Display Chat History at the top
st.subheader("Chat History")
if st.session_state.chat_history:
    for entry in st.session_state.chat_history:
        # Display user query
        st.markdown(f"**You:** {entry['query']}")
        # Display AI response
        st.markdown(f"**Translation:** {entry['response']}")
        st.divider()  # Adds a visual separator between chat entries
else:
    st.info("Your chat history will appear here.")

# Query input and language selection at the bottom
st.divider()  # Separator for layout
language = st.selectbox(
    "Select a language to translate into:",
    ["French", "Spanish", "German", "Chinese", "Italian", "Japanese", "English", "Urdu"],
    key="language"
)

# Text input for user text
text_to_translate = st.text_input(
    "Enter text to translate:",
    value=st.session_state.input_text,  # Bind input text to session state
    key="text_to_translate"
)

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
            
            # Access the content from the AIMessage object
            translation = response.content  # Access the 'content' attribute of the AIMessage object
            
            # Save the user query and translation to chat history
            st.session_state.chat_history.append({
                "query": text_to_translate,
                "response": translation
            })
            
            # Clear the input text box
            st.session_state.input_text = ""  # Clear the input text in session state
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Clear the input box when typing a new query
st.session_state.input_text = ""
