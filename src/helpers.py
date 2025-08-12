import re
from metadata import Metadata
from enums import ExerciseTypes

def extract_type(s):
    # Syntax: <type, variation>
    type_re = re.compile(r"\s*<([^>]+)>", re.DOTALL)

    m = type_re.search(s)
    if not m:
        return ValueError("No metadata declaration inside of exercise on multiple mode")

    if "," not in m.group(1) or len(m.group(1).split(",")) != 2:
        return ValueError("Incorrect syntax inside metadata declaration")

    exs_type, variation = m.group(1).split(",")

    exs_type = Metadata.canonical_enum(ExerciseTypes, exs_type)
    if not exs_type:
        return ValueError("Invalid exercise type found on metadata declaration")

    if not variation.strip():
        return ValueError("Variation information seems to be empty")

    return exs_type, variation
