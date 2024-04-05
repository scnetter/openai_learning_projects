import os
import openai 

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(model="gpt-3.5-turbo-instruct", 
                                    prompt="Give me two reasons to learn openai with python", 
                                    temperature=0, max_tokens=300)

print(response.choices[0].text)