import re
from logger_base import get_logger
from typing import List, Optional
from single.helpers import *
from src.models import ParseResult, OrderingContent, OrderingWrapper

from core.registry import register_type

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

@register_type("ordering")
class Ordering:

    def __init__(self, exercise):

        self.exercise = exercise
        self.type = None
        self.variation = None

        self.logger = get_logger(self.__class__.__name__)

    def initial_load(self):
        self.type, self.variation =  load_metadata(self.exercise).data

    def parse_content(self) -> ParseResult:

        items: List[OrderingContent] = []

        chunks = [c.strip() for c in self.exercise.split(";")]

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

            items.append(OrderingContent(instruction=ins, content=sn, distractors=distractors))

        return ParseResult(
            ok=True, content=OrderingWrapper(type=self.type, variation=self.variation, content=items)
            )

    @staticmethod
    def validate_ordering(data) -> bool:
        errors = []

        return len(errors) == 0

