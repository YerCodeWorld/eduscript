import re

exercise = """
#
I | am | your | brother

;

# We | are | not | a | family | [here, there];

# Most famous programming word
Hello, world!;

Never;
I | love | you | [sleep];
"""

# Constraints

"""
Model

{
    "instruction": "",
    "items": [""],
    "image": "",
    "distractors": [""]
}
"""

# 1 - Pipe separated indicate chunks
# 2 - Non-pipe separated indicate Every char is a value. Spaces are special cases
# 3 - if brackets [] found populate distractors
# 4 - # indicates sentence instruction population

chunks = [c.strip() for c in exercise.split(";")]
distractor_re = re.compile(r"\[(.*?)\]")

for sn in chunks:

    ins = None
    distractors = None
    words = []

    if ("#" and "\n") in sn:
        sn = sn.split("\n")
        ins = sn[0][1:].strip()
        sn = sn[1]

    m = distractor_re.findall(sn)
    if m:
        vals = [v for v in m]
        distractors = vals or None

    words = sn.split("\")


