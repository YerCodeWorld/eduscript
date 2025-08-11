import re
from typing import List, Optional
from pydantic import BaseModel
from dataclasses import dataclass
from single.helpers import extract_instructions

class SelectContent(BaseModel):
    instruction: str
    paragraph: str
    selections: List[str]
    points: Optional[List[int]]

class SelectWrapper(BaseModel):
    content: List[SelectContent]

@dataclass
class ParseResult:
    ok: bool
    content: Optional[SelectWrapper] = None
    errors: Optional[List[str]] = None

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

class Select:

    def __init__(self, exercise):

        self.data = exercise
        self.pattern = re.compile(r"\[([a-zA-Z]+)\]")

    def parse_select(self):

        chunks = [c.strip() for c in self.data.split(";")]
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
