import streamlit as st
import openai as OpenAI
import working_prompts


# Function to call OpenAI's ChatGPT model with system/user prompts and optional examples
def get_chatgpt_response(client,system_prompt, user_prompt, examples=None):
    # Prepare the conversation with system and user inputs
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add example pairs if provided
    if examples:
        for example in examples:
            messages.append({"role": "user", "content": example['user']})
            messages.append({"role": "assistant", "content": example['system']})
    
    # Add the main user prompt
    messages.append({"role": "user", "content": user_prompt})
    
    # Call the OpenAI API with the constructed conversation
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Adjust model as necessary
        messages=conversation
    )
    
    return response.choices[0].message.content


def construct_conversation(system_prompt, user_prompt, examples):
    # Initialize the conversation with the system prompt
    conversation = [{"role": "system", "content": system_prompt}]
    
    # Add example user-assistant pairs if any
    for example in examples:
        conversation.append({"role": "user", "content": example['user']})
        conversation.append({"role": "assistant", "content": example['system']})
    
    # Add the final user prompt at the end of the conversation
    conversation.append({"role": "user", "content": user_prompt})
    
    return conversation