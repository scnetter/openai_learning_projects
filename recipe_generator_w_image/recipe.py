# User gives list of ingredients
# completion model generates a recipe
# DALL-E generates an image of the dish

import os
import openai
import re
import requests
import shutil

openai.api_key = os.getenv("OPENAI_API_KEY")


def create_dish_prompt(list_of_ingredients):
    prompt = (
        f"Create a detailed recipe based on only the following ingredients: {', '.join(list_of_ingredients)}\n"
        + f"Additionally, assign a title starting with  'Recipe Title: ' to this recipe."
    )
    return prompt


def extract_title(text):
    # Get the portion after the "Recipe Title: " which will ultimately be send to DALL-E
    return (
        re.findall("^.*Recipe Title: .*$", text, re.MULTILINE)[0]
        .strip()
        .split("Recipe Title: ")[-1]
    )


def save_image(url, file_name):
    image_res = requests.get(url, stream=True)
    if image_res.status_code == 200:
        with open(file_name, "wb") as f:
            shutil.copyfileobj(image_res.raw, f)
    else:
        print("ERROR LOADING IMAGE")

    return image_res.status_code


recipe_prompt = create_dish_prompt(
    [
        "chicken",
        "condensed soup",
        "onions",
        "Chicken stock",
        "whipping cream",
        "cheddar cheese",
        "celery",
        "carrots",
    ]
)

response = openai.Completion.create(
    engine="gpt-3.5-turbo-instruct",
    prompt=recipe_prompt,
    max_tokens=512,
    temperature=0.7,
)

recipe = response["choices"][0]["text"]
print(response["choices"][0]["text"])
recipe_title = extract_title(recipe)
print(recipe_title)

# Adding "professional food photography, 15mm, studio lighting" can improve the quality of the image.
image_url = openai.Image.create(
    prompt=recipe_title + " professional food photography, 15mm, studio lighting",
    n=1,
    size="512x512",
)["data"][0]["url"]
print(image_url)
save_image(image_url, "example.png")
