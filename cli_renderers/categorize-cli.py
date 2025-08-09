import json
import random

exercise = """
{
    "variation": "corners",
    "categories": [
        {
            "name": "DOCTOR",
            "items": [
                "I check my patients and write medical reports in the afternoon.",
                "I work long shifts at the hospital, sometimes at night"
            ]
        },
        {
            "name": "ATHLETE",
            "items": [
                "I train for two hours every morning and follow a special diet",
                "I go to the gym before sunrise to practice for competitions."
            ]
        },
        {
            "name": "TEACHER",
            "items": [
                "I correct homework and prepare lessons for the next day.",
                "I attend meetings with other teachers once a week."
            ]
        },
        {
            "name": "MOTHER",
            "items": [
                "I wake up early to prepare breakfast and get the kids ready for school",
                "I help my children with their homework after work."
            ]
        }
    ]
}
"""

data = json.loads(exercise)
c = [n["name"] for n in data["categories"]]

def process_content(data):

  a = []

  for obj in data["categories"]:

    items = []

    k = obj["name"]
    v = obj["items"]

    # create a list off available values
    items.extend(v)

    for i in items:

      # create individual tuple category/item
      t = (k, i)
      a.append(t)

  return a

def exercise(data):
  global c

  print("Categories: \n")
  for i, n in enumerate(c):
    print(f"{i+1} - {n}")

  random.shuffle(data)

  for correct_key, item in data:
    print(f"\n Select category for: \n'{item}'")

    while True:
        user_input = input("Select a number: ")

        # Validate input
        try:
            selected_index = int(user_input) - 1
            selected_key = c[selected_index]
            break
        except (ValueError, IndexError):
            print("Invalid selection.")
            continue

    # Check answer
    if selected_key == correct_key:
        print("✅ Correct!")
    else:
        print(f"❌ Incorrect. It belongs to '{correct_key}'.")

def main():

  processed_content = process_content(data)
  exercise(processed_content)

main()
