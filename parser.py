import re
from metadata import Metadata
from sample_data import *
from enum import Enum
from logger_base import get_logger
from core.loader import load_plugins
from core.registry import get_handler
from single.helpers import load_metadata
from src.models import *
from enums import ExerciseTypes

class Mode(Enum):
    SINGLE = "single"
    MULTIPLE = "multiple"

class Parser:

    def __init__(self, code):

        # Initial string
        self.exercise = code

        # Parsing Processes
        self.mode: Mode = Mode.SINGLE.value
        self.metadata: MetadataBody = None
        self.content: List[ExerciseContent] = []

        # Final object
        self.result: Exercise = None

        self.logger = get_logger(self.__class__.__name__)

    @staticmethod
    def extract_content(s: str, is_multiple=False) -> List[str]:
        content_re = re.compile(r"@content\s*.*?{(.*?)}", re.DOTALL)
        content: str = None

        m = content_re.findall(s)
        if not m:
            raise ValueError("Couldn't extract any content bodies")

        if not is_multiple and len(m) == 1:
            return [content_re.sub("", m[0])]

        if is_multiple and (len(m) > 1):
            return [content_re.sub("", match) for match in m]

        raise ValueError("No more than one content body found in multiple mode exercise")

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
        self.logger.info(f"MODE: {self.mode}")

    def parse_metadata(self) -> None:

        instance = Metadata(self.exercise)
        block: str = None

        try:

            block = instance.get_metadata_block()
            self.logger.info("Extracted metadata block succesfully.")

            instance.validate_keys(block)
            self.logger.info("Metadata keys have been correctly validated.")

            instance.validate_values(block)
            self.logger.info("Metadata values have been correctly validated.")

        except ValueError as e:
            raise ValueError(e)

        # Then populate the attributes of the class
        instance.populate_attr(block)

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
        Utility function for parsing a single exercise.
        Gets the type either from metadata or by parsing <type, var> pattern in case we are inside multiple mode.
        Based on type registry loads the corresponding class and parse methods are loaded.
        """

        t: str = self.metadata.type
        v: str = self.metadata.variation
        type_re = re.compile(r"\s*<([^>]+)>", re.DOTALL)

        # ???
        k = load_metadata(exs)
        if k.ok:
            t, v = k.data[0], k.data[1]

        Handler = get_handler(t)
        instance = Handler(exs)

        if self.mode == Mode.MULTIPLE.value:
            instance.initial_load()
            if instance.type == None or instance.variation == None:
                raise ValueError("Multiple mode detected, but no metadata declaration in individual exercises")
            instance.exercise = type_re.sub("", instance.exercise)

        parse_r = instance.parse_content()
        if not parse_r.ok:
            raise ValueError(parse_r.errors)
        self.content.append(ExerciseContent(exercise=parse_r.content))

    def run(self):
        # Register classes
        load_plugins()

        # Populate mode variable
        self.extract_mode()

        try:

            metadata_r = self.parse_metadata()
            print(metadata_r, type(metadata_r))

            content_r = self.extract_content(self.exercise, self.mode == Mode.MULTIPLE.value)
            for i, exs in enumerate(content_r):
                self.parse_content(exs)
                self.logger.info(f"{i+1} exercise(s) parsed succesfully.")

        except ValueError as e:
            raise ValueError(e)

        self.result = Exercise(mode=self.mode, metadata=self.metadata, exercises=self.content)
        return self.result
