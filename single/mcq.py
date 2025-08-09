import re
from pydantic import BaseModel
from dataclasses import dataclass
from typing import List, Optional


class MCQcontent(BaseModel):
    question: str
    options: List[str]
    correctOptions: List[str]
    # adding now, but logic for this will be relevant come updates on
    points: Optional[List[int]]

class MCQwrapper(BaseModel):
    content: List[MCQcontent]

@dataclass
class ParseResult:
    ok: bool
    content: Optional[MCQwrapper] = None
    error: Optional[str] = None


class MCQ:

    def __init__(self, exercise):

        self.data = exercise
        self.distractor_re = re.compile(r"\[(.*?)\]")
        self.errors = {
            "short_instructions": "Instruction too short, did you really mean this? Consider adding some extra non-distracting characters if so.",
            "missing_correct": "No correct answers found for {0} - {1} Invalid sentence sequence. ",
            "genera_invalid": f"The following question {0} - {1} is not valid. Missing either instruction or options",
            "empty_sentence": "Empty sentence found. Did you create a sentence with correct answers [...] only?"
        }


    def parse_mcq(self) -> ParseResult:

        # CONVERED EDGE-CASES

        # 1 - No instructions '#' found
        # 2 - Instructions too short cases
        # 3 - No options found
        # 4 - No correct answers or empty [] correct answers brackets
        # 5 - Sentence normalization case


        items: List[MCQcontent] =  []
        chunks = [c.strip() for c in self.data.split(";")]

        # Using enumerate this time
        for i, sn in enumerate(chunks):

            if sn == "":
                continue

            if not "|" in sn:
                return ParseResult(ok=False, error=f"Error, no options found in {i} - {sn}")

            question: str = ""
            options: List[str] = []
            correct_options: List[str] = []

            # instructions are MANDATORY in this exercise type, unlike ordering for example
            if not "\n"  in sn:
                return ParseResult(ok=False, error=errors["genera_invalid"].format(i+1, sn))

            if sn.split("\n")[0].startswith("#"):
                lines = sn.split("\n")

                if len(lines[0].strip()) > 3:
                    question = lines[0][1:].strip()
                    sn = ' '.join(lines[1:])
                else:
                    return ParseResult(ok=False, error=errors["short_instructions"])
            else:
                return ParseResult(ok=False, error=errors["empty_sentence"])


            matches = self.distractor_re.findall(sn)
            if matches and not all(match == "" for match in matches):
                correct_options = matches
            else:
                return ParseResult(ok=False, error=errors["missing_correct"].format(i+1, sn))

            sn = self.distractor_re.sub("", sn)

            if sn.replace("|", "").strip() == "":
                return ParseResult(ok=False, error=errors["empty_sentence"])

            sn = [s.strip() for s in sn.split("|")]
            sn = [s for s in sn if s.strip()]

            items.append(MCQcontent(question=question, options=sn, correctOptions=correct_options, points=[]))

        return ParseResult(ok=True, content=MCQwrapper(content=items), error="")

    def validate_mcq() -> bool:
        errors: List[str] = []



        return len(errors) == 0



