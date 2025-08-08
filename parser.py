from metadata import Metadata

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
    pass

def main():
    metadata()

main()

