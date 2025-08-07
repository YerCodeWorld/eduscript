import re
from enums import *

# map key-enum

# the plan is to call from a main function in parser.py
"""
Using an instance, we do:

- Have a main flow function that:
-- extracts the metadata block (instance.extract_metadata_blocks())
-- validates keys (instance.validate_metadata_keys())
-- validates values (instance.validate_metadata_values())

Once these processes are done, we create the base data using
the properties in the __init()__.

instance.create_base_data() would result in variables like
self.type, self.category, self.style, ..., etc being populated,
and later I would be able to do something like instance.type,
instance.difficulty, etc.

Once these variables are populated I can use the instance of the
class to populate those keys in the JSON to generate.

self.data is supposed to take the exercise to would be sent to
the class via a parameter. self.logger is supposed to save the
print statements or Exceptions found in the processes, although
I just added this by intuition.
"""

class Metadata:

    # missing parameter s for exercise?
    def __init__(self, s):

        self.type = ""
        self.category = ""
        self.difficulty = ""
        self.style = ""
        self.instructions = ""
        self.title = ""
        self.packageId = ""
        self.variation = "original"
        self.is_published = False
        self.logger = []
        self.data = s # would be equal to s

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


    @staticmethod()
    def extract_key_val(pair_str: str) -> tuple[str, str]:
        key, val = pair_str.split("=")
        return key.strip(), val.strip()

    def validate_metadata_keys(self, s):
        data = []

        for i in range(len(s)):
            # we understand this symbol is present in the string, as we cleaned off those that didn't
            key, val = self.extract_key_val(s[i]);

            if ValidMetadataBlock.__contains__(key.strip()):
                data.append(key.strip())
            else:
                print(Exception(f"Key {key} is not a valid metadata field"))
                return False

        required = [i.value for i in RequiredMetadataInfo]
        for field in required:
            if field not in data:
                print(Exception("Missing required fields in the metadata block"))
                return False

        print("Validated all metadata keys!")
        return True

    def validate_metadata_values(s):
        def is_found(enum, val) -> bool:
            # create list of valid types to compare against
            valid_types = [e.value for e in enum]
            if val.lower() in valid_types:
                return True
            return False

        for i in range(len(s)):
            key, val = extract_key_val(s[i]);

            if key == "isPublished":
                if val.lower() not in ["true", "false"]:
                    print(Exception(f"Invalid value for key {key}"))
                    return False
                self.is_published = True if val.lower() == "true" else False
                continue

            if key in data.keys():
                result = is_found(data[key], val)
                if not result:
                    print(Exception(f"Value {val} is not a valid type for key {key}"))
                    return False

            elif len(val) > max_length[key]:
                print(Exception(f"Value of key {key} exceeds the allowed length ({max_length[key]})"))
                return False

            print("All values have been validated!")
            return True

    def extract_metadata_blocks(self):
        found_blocks = re.findall(r"@metadata\s*{(.*?)}", self.data, re.DOTALL)
        if len(found_blocks) > 1:
            return Exception("Error: More than one metadata block found. Just one allowed")

        trimmed_block = [bl.strip().replace("\n", "") for bl in found_blocks]
        single_block = [s.strip() for s in trimmed_block[0].split(";")]

        # remove any extra empty or non-valid value
        cleaned_block = [s for s in single_block if '=' in s and s != ""]
        return cleaned_block

    def create_base_structure():
        pass













is_published: bool = False


def extract_key_val(pair_str: str) -> tuple[str, str]:
    key, val = pair_str.split("=")
    return key.strip(), val.strip()

def extract_metadata_blocks(s) -> []:

    found_blocks = re.findall(r"@metadata\s*{(.*?)}", s, re.DOTALL)
    if len(found_blocks) > 1:
        return Exception("Error: More than one metadata block found. Just one allowed")

    trimmed_block = [bl.strip().replace("\n", "") for bl in found_blocks]
    single_block = [s.strip() for s in trimmed_block[0].split(";")]

    # remove any extra empty or non-valid value
    cleaned_block = [s for s in single_block if '=' in s and s != ""]
    return cleaned_block

def validate_metadata_keys(s) -> {}:

    data = []

    for i in range(len(s)):

        # we understand this symbol is present in the string, as we cleaned off those that didn't
        key, val = extract_key_val(s[i]);

        if ValidMetadataBlock.__contains__(key.strip()):
            data.append(key.strip())
        else:
            print(Exception(f"Key {key} is not a valid metadata field"))
            return False

    required = [i.value for i in RequiredMetadataInfo]
    for field in required:
        if field not in data:
            print(Exception("Missing required fields in the metadata block"))
            return False

    print("Validated all metadata keys!")
    return True

# In order to validate the keys:

"""
- Create proper enum types for each field
--type: ExerciseType
--title: str
--instructions: str
--difficulty: ExerciseDifficulty
--isPublished: bool
--category: ExerciseCategory
--variation: str
--style: DisplayStyle
--packageId: str
"""

# Have a single function that compares the given value against the corresponding
# enum (converted to a list of strings). For non-enumerated values, compare against
# max str length.

# If no errors are found, block has been validated. If a single error is found,
# return an Exception.

def validate_metadata_values(s):

    global data, max_length

    def is_found(enum, val) -> bool:
        # create list of valid types to compare against
        valid_types = [e.value for e in enum]
        if val.lower() in valid_types:
            return True
        return False

    for i in range(len(s)):
        key, val = extract_key_val(s[i]);

        if key == "isPublished":
            if val.lower() not in ["true", "false"]:
                print(Exception(f"Invalid value for key {key}"))
                return False
            is_published = True if val.lower() == "true" else False
            continue

        if key in data.keys():
            result = is_found(data[key], val)
            if not result:
                print(Exception(f"Value {val} is not a valid type for key {key}"))
                return False

        elif len(val) > max_length[key]:
            print(Exception(f"Value of key {key} exceeds the allowed length ({max_length[key]})"))
            return False

    print("All values have been validated!")
    return True

def create_base_data():
    pass

