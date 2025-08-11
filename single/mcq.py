import re
from pydantic import BaseModel
from dataclasses import dataclass
from typing import List, Optional
from single.helpers import extract_instructions, parse_mcq_pattern

class MCQcontent(BaseModel):
    question: str
    options: List[str]
    correctOptions: List[str]
    # adding now, but logic for this will be relevant come updates on
    points: Optional[List[int]]

class MCQwrapper(BaseModel):
    content: List[MCQcontent]

@dataclass
class ParseResult:
    ok: bool
    content: Optional[MCQwrapper] = None
    errors: Optional[List[str]] = None


class MCQ:

    def __init__(self, exercise):

        self.data = exercise
        self.errors = {
            "missing_correct": "No correct answers found for {0} - {1} Invalid sentence sequence. ",
            "empty_sentence": "Empty sentence found. Did you create a sentence with correct answers [...] only?"
        }


    def parse_mcq(self) -> ParseResult:

        # CONVERED EDGE-CASES

        # 1 - No instructions '#' found
        # 2 - Instructions too short cases
        # 3 - No options found
        # 4 - No correct answers or empty [] correct answers brackets
        # 5 - Sentence normalization case


        items: List[MCQcontent] =  []
        chunks = [c.strip() for c in self.data.split(";")]

        # Using enumerate this time
        for i, sn in enumerate(chunks):

            if sn == "":
                continue

            question: str = ""
            options: List[str] = []
            correct_options: List[str] = []

            # instructions are MANDATORY in this exercise type, unlike ordering for example
            result = extract_instructions(sn)
            if not result.ok:
                return ParseResult(ok=False, errors=[result.errors, p])
            question = result.data
            sn = result.result_string.replace("\n", " ")

            result = parse_mcq_pattern(sn)
            if not result.ok:
                return ParseResult(ok=False, errors=[result.errors, sn])
            correct_options = result.data
            options = result.result_string

            items.append(MCQcontent(question=question, options=options, correctOptions=correct_options, points=[]))

        return ParseResult(ok=True, content=MCQwrapper(content=items), errors=[])

    def validate_mcq() -> bool:
        errors: List[str] = []



        return len(errors) == 0



