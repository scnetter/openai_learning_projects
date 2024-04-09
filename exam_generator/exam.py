import openai
import os

# TODO: Refactor create_view_* to use a boolean to show answers or not.
openai.api_key = os.getenv("OPENAI_API_KEY")


def create_test_prompt(topic, num_questions, num_possible_answers):
    prompt = (
        f"Create a multiple choice quiz on he topic of {topic} consisting of {num_questions} questions. "
        + f"Each question should have {num_possible_answers} options. Don't use questions where the answer relies on opinion."
        + f"Also include the correct answer for each question using the starting string: 'Correct Answer:' "
    )
    return prompt


response = openai.Completion.create(
    engine="gpt-3.5-turbo-instruct",
    prompt=create_test_prompt("US History", 4, 4),
    max_tokens=256,
    temperature=0.6,
)

test = response["choices"][0]["text"]


def create_student_view(test, num_questions):
    student_view = {1: ""}
    question_number = 1
    for line in test.split("\n"):
        if not line.startswith("Correct Answer:"):
            student_view[question_number] += line + "\n"
        else:
            if question_number < num_questions:
                question_number += 1
                student_view[question_number] = ""
    return student_view


student_view = create_student_view(test, 4)

for key in student_view:
    print(student_view[key])


def extract_answer(test, num_questions):
    answers = {1: ""}
    question_number = 1
    for line in test.split("\n"):
        if line.startswith("Correct Answer:"):
            answers[question_number] += line + "\n"
            if question_number < num_questions:
                question_number += 1
                answers[question_number] = ""
    return answers


answers = extract_answer(test, 4)

for key in answers:
    print(f"{key}: {answers[key]}")
