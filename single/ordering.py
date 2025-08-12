import re
from logger_base import get_logger
from typing import List, Optional
from single.helpers import extract_instructions, parse_mcq_pattern

from src.models import ParseResult, OrderingContent, OrderingWrapper

# Constraints

"""
Model

{
    "instruction": "",
    "items": [""],
    "distractors": [""]
}
"""

# 1 - Pipe separated indicate items of a sentence
# 2 - Non-pipe separated indicate Every char is an item. Spaces are special cases
# 3 - if brackets [] found populate distractors
# 4 - # indicates sentence instruction population



class Ordering:

    def __init__(self, exercise):

        self.exercise = exercise
        self.logger = get_logger(self.__class__.__name__)
        self.distractor_re = ""  # update this instead

    def parse_content(self) -> ParseResult:

        items: List[OrderingContent] = []

        chunks = [c.strip() for c in self.exercise.split(";")]
        distractor_re = re.compile(r"\[(.*?)\]")

        for sn in chunks:

            if sn == "":
                continue

            ins: str = ""
            distractors: List[str] = None

            result = extract_instructions(sn)
            if result.ok:
                ins = result.data
                sn = result.result_string.replace("\n", " ")

            # This is what I was talking about, ordering can benefit from mcq pattern as many exercise types
            result = parse_mcq_pattern(sn, True)
            if not result.ok:
                return ParseResult(ok=False, errors=[result.errors])

            if len(result.result_string) < 3:
                return ParseResult(ok=False, errors=["Sentence with too little values", sn])

            sn = result.result_string
            distractors = result.data
            """
            print(f"
                Sentence: {sn}
                Instruction: {ins}
                Distractors: {distractors}
                ")
            """
            items.append(OrderingContent(instruction=ins, content=sn, distractors=distractors))

        return ParseResult(ok=True, content=OrderingWrapper(content=items))

    @staticmethod
    def validate_ordering(data) -> bool:
        errors = []

        return len(errors) == 0

