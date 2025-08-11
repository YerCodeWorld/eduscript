from metadata import Metadata
from single.matching import Matching
from single.ordering import Ordering
from single.mcq import MCQ
from single.categorize import Categorize
from single.select import Select
from single.blanks import Blanks
from sample_data import *

def metadata():
    instance = Metadata(data)
    result = instance.extract_metadata_blocks()

    if not result:
        return

    if not instance.validate_metadata_keys(result):
        return

    if not instance.validate_metadata_values(result):
        return

    instance.create_base_structure(result)

    # ✅ Access instance attributes like this
    # print(instance.type)
    # print(instance.difficulty)
    # print(instance.style)
    # print(instance.category)
    # print(instance.title)

    # we need to either append to some JSON or create a data structure

def content():
    instance = Blanks(blanks_sample)
    result = instance.parse_blanks()
    if result.ok:
        print(result.content.model_dump())
    else:
        print(result.errors)
        # is_valid = instance.validate_matching(result.value)
        # if not is_valid:
        #    return

# Process might look like this:

"""
1 - Check if MODE = dynamic
2 - Call corresponding process stack

If static

3 - Parse Metadata
4 - Based on info, use corresponding parser
5 - Validate exercise
6 - If no errors, return result model dump
"""
def main():
    content()

main()

