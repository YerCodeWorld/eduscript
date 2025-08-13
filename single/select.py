import re
from typing import List, Optional
from single.helpers import extract_instructions, load_metadata
from src.models import ParseResult, SelectContent, SelectWrapper

from core.registry import register_type

# Parses something like this
"""
# Select all the verbs
I [am] someone who [knows] when everything
[turns] bad and destiny [decides] it's time
for trouble.;

# Select all the adjectives
We [never] considered such an [amazing] person
to be this [bad]. What could actually have been
just a [smooth] step in the middle turned out
to be [horrific].;
"""

@register_type("select")
class Select:

    def __init__(self, exercise):

        self.exercise = exercise
        self.type: str = None
        self.variation: str = None

        self.pattern = re.compile(r"\[([a-zA-Z]+)\]")

    def initial_load(self):
         self.type, self.varation = load_metadata(self.exercise).data

    def parse_content(self):

        self.type, self.variation = load_metadata(self.exercise)

        chunks = [c.strip() for c in self.exercise.split(";")]
        items: List[SelectContent] = []

        for p in chunks:

            ins: str = ""

            if not p.strip():
                continue

            result = extract_instructions(p)
            if not result.ok:
                return ParseResult(ok=False, errors=[result.errors, p])
            ins = result.data
            p = result.result_string.replace("\n", " ")  # The renderer must determine based on screen size anyways

            selections = [m for m in re.findall(self.pattern, p)]
            if not selections:
                return ParseResult(ok=False, errors=["This paragraph does not seem to have any valid selections:", p])

            cleaned_text = re.sub(self.pattern, r"\1", p)

            items.append(SelectContent(instruction=ins, paragraph=cleaned_text, selections=selections))

        return ParseResult(ok=True, content=SelectWrapper(content=items))

    def valide_select(self):
        errors = []

        return len(errors) == 0
