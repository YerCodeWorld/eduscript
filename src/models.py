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

class MultipleMetadata(BaseModel):
    type: str
    variation: str

# Matching
class Pair(BaseModel):
    left: str
    right: str

class MatchingContent(BaseModel):
    type: Optional[str] = None
    variation: Optional[str] = "original"
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
    type: Optional[str] = None
    variation: Optional[str] = "original"
    content: List[BlanksContent]

# Ordering

class OrderingContent(BaseModel):
    instruction: Optional[str]
    content: List[str]
    distractors: Optional[List[str]]
    points: Optional[List[int]] = []

class OrderingWrapper(BaseModel):
    type: Optional[str] = None
    variation: Optional[str] = "original"
    content: List[OrderingContent]

# Select

class SelectContent(BaseModel):
    instruction: str
    paragraph: str
    selections: List[str]
    points: Optional[List[int]] = []

class SelectWrapper(BaseModel):
    type: Optional[str] = None
    variation: Optional[str] = "original"
    content: List[SelectContent]

# MCQ

class MCQcontent(BaseModel):
    question: str
    options: List[str]
    correctOptions: List[str]
    points: Optional[List[int]]

class MCQwrapper(BaseModel):
    type: Optional[str] = None
    variation: Optional[str] = "original"
    content: List[MCQcontent]

# Categorize
class CategorizeContent(BaseModel):
    category: str
    items: List[str]
    points: Optional[List[int]]

class CategorizeWrapper(BaseModel):
    type: Optional[str] = None
    variation: Optional[str] = "original"
    content: List[CategorizeContent]
    distractors: Optional[List[str]] = None

# Exercise
class MetadataBody(BaseModel):
    type: str
    variation: str
    instructions: Optional[str] = "Complete the exercise"
    category: Optional[str] = "General"
    difficulty: Optional[str] = "Beginner"
    style: Optional[str] = None
    title: Optional[str] = "Exercise"
    packageId: Optional[str] = None
    variation: Optional[str] = "original"
    is_published: Optional[bool] = False

class ExerciseContent(BaseModel):
    exercise: Union[
            'BlanksWrapper',
            'SelectWrapper',
            'MCQwrapper',
            'OrderingWrapper',
            'CategorizeWrapper',
            'MatchingContent'
        ]

class Exercise(BaseModel):
    mode: str
    metadata: MetadataBody
    exercises: List[ExerciseContent]
