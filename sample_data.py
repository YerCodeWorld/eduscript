# This assumes your DSL is stored in a string
metadata_sample = """
@metadata () {
  type= blanks;
  title = myLife;
  difficulty=BEGINNER;
               difficulty = upper_bEginneR;
  isPublished = true;category = VOCABULARY;
  style = nature;

}
"""

matching_sample = """

    apple = red;
    pear :: green;
    grape  = purple;
    banana = yellow;
    = [blank, white];

"""

# A properly typed exercise
ordering_sample = """

# Don't get distracted!
She  | takes | a   | shower | in | the | morning | [forgets] | [likes];
they | do    | the | homework;
I    | watch | [cooking] | tv | in | the| afternoon;
we   | go    |   to work | at |seven;

# Can you brush that!??
He   | brushes | his   | teeth | [bed] | with | colgate;

they | have    | lunch | together;
"""
#
