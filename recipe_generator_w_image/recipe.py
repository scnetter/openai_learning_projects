# User gives list of ingredients
# completion model generates a recipe
# DALL-E generates an image of the dish

import os
import openai
import re

openai.api_key = os.getenv("OPENAI_API_KEY")


def create_dish_prompt(list_of_ingredients):
    prompt = (
        f"Create a detailed recipe based on only the following ingredients: {', '.join(list_of_ingredients)}\n"
        + f"Additionally, assign a title starting with  'Recipe Title: ' to this recipe."
    )
    return prompt


def extract_title(text):
    # Get the portion after the "Recipe Title: " which will ultimately be send to DALL-E
    return re.findall("^.*Recipe Title: .*$", text, re.MULTILINE)[0].strip().split('Recipe Title: ')[-1]


recipe_prompt = create_dish_prompt(["ham", "turkey", "eggs", "bread"])

response = openai.Completion.create(
    engine="gpt-3.5-turbo-instruct",
    prompt=recipe_prompt,
    max_tokens=512,
    temperature=0.7,
)

recipe = response["choices"][0]["text"]
recipe_title = extract_title(recipe)
