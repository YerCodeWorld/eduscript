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
    def canonical_enum(enum_cls, val: str) -> str:
        """
        Validate a fiven enum value

        :params:  enum_cls    enum to check against
        :param:   val         current key val to validate
        """
        try:
            return enum_cls(val.strip().lower()).value
        except ValueError:
            print(f"Invalid enum value '{val}' for {enum_cls.__name__}")
            raise

    def extract_metadata_blocks(self):
        found = re.findall(r"@metadata\s*.*?{(.*?)}", self.data, re.DOTALL)

        if not found:
            self.logger.error("No @metadata block found.")
            return None

        if len(found) > 1:
            self.logger.error("More than one metadata block found. Just one allowed")
            return None

        removed_newlines = found[0].strip().replace("\n", "")
        fields = [f.strip() for f in removed_newlines.split(";")]

        # remove any extra empty or non-valid value
        filtered = []
        for f in fields:
            if '=' in f and f.strip():
                filtered.append(f)
            else:
                self.logger.warning(f"Found empty or uncomplete metadata field: {f}")

        self.logger.info("Extracted metadata block succesfully")
        return filtered

    def validate_metadata_keys(self, fields):
        valid_keys = {e.value for e in ValidMetadataBlock}
        required   = {e.value for e in RequiredMetadataInfo}
        seen = set()

        for field in fields:
            # we understand this symbol is present in the string, as we cleaned off those that didn't
            key, _ = self.extract_key_val(field);
            key = key.strip()

            if key not in valid_keys:
                self.logger.error(f"Key '{key}' is not a valid metadata field")
                return False

            if key in seen:
                self.logger.warning(f"Duplicate key '{key}' – last value will be used.")
            seen.add(key)

        missing = required - seen
        if missing:
            self.logger.error("Missing required fields in the metadata block")
            return False

        self.logger.info("Validated all metadata keys!")
        return True

    def validate_metadata_values(self, fields):

        for field in fields:
            key, val = self.extract_key_val(field);
            key = key.strip()
            val = val.strip()

            if key == "isPublished":
                continue

            if key in self.enums:
                val = self.canonical_enum(self.enums[key], val)

            # enforce max length for free-text fields
            if key in self.max_length and len(val) > self.max_length[key]:
                v = self.strip_quotes(val)
                if len(v) > self.max_length[key]:
                    self.logger.error(
                        f"Value too long for '{key}' ({len(v)} > {self.max_length[key]})"
                    )
                    return False

            self.logger.info("All values have been validated!")
            return True

    def create_base_structure(self, fields):

        attr_map = {
            "type": "type",
            "difficulty": "difficulty",
            "style": "style",
            "variation": "variation",
            "instructions": "instructions",
            "title": "title",
            "category": "category",
            "packageId": "packageId"
        }

        for field in fields:
            key, val = self.extract_key_val(field)
            key, val = key.strip(), self.strip_quotes(val)

            if key == "isPublished":
                # wrongly writing the value would result on it not being published, but it is not warned
                self.is_published = (val.lower() == "true")
                continue

            if key in self.enums:
                val = self.canonical_enum(self.enums[key], val)

            setattr(self, attr_map[key], val)





