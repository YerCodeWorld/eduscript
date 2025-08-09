from metadata import Metadata
from single.matching import Matching
from single.ordering import Ordering
from sample_data import ordering_sample

# This assumes your DSL is stored in a string
data = """
@metadata () {
  type= blanks;
  title = myLife;
  difficulty=BEGINNER;
               difficulty = upper_bEginneR;
  isPublished = true;category = VOCABULARY;
  style = nature;

}

@content {

}
"""


match = """

    apple = red;
    pear :: green;
    grape  = purple;
    banana = yellow;
    = [blank, white];

"""

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
    instance = Ordering(ordering_sample)
    result = instance.parse_ordering()
    if result.ok:
        print(result.content.model_dump())
        # is_valid = instance.validate_matching(result.value)
        # if not is_valid:
        #    return


def main():
    content()

main()

