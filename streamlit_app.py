import streamlit as st
from openai import OpenAI

st.title("Project 🍲🦑: experiment with ChatGPT prompts for multilingual recipe generation")

def chat_with_gpt(conversation):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Adjust model as necessary
        messages=conversation
    )
    return response.choices[0].message.content

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    system_prompt_text = st.text_area('Enter system prompt')
    user_prompt_text = st.text_input('Enter user prompt')

    conversation = [{"role": "system", "content": system_prompt_text},
                    {"role": "user", "content": user_prompt_text}]

    if st.button('Send to ChatGPT'):
        st.write(chat_with_gpt(conversation))