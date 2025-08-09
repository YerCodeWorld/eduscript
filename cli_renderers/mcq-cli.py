import json
import random

exercise = """
{
    "content": [
        {
            "sentence": "Which are pets?",
            "options": ["elephant", "tiger", "parrot", "hamster"],
            "correctAnswers": [3, 4],
            "image": ""
        },
        {
            "sentence": "What are basic colors?",
            "options": ["purple", "magenta", "red", "blue"],
            "correctAnswers": [3, 4, 1],
            "image": ""
        },
        {
            "sentence": "How do you feel?",
            "options": ["tired", "bored", "happy", "angry"],
            "correctAnswers": [3, 4],
            "image": ""
        }
    ],
    "extraAnswers": [""]
}
"""

data = json.loads(exercise)
score = 0

for q in data["content"]:

    options = q["options"]
    correctAnswers = q["correctAnswers"]

    print(f"{q['sentence']}: \n")
    for i, option in enumerate(options):
        print(f"{i+1} - {option}")

    try:
        options = input("Enter options (comma separated): " ).split(",")
        for o in options:
            if int(o) in correctAnswers:
                print(f"Answer '{o}' is correct!")
                score += 1
            else:
                print(f"Answer '{o}' was not correct")

    except ValueError:
        print("An option you entered is not valid")


print("final score: ", score)
