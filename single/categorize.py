import re
from typing import List, Optional
from sample_data import categorize_sample
from single.helpers import remove_distractors
from src.helpers import extract_type

from src.models import ParseResult, CategorizeContent, CategorizeWrapper

class Categorize:

    def __init__(self, exercise):

        self.exercise = exercise
        self.type = None
        self.variation = None

    def initial_load(self):

        r = extract_type(self.exercise)
        if isinstance(r, ValueError):
            return ParseResult(ok=False, errors=[r])
        self.type, self.variation = r[0].strip(), r[1].strip()
        return ParseResult(ok=True)

    def parse_content(self):

        # PATTERN FOR EXTRA: @EXTRA = [ value1 | value2 ]
        result = remove_distractors(self.exercise)
        if not result.ok:
            return result.error
        distractors = result.data
        exercise = result.result_string

        items: List[CategorizeContent] = []
        chunks = [c.strip() for c in exercise.split(";")]

        for i, sn in enumerate(chunks):

            category: str = ""
            values: List[str] = []

            # ignore extra "\n" or " " items
            if not sn.strip():
                continue

            if ("=" not in sn) or not (sn.split("=")[0]):
                return ParseResult(ok=False, errors=[f"No category name found in sentence {i} - {sn}"])


            # enforce at least two values, althought that's a job for the validator
            if "|" not in sn:
                return ParseResult(ok=False, errors=[f"Need at least two values in a sentece content {i} - {sn}"])

            category = sn.split("=")[0]
            # We could've sliced no? Don't judge me... Being a creative self and it works anyways
            sn = sn.replace(category+"=", "")
            category = category.strip()

            values = [s.strip() for s in sn.split("|") if "|" in sn]

            items.append(CategorizeContent(category=category, items=values, points=[]))

        # We could add logic for breaking single categories exercises, but we'll let that to the validator
        return ParseResult(
            ok=True, content=CategorizeWrapper(type=self.type, variation=self.variation, content=items, distractors=distractors)
            )

    def validate_categorize(data):
        errors = []


        return len(errors) == 0



