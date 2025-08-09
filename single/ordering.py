import re
from logger_base import get_logger
from dataclasses import dataclass
from pydantic import BaseModel
from typing import List, Optional

class OrderingContent(BaseModel):
    instruction: Optional[str]
    content: List[str]
    distractors: Optional[List[str]]

class OrderingBase(BaseModel):
    values: List[OrderingContent]

@dataclass
class ParseResult:
    ok: bool
    content: Optional[OrderingContent] = None
    error: Optional[str] = None

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

    def parse_ordering(self) -> ParseResult:

        items: List[OrderingContent] = []

        chunks = [c.strip() for c in self.exercise.split(";")]
        distractor_re = re.compile(r"\[(.*?)\]")

        for sn in chunks:

            if sn == "":
                continue

            ins: str = ""
            distractors: List[str] = None

            # Makes it so that we can write until we find a ';', and instructions logic would still work
            if "\n" in sn and "#" in sn.split("\n")[0]:
                lines = sn.split("\n")
                if lines[0].startswith("#"):
                    ins = lines[0][1:].strip() # slice to remove '#'
                    sn = ' '.join(lines[1:])
                    # we should raise a warning else

            m = distractor_re.findall(sn)
            # substitute match with none
            sn = distractor_re.sub("", sn)

            # edge-case: non-critical, but return just because
            if sn.replace("|", "").strip() == "":
                return ParseResult(ok=False, error="Empty sentence found. Did you create a sentence with distractors [...] only?")

            if m:
                distractors = m or []

            sn = [s.strip() for s in sn.split("|")] if "|" in sn else [sn]
            sn = [s for s in sn if s.strip()] # removing any remaining empty items
            """
            print(f"
                Sentence: {sn}
                Instruction: {ins}
                Distractors: {distractors}
                ")
            """
            items.append(OrderingContent(instruction=ins, content=sn, distractors=distractors))

        return ParseResult(ok=True, content=OrderingBase(values=items), error=[])

    @staticmethod
    def validate_ordering(data):
        errors = []

        return len(errors) == 0

