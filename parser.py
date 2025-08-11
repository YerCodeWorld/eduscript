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
from typing import List, Optional
from enum import Enum
from logger_base import get_logger

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

class ContentBody(BaseModel):
    type: Optional[str]
    variation: Optional[str]
    content: str



class Parser:

    def __init__(self, exercise):
        self.exercise = exercise
        self.mode: Mode = Mode.SINGLE.value
        self.metadata: MetadataBody = None
        self.content: ContentBody = None

        self.logger = get_logger(self.__class__.__name__)

    def extract_mode(self):
        mode_re = re.compile(r"\s*.*?@MODE=multiple")
        is_multiple = len(re.findall(mode_re, self.exercise)) != 0
        if is_multiple:
            self.mode = Mode.MULTIPLE.value

    def parse_metadata(self):
        instance = Metadata(self.exercise)
        block = instance.extract_metadata_blocks()

        if not block:
            return ValueError("No metadata blocks found")

        if not instance.validate_metadata_keys(block):
            return ValueError("Found invalid Metadata key")

        if not instance.validate_metadata_values(block):
            return ValueError("Found invalid metadata value")

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

    def extract_content():
        pass

    def parse_type(self):
        instance = Blanks(blanks_sample)
        result = instance.parse_blanks()
        if result.ok:
            print(result.content.model_dump())
        else:
            print(result.errors)
            # is_valid = instance.validate_matching(result.value)
            # if not is_valid:
            #    return

    def run(self):
        self.extract_mode()
        self.logger.info(f"Determined mode: {self.mode}")

        self.parse_metadata()
        print(self.metadata)

        if self.mode = Mode.MULTIPLE.value:
            pass


exercise = """
@MODE=multiple

@metadata {
  type= blanks;
  title = myLife;
  instructions = Do not die please;
  difficulty=BEGINNER;
  isPublished = true;
  category = VOCABULARY;
  style = nature;
}

[type=blanks, variation=original]
@content {
    // ...

}
"""

instance = Parser(exercise)
instance.run()
