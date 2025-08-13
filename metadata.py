import re
from enums import *
from logger_base import get_logger

class Metadata():

    # missing parameter s for exercise?
    def __init__(self, s):

        self.data = s # would be equal to s
        self.logger = get_logger(self.__class__.__name__)

        self.type = ""
        self.category = ""
        self.difficulty = ""
        self.style = ""
        self.instructions = ""
        self.title = ""
        self.packageId = ""
        self.variation = "original"
        self.is_published = False

        self.metadata_re = re.compile(r"@metadata\s*.*?{(.*?)}", re.DOTALL)

        self.enums = {
            "type": ExerciseTypes,
            "category": ExerciseCategory,
            "difficulty": ExerciseDifficulty,
            "style": DisplayStyle
        }

        # map key-enum val
        self.max_length = {
            "instructions": MaxValuesLength.INSTRUNCTIONS.value,
            "title": MaxValuesLength.TITLE.value,
            "style": MaxValuesLength.STYLE.value,
            "variation": MaxValuesLength.VARIATION.value,
            "packageId": MaxValuesLength.PACKAGEID.value
        }

    @staticmethod
    def extract_key_val(pair_str: str) -> tuple[str, str]:
        key, val = pair_str.split("=", 1)
        return key.strip(), val.strip()

    @staticmethod
    def strip_quotes(s: str) -> str:
        s = s.strip()
        return s[1:-1] if (len(s) >= 2 and s[0] in "'\"" and s[-1] == s[0]) else s

    @staticmethod
    def canonical_enum(enum_cls, val: str):
        """
        Validate a fiven enum value

        :params:  enum_cls    enum to check against
        :param:   val         current key val to validate
        """
        try:
            return enum_cls(val.strip().lower()).value
        except ValueError as e:
            raise ValueError(f"Invalid enum value '{val}' for {enum_cls.__name__}")

    def remove_metadata_block(self, s):
        return self.metadata_re.sub("", s)

    def get_metadata_block(self):
        m = re.findall(self.metadata_re, self.data)

        if not m:
            raise ValueError("No @metadata block found.")

        if len(m) > 1:
            raise ValueError("More than one metadata block found. Just one allowed")

        return [field.strip() for field in m[0].split(";") if '=' in field and field.strip()]

    def validate_keys(self, fields: list[str]) -> None:

        valid_keys = {e.value for e in ValidMetadataBlock}
        required   = {e.value for e in RequiredMetadataInfo}

        seen = set()

        for f in fields:
            # we understand this symbol is present in the string, as we cleaned off those that didn't
            key, _ = self.extract_key_val(f);
            key = key.strip()

            if key not in valid_keys:
                raise ValueError(f"Key '{key}' is not a valid metadata field")

            if key in seen:
                self.logger.warning(f"Duplicate key '{key}' – last value will be used.")

            seen.add(key)

        missing = required - seen
        if missing:
            raise ValueError("Missing required fields in the metadata block")

    def validate_values(self, fields: list[str]) -> None:

        for f in fields:

            key, val = self.extract_key_val(f);
            key, val = key.strip(), val.strip()

            if key == "isPublished":
                continue

            if key in self.enums:
                try:
                    self.canonical_enum(self.enums[key], val)
                except ValueError as e:
                    return e

            # enforce max length for free-text fields
            if key in self.max_length and len(val) > self.max_length[key]:
                v = self.strip_quotes(val)

                if len(v) > self.max_length[key]:
                    raise ValueError(f"Value too long for '{key}' ({len(v)} > {self.max_length[key]})")

            if not val.strip() or len(val) < 2:
                raise ValueError(f"Value too short or non-existent for '{key}': {val}")

    def populate_attr(self, fields: list[str]) -> None:
        """
        Taken that using an outer function the fields have being validated and filtered,
        this function populates the attributes of the class to later be used to create a model_dump
        """

        for f in fields:
            key, val = self.extract_key_val(f)
            key, val = key.strip(), self.strip_quotes(val)

            if key == "isPublished":
                # wrongly writing the value would result on it not being published, but it is not warned
                self.is_published = (val.lower() == "true")
                continue

            if key in self.enums:
                val = self.canonical_enum(self.enums[key], val)

            setattr(self, key, val)





