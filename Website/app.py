import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Google Gemini API
gemini_api_key = os.getenv('gemini_api_key')
genai.configure(api_key=gemini_api_key)

# Define the model with system instructions
system_instruction_question = "You are a helpful assistant that answers user questions."
model = genai.GenerativeModel('gemini-1.5-pro-latest', system_instruction=system_instruction_question)

# Initialize Streamlit app
st.title("Chatbot")

# Initialize chat history if not already initialized
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response using Gemini model
    response = model.generate_content(prompt)
    
    # Extract the assistant's content from the response
    assistant_message = response.text  # Use the 'result' attribute to get the content
    
    # Display the assistant's message in chat message container
    with st.chat_message("assistant"):
        st.markdown(assistant_message)

    # Append the assistant's message to the chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
