import streamlit as st
import google.generativeai as genai

# Configure your Gemini API key
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]  # Store your API key in Streamlit secrets
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Gemini Chatbot")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response from Gemini
    try:
        response = model.generate_content(prompt)
        response_text = response.text

        st.session_state.messages.append({"role": "assistant", "content": response_text})
        with st.chat_message("assistant"):
            st.markdown(response_text)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.session_state.messages.append({"role": "assistant", "content": "Sorry, an error occured. Please try again later."})
        with st.chat_message("assistant"):
            st.markdown("Sorry, an error occured. Please try again later.")