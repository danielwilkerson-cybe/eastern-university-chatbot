
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load Gemini API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.error("Gemini API key not found. Please check your settings.")
    st.stop()

# Connect to Gemini
client = genai.Client(api_key=api_key)

st.set_page_config(
    page_title="Eastern University Chatbot",
    page_icon="🎓"
)

st.title("🎓 Eastern University Graduate Information Assistant")

st.write(
    "Welcome! Ask me questions about Eastern University's "
    "graduate programs, admissions, tuition, and student services."
)

# Store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages[:-1]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Accept a new question
question = st.chat_input("Type your question here...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.write(question)

    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Read Eastern University information
                with open("university_info.txt", "r", encoding="utf-8") as file:
                    university_info = file.read()

                # Include previous conversation messages
                conversation_history = ""

                for message in st.session_state.messages[:-1]:
                    conversation_history += f"{message['role']}: {message['content']}\n"

                # Send university information and conversation history to Gemini
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=f"""
You are the Eastern University Information Assistant.

Use the following official university information to answer questions.

UNIVERSITY INFORMATION:
{university_info}

PREVIOUS CONVERSATION:
{conversation_history}

USER QUESTION:
{question}

Instructions:
- Answer using the university information provided.
- Consider previous messages when answering follow-up questions.
- Do not invent facts.
- If the information is not available, say so.
- Direct users to the official Eastern University website when necessary.
- Use simple and clear language.
"""
                )

                answer = response.text
                st.write(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                st.error(f"Something went wrong: {e}")

