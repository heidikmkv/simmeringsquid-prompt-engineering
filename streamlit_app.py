import streamlit as st
from openai import OpenAI
import working_prompts
from helpers import *


st.title("Project 🍲🦑: experiment with ChatGPT prompts")

openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Input for system prompt
    system_prompt = st.text_area("System Prompt", value="You are a helpful assistant.")
    user_prompt = st.text_area("User Prompt", placeholder="Enter your question or command here...")

    # Container to hold dynamically added example pairs
    example_container = st.container()
    examples = []

    # Define function to add a new example pair (user-system)
    def add_example():
        with example_container:
            user_input = st.text_input(f"Example User Prompt", key=f"user_{len(examples)}")
            system_response = st.text_input(f"Example System Response", key=f"system_{len(examples)}")
            if user_input and system_response:
                examples.append({"user": user_input, "system": system_response})

    # Add a button to allow users to add examples
    if st.button("Add Example"):
        add_example()

    # Display each existing example as input fields
    for i, example in enumerate(examples):
        st.text_input(f"Example {i+1} User", value=example['user'], key=f"example_user_{i}")
        st.text_input(f"Example {i+1} System", value=example['system'], key=f"example_system_{i}")

    # Submit button
    if st.button("Submit"):
        if system_prompt and user_prompt:
            # Get the response from ChatGPT
            response = get_chatgpt_response(system_prompt, user_prompt, examples,client)
            # Display the response
            st.write("### ChatGPT Response")
            st.write(response)
        else:
            st.error("Please provide both a system prompt and a user prompt.")