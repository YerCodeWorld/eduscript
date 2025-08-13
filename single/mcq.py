import re
from typing import List, Optional
from single.helpers import *
from core.registry import register_type
from src.models import ParseResult, MCQcontent, MCQwrapper

@register_type("mcq")
class MCQ:

    def __init__(self, exercise):

        self.exercise = exercise
        self.type: str = None
        self.variation: str = None

        # This
        self.errors = {
            "missing_correct": "No correct answers found for {0} - {1} Invalid sentence sequence. ",
            "empty_sentence": "Empty sentence found. Did you create a sentence with correct answers [...] only?"
        }

    def initial_load(self):
         self.type, self.varation = load_metadata(self.exercise).data

    def parse_content(self) -> ParseResult:

        # CONVERED EDGE-CASES

        # 1 - No instructions '#' found
        # 2 - Instructions too short cases
        # 3 - No options found
        # 4 - No correct answers or empty [] correct answers brackets
        # 5 - Sentence normalization case


        items: List[MCQcontent] =  []
        chunks = [c.strip() for c in self.exercise.split(";")]

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
                return ParseResult(ok=False, errors=[result.errors, sn])
            question = result.data
            sn = result.result_string.replace("\n", " ")

            result = parse_mcq_pattern(sn)
            if not result.ok:
                return ParseResult(ok=False, errors=[result.errors, sn])
            correct_options = result.data
            if len(correct_options) == 0:
                return ParseResult(ok=False, errors=["Sentence does not have any correct options", sn])

            options = result.result_string

            items.append(MCQcontent(question=question, options=options, correctOptions=correct_options, points=[]))

        return ParseResult(ok=True, content=MCQwrapper(content=items), errors=[])

    def validate_mcq() -> bool:
        errors: List[str] = []



        return len(errors) == 0



