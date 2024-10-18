import os
import uuid

import requests
import streamlit as st
from dotenv import load_dotenv
from lyzr_agent_api.client import AgentAPI
from lyzr_agent_api.models.chat import ChatRequest

st.title("NPD Chat Bot")
load_dotenv()
LYZR_API_KEY = os.getenv("LYZR_API_KEY")


# Initialize the API client
def get_client(api_key):
    return AgentAPI(x_api_key=api_key)


def generate_response(message):
    client = get_client(LYZR_API_KEY)

    session_id = st.session_state.session_id

    response = client.chat_with_agent(
        json_body=ChatRequest(
            user_id="rash@example.com",
            agent_id="67110ddfa929339fb3252dbb",
            message=message,
            session_id=session_id,
        )
    )
    return response["response"]


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = generate_response(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
