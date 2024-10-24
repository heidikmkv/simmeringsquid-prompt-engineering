import streamlit as st

st.title("Project Simmering Squid: experiment with ChatGPT prompts for multilingual recipe generation")

from openai import OpenAI

openai_api_key = st.secrets["openai_api_key"]
client = OpenAI(api_key=openai_api_key)

text_example_recipe_prompt = 'ice cream sundae'
text_example_recipe_reply = '**Ice Cream Sundae**\n\n**Ingredients:**\n- 2 scoops of ice cream (flavor of your choice)\n- Chocolate syrup\n- Whipped cream\n- Sprinkles\n- Cherry\n\nInstructions:\n1. Place 2 scoops of ice cream in a bowl.\n2. Drizzle chocolate syrup over the ice cream.\n3. Top with whipped cream.\n4. Sprinkle some colorful sprinkles over the whipped cream.\n5. Garnish with a cherry on top.'
text_systemprompt_recipe = "You are an assistant trained to provide recipes in less than 150 words in a factual, serious tone, \
                                       without any closing remarks like 'Enjoy!' or similar phrases. \
                                       The recipe begins with the name of the dish. \
                                       The ingredients unordered list is concise, with bullet points being combined where it makes sense, \
                                       for example: salt & pepper on one line instead of two. \
                                       Cooking instructions should be no more than 5 steps. \
                                       DO NOT talk casually to the user. No exclamation points. \
                                       If the prompt does not pertain to food, \
                                       you must reply to the user: Please enter the name of a dish."

text_example_remix_prompt = 'transform the following recipe into keto: \n ' + text_example_recipe_reply
text_example_remix_reply = keto_sundae = "**Keto Ice Cream Sundae**\n\n**Ingredients:**\n- 2 scoops of keto ice cream (flavor of your choice)\n- Sugar-free chocolate syrup\n- Unsweetened whipped cream\n- Chopped nuts\n- Fresh berries (optional)\n\n**Instructions:**\n1. Place 2 scoops of keto ice cream in a bowl.\n2. Drizzle sugar-free chocolate syrup over the ice cream.\n3. Top with unsweetened whipped cream.\n4. Sprinkle chopped nuts or fresh berries if desired."
text_systemprompt_remix = "You are an assistant trained to change recipes to a new diet or cuisine \
                             in a factual, serious tone, with no editorializing, no extra text, \
                             and no closing remarks like 'Enjoy!'. Reply with exactly the same format \
                             as what you're given, just updated for the new diet or cuisine. \
                             If the input is 'Please enter the name of a dish.', reply with: No recipe provided. \
                             If the diet/cuisine prompt is not a diet or cuisine, reply with: Please provide a diet or cuisine."


def recipe_generator(client,text_prompt_recipe):
    # prompt linting goes here
    recipe_conversation = [{"role": "system", "content": text_systemprompt_recipe},
                            {"role": "user", "content": text_example_recipe_prompt},
                            {"role": "assistant","content":text_example_recipe_reply},
                            {"role": "user", "content": text_prompt_recipe}]
    text_recipe = chat_with_gpt(recipe_conversation)
    return text_recipe
    
def recipe_remixer(client,text_prompt_remix,text_recipe):
    if 'Please enter the name of a dish' in text_recipe:
        text_remix = 'Please enter the name of a dish.'
    else:
        prompt_text = 'transform the following recipe into '+text_prompt_remix+' style: '+text_recipe
        remix_conversation = [{"role": "system", "content": text_systemprompt_remix},
                              {"role": "user", "content": text_example_remix_prompt},
                              {"role": "assistant","content":text_example_remix_reply},
                              {"role": "user", "content": prompt_text}]
        text_remix = chat_with_gpt(remix_conversation)
    return text_remix

# Function to interact with ChatGPT
def chat_with_gpt(conversation):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Adjust model as necessary
        messages=conversation
    )
    return response.choices[0].message.content