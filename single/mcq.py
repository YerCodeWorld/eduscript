import re
from pydantic import BaseModel
from dataclasses import dataclass
from typing import List, Optional


class MCQcontent(BaseModel):
    question: str
    options: List[str]
    correctOptions: List[str]

    # adding now, but logic for this will be relevant come updates on
    points: Optional[List[int]]

class MCQwrapper(BaseModel):
    content: List[MCQcontent]

class ParseResult(BaseModel):
    pass


distractor_re = re.compile(r"\[(.*?)\]")

exercise = """

# what is this?
value1 | value2 | [value3] | [value4];

# What is the capital of Japan?
ShanGai | Seol | Paris | [Tokyo];
"""

# Content

# question: str
# options: str
# correctOptions: str


def parse_mcq(exercise):


    items: List[MCQcontent] =  []
    chunks = [c.strip() for c in exercise.split(";")]

    # Using enumerate this time
    for i, sn in enumerate(chunks):

        if sn == "":
            continue

        if not "|" in sn:
            print(f"Error, no options found in {i} - {sn}")
            return False

        question: str = ""
        options: List[str] = []
        correct_options: List[str] = []

        # instructions are MANDATORY in this exercise type
        if not "\n"  in sn:
            print(f"The following question {i+1} - {sn} is not valid")

        if sn.split("\n")[0].startswith("#"):
            lines = sn.split("\n")

            if len(lines[0].strip()) > 3:
                question = lines[0][1:].strip()
                sn = ' '.join(lines[1:])
            else:
                print("""
                    Instruction too short, did you really mean this? Consider adding some extra
                    non-distracting characters if so.
                    """)
                return False

        else:

            print(f"""
                  Missing instruction for question {i+1}: \n{sn}\n Please add a proper '#' initialized
                  line on top.

                  # instruction
                  option | option | [correctOption]
                  """.strip())
            return False

        matches = distractor_re.findall(sn)
        if matches:
            correct_options = matches

        sn = distractor_re.sub("", sn)

        if sn.replace("|", "").strip() == "":
            return ParseResult(ok=False, error="Empty sentence found. Did you create a sentence with distractors [...] only?")

        sn = [s.strip() for s in sn.split("|")]
        sn = [s for s in sn if s.strip()]

        print(f"""
              Question: {question}
              Options: {sn}
              Answers: {correct_options}
              """)

        items.append(MCQcontent(question=question, options=sn, correctOptions=correct_options, points=[]))

    return MCQwrapper(content=items)


# @%033...[033
# @ function call
# % open
# int function identifier
# ... content
# [ close

parse_mcq(exercise)














