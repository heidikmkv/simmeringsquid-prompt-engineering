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

    system_prompt = st.text_area('Enter a system prompt, which sets the overall chatbot behavior:',value=working_prompts.text_systemprompt_recipe)
    # Numeric input for the number of examples
    num_examples = st.number_input("Enter the number of examples you want to provide to ChatGPT:", min_value=0, value=len(st.session_state.examples), step=1)

    # Adjust the number of examples in the session state if necessary
    if len(st.session_state.examples) < num_examples:
        for _ in range(num_examples - len(st.session_state.examples)):
            st.session_state.examples.append({"user": "", "system": ""})
    elif len(st.session_state.examples) > num_examples:
        st.session_state.examples = st.session_state.examples[:num_examples]

    # Display each existing example pair for input
    for i, example in enumerate(st.session_state.examples):
        user_input = st.text_input(f"Example {i+1} User Prompt", key=f"user_{i}", value=example['user'])
        system_response = st.text_area(f"Example {i+1} System Response", key=f"system_{i}", value=example['system'])
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