import re
from dataclasses import dataclass
from logger_base import get_logger
from pydantic import BaseModel
from typing import List, Optional

# Pair type
class Pair(BaseModel):
    left: str
    right: str

# Matching Content Type
class MatchingContent(BaseModel):
    pairs: List[Pair]
    distractors: Optional[List[str]] = None

@dataclass
class ParseResult:
    ok: bool
    value: Optional[MatchingContent] = None
    error: str = None

# Constraints
"""

    apple = red;
    pear :: green;
    grape  = purple;
    banana = yellow;
    = [blank, white];

"""
"""
Model

{
    "left": "",
    "right": ""
}
"""

# 1 - = or :: separate the left and right sides
# 2 - empty left and line.startWith("=") indicates distractors (brackets, comma-separated)

class Matching:

    def __init__(self, content: str):

        self.content = content
        self._distractors_re = re.compile(r"^\s*=\s*\[(.*?)\]\s*$")
        self.logger = get_logger(self.__class__.__name__)

    def parse_matching(self) -> ParseResult:

        pairs: List[Pair] = []
        distractors: Optional[List[str]] = None

        chunks = [c.strip() for c in self.content.split(";") if c.strip()]

        for sn in chunks:

            m = self._distractors_re.match(sn)
            if m:
                vals = [v.strip() for v in m.group(1).split(",") if v.strip()]
                distractors = vals or None
                self.logger.info(f"Distractors: {distractors}")
                continue

            has_eq = '=' in sn
            has_colon = '::' in sn

            if sn.count("=") > 1 or sn.count("::") > 1:
                return ParseResult(ok=False, error=f"More than one separator found in a single sentence: {sn!r}")

            if has_eq and has_colon:
                return ParseResult(ok=False, error=f"Ambiguous separators in: {sn!r}")
            if not (has_eq or has_colon):
                return ParseResult(ok=False, error=f"No separators found in: {sn!r}")

            sep = '::' if has_colon else '='

            left, right = [p.strip() for p in sn.split(sep, 1)]
            if not (left and right):
                return ParseResult(ok=False, error=f"Incomplete pair in: {sn!r}")

            pairs.append(Pair(left=left, right=right))

        return ParseResult(ok=True, value=MatchingContent(pairs=pairs, distractors=distractors), error=[])

    def validate_matching(self, content: MatchingContent) -> bool:
        errors = []

        # min/max length logic
        # duplicated lines logic
        # validate right and left items
        # validate extra answers

        return len(errors) == 0


"""
VALIDATOR

function validateMatchingContent(content: MatchingContent): ValidationResult {
    const errors: string[] = [];

    // Check basic structure
    if (!content.pairs || !Array.isArray(content.pairs)) {
        errors.push(ErrorMessages.missingContent('pairs'));
        return { isValid: false, errors };
    }

    // Validate pair count
    const minError = validateMinLength(content.pairs, 2, 'pairs');
    if (minError) errors.push(minError);

    const maxError = validateMaxLength(content.pairs, 20, 'pairs');
    if (maxError) errors.push(maxError);

    // Track items to check for duplicates
    const leftItems = new Set<string>();
    const rightItems = new Set<string>();

    // Validate each pair
    content.pairs.forEach((pair, index) => {
        const pairNum = index + 1;

        // Validate left item
        if (!pair.left || typeof pair.left !== 'string') {
            errors.push(`Pair ${pairNum} is missing left item`);
        } else {
            const leftLengthError = validateStringLength(pair.left, 1, 200, `Left item in pair ${pairNum}`);
            if (leftLengthError) errors.push(leftLengthError);

            // Check for duplicates
            if (leftItems.has(pair.left.toLowerCase())) {
                errors.push(`Duplicate left item "${pair.left}" in pair ${pairNum}`);
            } else {
                leftItems.add(pair.left.toLowerCase());
            }
        }

        // Validate right item
        if (!pair.right || typeof pair.right !== 'string') {
            errors.push(`Pair ${pairNum} is missing right item`);
        } else {
            const rightLengthError = validateStringLength(pair.right, 1, 200, `Right item in pair ${pairNum}`);
            if (rightLengthError) errors.push(rightLengthError);

            // Check for duplicates
            if (rightItems.has(pair.right.toLowerCase())) {
                errors.push(`Duplicate right item "${pair.right}" in pair ${pairNum}`);
            } else {
                rightItems.add(pair.right.toLowerCase());
            }
        }

        // Validate optional hint
        if (pair.hint) {
            const hintError = validateStringLength(pair.hint, 1, 200, `Hint for pair ${pairNum}`);
            if (hintError) errors.push(hintError);
        }
    });

    // Validate randomize setting
    if (content.randomize !== undefined && typeof content.randomize !== 'boolean') {
        errors.push('Randomize setting must be a boolean');
    }

    // Validate extra answers if present
    if (content.extraAnswers) {
        if (!Array.isArray(content.extraAnswers)) {
            errors.push('Extra answers must be an array');
        } else {
            content.extraAnswers.forEach((answer, index) => {
                if (typeof answer !== 'string' || !answer.trim()) {
                    errors.push(`Extra answer ${index + 1} must be a non-empty string`);
                } else {
                    const extraAnswerError = validateStringLength(answer, 1, 200, `Extra answer ${index + 1}`);
                    if (extraAnswerError) errors.push(extraAnswerError);
                }
            });
        }
    }

    return {
        isValid: errors.length === 0,
        errors
    };
}
"""
