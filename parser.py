import re
from metadata import Metadata
from single.matching import Matching
from single.ordering import Ordering
from single.mcq import MCQ
from single.categorize import Categorize
from single.select import Select
from single.blanks import Blanks
from sample_data import *
from pydantic import BaseModel
from typing import List, Optional, Union
from enum import Enum
from logger_base import get_logger

from src.models import *

# Process might look like this:

"""
1 - Check if MODE = dynamic
2 - Call corresponding process stack

If static

3 - Parse Metadata
4 - Based on info, use corresponding parser
5 - Validate exercise
6 - If no errors, return result model dump
"""

class Mode(Enum):
    SINGLE = "single"
    MULTIPLE = "multiple"

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
    type: Optional[str]
    variation: Optional[str]
    content: Union[
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
    content: List[ExerciseContent]

class Parser:

    def __init__(self, exercise):
        self.exercise = exercise
        self.mode: Mode = Mode.SINGLE.value
        self.metadata: MetadataBody = None
        self.content: List[ExerciseContent] = []

        self.result: Exercise = None

        self.logger = get_logger(self.__class__.__name__)

    @staticmethod
    def extract_content(s, is_multiple=False):
        content_re = re.compile(r"@content\s*.*?{(.*?)}", re.DOTALL)
        content: str = None

        if not is_multiple:
            return content_re.findall(s)[0]



    def extract_mode(self):
        mode_re = re.compile(r"\s*.*?@MODE=multiple")
        is_multiple = len(re.findall(mode_re, self.exercise)) != 0
        if is_multiple:
            self.mode = Mode.MULTIPLE.value
            # Remove from current string
            self.exercise = mode_re.sub("", self.exercise)

    def parse_metadata(self):
        instance = Metadata(self.exercise)
        block = instance.extract_metadata_blocks()

        if not block:
            return ValueError

        if not instance.validate_metadata_keys(block):
            return ValueError

        if not instance.validate_metadata_values(block):
            return ValueError

        instance.create_base_structure(block)

        self.metadata = MetadataBody(
                type=instance.type,
                variation=instance.variation,
                category=instance.category,
                difficulty=instance.difficulty,
                style=instance.style,
                instructions=instance.instructions,
                title=instance.title,
                packageId=instance.packageId,
                is_published=instance.is_published
            )

        self.exercise = instance.remove_metadata_block(self.exercise).strip()

    def parse_type(self):

        class_mapping = {
            'blanks': Blanks,
            'ordering': Ordering,
            'mcq': MCQ,
            'categorize': Categorize,
            'select': Select,
            'matching': Matching
        }

        class_type = class_mapping.get(self.metadata.type)

        instance = class_type(self.exercise)
        result = instance.parse_content()
        if result.ok:
            self.content.append(ExerciseContent(type=self.metadata.type, variation=self.metadata.variation, content=result.content))
        else:
            print(result.errors)

    def run(self):
        self.extract_mode()
        self.logger.info(f"Determined mode: {self.mode}")

        r = self.parse_metadata()
        if r == ValueError:
            return None

        self.logger.info(self.metadata)
        if self.mode == Mode.MULTIPLE.value:
            self.logger.warning("Exercise is multiple")

        self.exercise = self.extract_content(self.exercise)
        self.parse_type()

        exercise = Exercise(mode=self.mode, metadata=self.metadata, content=self.content)
        print(exercise.model_dump())

exercise = """
@metadata {
  type = ordering;
  title = The best time of my life;
  instructions = Do not die please;
  difficulty=BEGINNER;
  isPublished = true;
  category = VOCABULARY;
  style = nature;
}

@content {
# Don't get distracted!
She  | takes | a   | shower | in | the | morning | [forgets] | [likes];
they | do    | the | homework;
I    | watch | [cooking] | tv | in | the| afternoon;
we   | go    |   to work | at |seven;

# Can you brush that!??
He   | brushes | his   | teeth | [bed] | with | colgate;

they | have    | lunch | together;
}
"""

instance = Parser(exercise)
result = instance.run()
if not result:
    print("Oops!")
