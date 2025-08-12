from dataclasses import dataclass
from typing import List, Optional, Union
from pydantic import BaseModel

@dataclass
class ParseResult:
    ok: bool
    content: Optional[Union[
            'BlanksContent',
            'SelectContent',
            'MCQcontent',
            'OrderingContent',
            'CategorizeBody',
            'MatchingContent'
        ]] = None
    errors: Optional[List[str]] = None


# Matching
class Pair(BaseModel):
    left: str
    right: str

class MatchingContent(BaseModel):
    pairs: List[Pair]
    distractors: Optional[List[str]] = None
    points: Optional[List[int]] = None


# Blanks
class Blank(BaseModel):
    position: int
    correct_options: Optional[List[str]]
    options: Optional[List[str]]

class BlanksContent(BaseModel):
    sentence: str
    blanks: List[Blank]
    instruction: Optional[str]
    points: Optional[List[int]] = None

class BlanksWrapper(BaseModel):
    content: List[BlanksContent]


# Ordering

class OrderingContent(BaseModel):
    instruction: Optional[str]
    content: List[str]
    distractors: Optional[List[str]]
    points: Optional[List[int]] = []

class OrderingWrapper(BaseModel):
    content: List[OrderingContent]

# Select

class SelectContent(BaseModel):
    instruction: str
    paragraph: str
    selections: List[str]
    points: Optional[List[int]] = []

class SelectWrapper(BaseModel):
    content: List[SelectContent]


# MCQ

class MCQcontent(BaseModel):
    question: str
    options: List[str]
    correctOptions: List[str]
    points: Optional[List[int]]

class MCQwrapper(BaseModel):
    content: List[MCQcontent]

# Categorize

class CategorizeContent(BaseModel):
    category: str
    items: List[str]
    points: Optional[List[int]]

class CategorizeWrapper(BaseModel):
    categories: List[CategorizeContent]
    distractors: Optional[List[str]] = None


