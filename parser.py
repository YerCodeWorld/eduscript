import re
from metadata import Metadata
from single.matching import Matching
from single.ordering import Ordering
from single.mcq import MCQ
from single.categorize import Categorize
from single.select import Select
from single.blanks import Blanks
from sample_data import *
from typing import List, Optional, Union
from enum import Enum
from logger_base import get_logger

from src.helpers import extract_type
from src.models import *
from enums import ExerciseTypes

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

class Parser:

    def __init__(self, code):
        self.exercise = code

        self.mode: Mode = Mode.SINGLE.value
        self.metadata: MetadataBody = None
        self.content: List[ExerciseContent] = []

        self.result: Exercise = None

        self.logger = get_logger(self.__class__.__name__)

    @staticmethod
    def extract_content(s: str, is_multiple=False) -> List[str]:
        content_re = re.compile(r"@content\s*.*?{(.*?)}", re.DOTALL)
        content: str = None

        m = content_re.findall(s)
        if not m:
            return ValueError("Couldn't extract any content bodies")

        if not is_multiple and len(m) == 1:
            return [content_re.sub("", m[0])]

        if is_multiple and (len(m) > 1):
            return [content_re.sub("", match) for match in m]
        return ValueError("No more than one content body found in multiple mode exercise")

    def extract_mode(self) -> None:
        """
        The mode feature is a flag that can be placed in the exercise (@MODE=multiple),
        to indicate we will create an exercise body with multiple exercises.

        If this flag is not present the code will assume mode is equal to single.
        """

        mode_re = re.compile(r"\s*.*?@MODE=multiple")
        is_multiple: bool = len(re.findall(mode_re, self.exercise)) != 0
        if is_multiple:
            self.mode = Mode.MULTIPLE.value
            # Remove from current string
            self.exercise = mode_re.sub("", self.exercise)

    def parse_metadata(self) -> None:
        instance: Metadata = Metadata(self.exercise)
        block: str = instance.extract_metadata_blocks()

        # First confirm the whole code is valid
        if not block:
            return ValueError

        if not instance.validate_metadata_keys(block):
            return ValueError

        if not instance.validate_metadata_values(block):
            return ValueError

        # Then populate the attributes of the class
        instance.create_base_structure(block)

        # Finally let's create an object we can model_dump
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

        # Also remove the metadata block from main string
        self.exercise = instance.remove_metadata_block(self.exercise).strip()

    def parse_content(self, exs: str):
        """
        Utility function for parsing a single mode exercise.
        Gets the type from metadata and invokes the proper class passing the exercise
        attribute as an argument
        """
        type_re = re.compile(r"\s*<([^>]+)>", re.DOTALL)

        class_mapping = {
            'blanks': Blanks,
            'ordering': Ordering,
            'mcq': MCQ,
            'categorize': Categorize,
            'select': Select,
            'matching': Matching
        }

        t: str = self.metadata.type
        v: str = self.metadata.variation

        # didn't think about it... i needed to find out what the type was before instanciating the class...
        # seems horrible specially after I called it again a bit below
        # well idk, it works, let it there until you find something better. Why k tho?
        k = extract_type(exs)
        if not isinstance(k, ValueError):
            t = k[0]

        exs_class = class_mapping.get(t)
        instance = exs_class(exs)

        if self.mode == Mode.MULTIPLE.value:
            r = instance.initial_load()
            if isinstance(r, ValueError):
                return r
            instance.exercise = type_re.sub("", instance.exercise)

        result = instance.parse_content()

        if not result.ok:
            self.logger.error(result.errors)
            return ValueError

        self.logger.info(f"Exercise has been parsed")
        self.content.append(ExerciseContent(exercise=result.content))

    def run(self):

        self.extract_mode()
        self.logger.info(f"MODE: {self.mode}")

        metadata_r = self.parse_metadata()
        if isinstance(metadata_r, ValueError):
            self.logger.error(metadata_r)
            return None
        self.logger.info(self.metadata)

        content_r = self.extract_content(self.exercise, self.mode == Mode.MULTIPLE.value)
        if isinstance(content_r, ValueError):
            self.logger.error(content_r)
            return None
        self.logger.info(content_r)

        for exs in content_r:
            self.parse_content(exs)

        self.result = Exercise(mode=self.mode, metadata=self.metadata, content=self.content)
        print(self.result.model_dump())
        #if self.mode == Mode.MULTIPLE.value:
        #    self.logger.warning("Exercise is multiple")

        # self.parse_content()

        # exercise = Exercise(mode=self.mode, metadata=self.metadata, content=self.content)
        # print(exercise.model_dump())

exercise = """
@MODE=multiple

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
    <ordering, original>

    # Don't get distracted!
    She  | takes | a   | shower | in | the | morning | [forgets] | [likes];
    they | do    | the | homework;
    I    | watch | [cooking] | tv | in | the| afternoon;
    we   | go    |   to work | at |seven;

    # Can you brush that!??
    He   | brushes | his   | teeth | [bed] | with | colgate;

    they | have    | lunch | together;
}

@content {

<categorize, colors>

ANIMALS = Lion | Chicken | Tiger | Dog | Cat;
FRUITS = Banana | apple | Pear | Orage | Dragon Fruit;
COLORS = Blue | Red | White | Green | Black;
CLASSROOM = Pencil | Notebook | School Bag | Computer | Eraser;
@EXTRA=[beach|happyness]
}
"""

instance = Parser(exercise)
result = instance.run()
if not result:
    print("...")
