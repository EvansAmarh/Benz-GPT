import os
import json

import streamlit as st 
import openai 

# configuring openai - api key 
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))

OPENAI_AI_KEY = config_data["OPENAI_API_KEY"]
openai.api_key = OPENAI_AI_KEY

# configuring streamlit page setings
st.set_page_config(
    page_title="Benz-GPT Chat",
    page_icon="💬",
    layout="centered"
)

# Start chat session in streamlit if does not exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
# streamlit title page
st.title("🤖 Benz-GPT ChatBot")

# chat history 
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
# User's input field
user_prompt = st.chat_input("Ask Benz-GPT...")
if user_prompt:
    # display user message
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    
    # submit message for response
    response = openai.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            *st.session_state.chat_history
        ]
    )
    
    assistant_response = response.choices[0].message.content 
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
    
    # display GPT's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)