from metadata import Metadata
from single.matching import Matching
from single.ordering import Ordering
from single.mcq import MCQ
from sample_data import ordering_sample, mcq_sample

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
    instance = MCQ(mcq_sample)
    result = instance.parse_mcq()
    if result.ok:
        print(result.content.model_dump())
        # is_valid = instance.validate_matching(result.value)
        # if not is_valid:
        #    return


def main():
    content()

main()

