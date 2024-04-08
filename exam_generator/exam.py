import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def create_test_prompt(topic, num_questions, num_possible_answers):
    prompt = (
        f"Create a multiple choice quiz on he topic of {topic} consisting of {num_questions} questions. "
        + f"Each question should have {num_possible_answers} options. "
        + f"Also include the correct answer for each question using the starting string: 'Correct Answer:' "
    )
    return prompt


response = openai.Completion.create(
    engine="gpt-3.5-turbo-instruct",
    prompt=create_test_prompt("US History", 4, 4),
    max_tokens=256,
    temperature=0.6,
)

print(response["choices"][0]["text"])
