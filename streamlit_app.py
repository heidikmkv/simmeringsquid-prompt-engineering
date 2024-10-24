import streamlit as st
from openai import OpenAI

import working_prompts
from helpers import construct_conversation, get_chatgpt_response

st.title("Project 🍲🦑: experiment with ChatGPT prompts")

# Initialize session state to hold example pairs
if 'examples' not in st.session_state:
    st.session_state.examples = []

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

    system_prompt = st.text_area('Enter system prompt',value=working_prompts.text_systemprompt_recipe)

    # Container to hold dynamically added example pairs
    example_container = st.container()

    # Function to add a new example pair
    def add_example():
        st.session_state.examples.append({"user": "", "system": ""})

    # Add a button to allow users to add examples
    if st.button("Add Example"):
        add_example()

    # Display each existing example pair for input
    for i, example in enumerate(st.session_state.examples):
        user_input = st.text_input(f"Example User Prompt", key=f"user_{i}", value=example['user'])
        system_response = st.text_area(f"Example System Response", key=f"system_{i}", value=example['system'])
        # Update the examples in session state as the user types
        st.session_state.examples[i]['user'] = user_input
        st.session_state.examples[i]['system'] = system_response

    # Input for user prompt (mandatory), after the example fields
    user_prompt = st.text_input("Final User Prompt", placeholder="Enter your question or command here...")

    # Submit button
    if st.button("Submit"):
        if system_prompt and user_prompt:
            # Construct the conversation
            conversation = construct_conversation(system_prompt, user_prompt, st.session_state.examples)
            
            # Call the chat_with_gpt function with the constructed conversation
            response = chat_with_gpt(conversation)
            
            # Display the response
            st.write("### ChatGPT Response")
            st.write(response)
        else:
            st.error("Please provide both a system prompt and a final user prompt.")