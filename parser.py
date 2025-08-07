
from metadata import Metadata  # Assuming the class is in metadata.py

# This assumes your DSL is stored in a string
data = """
@metadata{
  type = blanks;
  title = myLife;
  difficulty = upper_beginner;
  isPublished = true;
  category = VOCABULARY;
}
"""

def main():
    instance = Metadata(data)
    result = instance.extract_metadata_blocks()

    if not instance.validate_metadata_keys(result):
        return
    if not instance.validate_metadata_values(result):
        return

    instance.create_base_structure()

    # ✅ Access instance attributes like this
    print(instance.type)
    print(instance.difficulty)

main()
