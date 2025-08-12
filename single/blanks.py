import re
from typing import List, Optional
from pydantic import BaseModel
from single.helpers import extract_instructions, parse_mcq_pattern
from src.models import ParseResult, Blank, BlanksContent, BlanksWrapper

class Blanks:

    def __init__(self, exercise):
        self.exercise = exercise

    @staticmethod
    def parse_blanks_pattern(s):
        """
        Search for blanks using a pointer approach just because it's different and looks dope
        ... (She *takes* a shower and *goes* to work.)
        Also it's useful no? I mean * are not something you can pair like brackets
        """

        blanks: List[str] = []
        pointer = 0
        current_blank = []
        in_blank = False

        while pointer < len(s):

            char = s[pointer]
            # Avoiding some possible dumb case that someone mistakenly writtes consecutive * chars
            if char == "*" and pointer != 0 and char == s[pointer-1]:
                pointer += 1
                continue

            if char == "*":
                if in_blank:
                    blanks.append(''.join(current_blank))
                    current_blank = []
                    in_blank = False
                else:
                    in_blank = True
            elif in_blank:
                current_blank.append(char)

            pointer += 1

        return blanks


    def parse_content(self):

        items: List[BlanksContent] = []
        chunks = [ch.strip() for ch in self.exercise.split(";")]

        for ch in chunks:

            if ch == "":
                continue

            if "*" not in ch:
                return ParseResult(ok=False, errors=["The following sentence does not have any valid blanks content: ", ch])

            # Edge-cases helper
            ch = ch.replace("**", "*")
            if ch.count("*") % 2 != 0:
                return ParseResult(ok=False, errors=["Irregular sets of '*' characters. Make sure each of them is matched accordingly. Consecutive '*' chars are counted as one."])

            ins: str = ""
            sentence: str = ""
            blanks: List[Blank] = []

            result = extract_instructions(ch)
            if result.ok:
                ins = result.data
                ch = result.result_string.replace("\n", " ")

            extracted_blanks = self.parse_blanks_pattern(ch)
            if not all(b.strip() for b in extracted_blanks):
                return ParseResult(ok=False, errors=[f"The following sentence has empty or invalid blanks: {ch}"])

            seen = set()

            for i, blank in enumerate(extracted_blanks):

                # avoiding errors for repetead blanks in a sentence, although no exercise should ever be like this
                if blank not in seen:
                    ch = ch.replace(blank, "___")
                seen.add(blank)

                # Omitting both checks results in 0 rules-violation errors
                r = parse_mcq_pattern(blank, True, True)
                blanks.append(Blank(position = i+1, correct_options=r.data, options=r.result_string))

            # The 'ch' reassignments in fro loop above actually mutate it with each new blank.
            sentence = ch
            items.append(BlanksContent(sentence=sentence, blanks = blanks, instruction=ins))

        return ParseResult(ok=True, content=BlanksWrapper(content=items))

    def validate_blanks(self, data):
        errors = []


        return errors == 0
