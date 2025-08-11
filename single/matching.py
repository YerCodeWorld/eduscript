import re
from dataclasses import dataclass
from logger_base import get_logger
from dataclasses import dataclass
from pydantic import BaseModel
from typing import List, Optional
from single.helpers import remove_distractors

# Pair type
class Pair(BaseModel):
    left: str
    right: str

# Matching Content Type
class MatchingContent(BaseModel):
    pairs: List[Pair]
    distractors: Optional[List[str]] = None
    points: Optional[List[int]]

@dataclass
class ParseResult:
    ok: bool
    content: Optional[MatchingContent] = None
    error: str = None


# Constraints
"""

    apple = red;
    pear :: green;
    grape  = purple;
    banana = yellow;
    = [blank, white];

"""
"""
Model

{
    "left": "",
    "right": ""
}
"""

# 1 - = or :: separate the left and right sides
# 2 - empty left and line.startWith("=") indicates distractors (brackets, comma-separated)

class Matching:

    def __init__(self, content: str):

        self.content = content
        self.logger = get_logger(self.__class__.__name__)

    def parse_matching(self) -> ParseResult:

        # PATTERN FOR EXTRA: @EXTRA = [ value1 | value2 ]
        result = remove_distractors(self.content)
        if not result.ok:
            return result.error
        distractors = result.data
        self.content = result.result_string

        pairs: List[Pair] = []
        chunks = [c.strip() for c in self.content.split(";") if c.strip()]

        for sn in chunks:

            has_eq = '=' in sn
            has_colon = '::' in sn

            if sn.count("=") > 1 or sn.count("::") > 1:
                return ParseResult(ok=False, error=f"More than one separator found in a single sentence: {sn!r}")

            if has_eq and has_colon:
                return ParseResult(ok=False, error=f"Ambiguous separators in: {sn!r}")
            if not (has_eq or has_colon):
                return ParseResult(ok=False, error=f"No separators found in: {sn!r}")

            sep = '::' if has_colon else '='

            left, right = [p.strip() for p in sn.split(sep, 1)]
            if not (left and right):
                return ParseResult(ok=False, error=f"Incomplete pair in: {sn!r}")

            pairs.append(Pair(left=left, right=right))

        return ParseResult(ok=True, content=MatchingContent(pairs=pairs, distractors=distractors, points=[]), error=[])

    def validate_matching(self, content: MatchingContent) -> bool:
        errors = []

        # min/max length logic
        # duplicated lines logic
        # validate right and left items
        # validate extra answers

        return len(errors) == 0

