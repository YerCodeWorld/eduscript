
import re
from typing import List, Optional
from dataclasses import dataclass
from metadata import Metadata
from enums import ExerciseTypes

@dataclass
class FunctionResult:
    ok: bool
    data: Optional[List[str]] = None
    result_string: Optional[str] = None
    errors: Optional[List[str]] = None

def remove_distractors(s) -> FunctionResult:
    """
    Extra feature for #categorize and #matching exercises to add distractors.
    @EXTRA = [value | value | value]
    """

    distractors_re = re.compile(r"@EXTRA\s*=\s*\[(.*?)\]")

    distractors: Optional[List[str]] = None
    match = re.findall(distractors_re, s)

    if match:
        if len(match) > 1:
            return FunctionResult(ok=False, errors=["Found more than one distractors declaration, please have just one existing"])
        values = match[0]
        distractors = [v.strip() for v in values.split("|")]

    removed = distractors_re.sub("", s)
    return FunctionResult(ok=True, data=distractors, result_string=removed, errors=[])

def extract_instructions(s) -> FunctionResult:
    """
    Provided that we will be handle just a single string (meaning no more
    than one exercise sentence), then this function should extract the
    instruction and return it alongside the cleaned text

    it clears some edge-cases that could be assigned to the parse function as well,
    so it's a great helper
    """

    if not "\n" in s:
        return FunctionResult(ok=False, errors=["This text does not have any instructions."])

    ins = s.strip().split("\n")[0]
    p = s.replace(ins, "").strip()

    if ins == "":
        return FunctionResult(ok=False, errors=["No instruction found with any type of content"])

    if ins[0] != "#":
        return FunctionResult(ok=False, errors=["This sentence has no instructions identifier"])

    # Skip '#' instruction indicator
    ins = ins[1:].strip()

    if len(ins) <= 2:
        return FunctionResult(ok=False, errors=["Instruction too short"])

    return FunctionResult(ok=True, data=ins, result_string=p, errors=[])

# Fill blanks has a variation in which this is useful, so that's why it's a helper function
def parse_mcq_pattern(s: str, skip_brackets=False, skip_pipes=False) -> FunctionResult:
    """
    I | am | [a | correct | answer] | and | me | [too!]

    For ordering: Items + distractors
    For blanks:   options + correct options
    For MCQ:      options + correct options
    """
    brackets_re = re.compile(r"\[(.*?)\]")

    if not skip_pipes and not ("|" in s or len(s.split("|")) <= 2):
        return FunctionResult(ok=False, errors=["No valid options in the provided string"])

    matches = brackets_re.findall(s)
    if not skip_brackets and not (matches or all(match == "" for match in matches)):
        return FunctionResult(ok=False, errors=["No valid correct options in a provided string"])

    s = brackets_re.sub("", s)
    correct_options = []
    for m in matches:
        for val in m.split("|"):
            correct_options.append(val.strip())

    options = [item.strip() for item in s.split("|") if item.strip()]
    if not all(val.strip() for val in options):
        return FunctionResult(ok=False, errors=["The string provided do seems to have options, but they are all empty."])

    # print(correct_options, options)
    return FunctionResult(ok=True, data=correct_options, result_string=options)

def load_metadata(exs: str):

    def get_metadata(exs: str) -> list[str]:
        # Syntax: <type, variation>
        type_re = re.compile(r"\s*<([^>]+)>", re.DOTALL)

        m = type_re.search(exs)
        if not m:
            raise ValueError("No metadata declaration inside of exercise on multiple mode")

        if "," not in m.group(1) or len(m.group(1).split(",")) != 2:
            raise ValueError("Incorrect syntax inside metadata declaration")

        exs_type, variation = m.group(1).split(",")

        exs_type = Metadata.canonical_enum(ExerciseTypes, exs_type)
        if not exs_type:
            raise ValueError("Invalid exercise type found on metadata declaration")

        if not variation.strip():
            raise ValueError("Variation information seems to be empty")

        return [exs_type, variation]

    try:
        r = get_metadata(exs)
        return FunctionResult(ok=True, data=r)

    except ValueError as e:
        # None None ugly hack, but I guess it works fine
        return FunctionResult(ok=False, data=[None, None], errors=[e])
