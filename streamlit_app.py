import streamlit as st
from openai import OpenAI

import working_prompts
from helpers import construct_conversation, get_chatgpt_response

st.title("Project 🍲🦑: experiment with ChatGPT prompts")

# Initialize session state to hold example pairs
if 'examples' not in st.session_state:
    st.session_state.examples = []

# Initialize session state to hold the original and remixed recipe
if 'original_recipe' not in st.session_state:
    st.session_state.original_recipe = None

if 'remixed_recipe' not in st.session_state:
    st.session_state.remixed_recipe = None


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
    num_examples = st.number_input("Enter the number of examples", min_value=0, value=len(st.session_state.examples), step=1)

    # Adjust the number of examples in the session state if necessary
    if len(st.session_state.examples) < num_examples:
        for _ in range(num_examples - len(st.session_state.examples)):
            st.session_state.examples.append({"user": "", "system": ""})
    elif len(st.session_state.examples) > num_examples:
        st.session_state.examples = st.session_state.examples[:num_examples]

    # Display each existing example pair for input
    for i, example in enumerate(st.session_state.examples):
        user_input = st.text_input(f"Example {i+1} User Prompt", key=f"user_{i}", value=example['user'])
        system_response = st.text_input(f"Example {i+1} System Response", key=f"system_{i}", value=example['system'])
        # Update the examples in session state as the user types
        st.session_state.examples[i]['user'] = user_input
        st.session_state.examples[i]['system'] = system_response

    # Input for user prompt (mandatory), after the example fields
    user_prompt = st.text_input("Final User Prompt", placeholder="Enter your question or command here...")

    # Submit button for original recipe generation
    if st.button("Submit"):
        if system_prompt and user_prompt:
            # Construct the conversation
            conversation = construct_conversation(system_prompt, user_prompt, st.session_state.examples)
            
            # Call the chat_with_gpt function with the constructed conversation to get the recipe
            st.session_state.original_recipe = get_chatgpt_response(client,conversation)
            st.session_state.remixed_recipe = None  # Clear any previously remixed recipes
            
            # Display the original recipe
            st.write("### Original Recipe")
            st.write(st.session_state.original_recipe)
        else:
            st.error("Please provide both a system prompt and a final user prompt.")

    # If an original recipe is present, offer the option to remix it
    if st.session_state.original_recipe:
        st.write("### Enter a new cuisine to remix the recipe")
        
        # Input for the new cuisine prompt
        new_cuisine_prompt = st.text_input("New Cuisine", placeholder="Enter a cuisine (e.g., Italian, Vegan, etc.)")
        
        # Button to remix the recipe
        if st.button("Remix Recipe"):
            if new_cuisine_prompt:
                # Call remix_recipe to get a new recipe based on the entered cuisine
                st.session_state.remixed_recipe = remix_recipe(client,st.session_state.original_recipe, new_cuisine_prompt)
                
                # Display the remixed recipe
                st.write("### Remixed Recipe")
                st.write(st.session_state.remixed_recipe)
            else:
                st.error("Please enter a cuisine to remix the recipe.")