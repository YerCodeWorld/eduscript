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
    @EXTRA = [blank | white];

"""
mcq_sample = """
# Sit here
Sit here | [Here is your table please have a seat] | Take your place.;

# Do you have a booking?
[Do you have a reservation?] | Are you booked? | What’s your table number?;

# Wait a moment.
Wait one second. | [Could you wait here for a few minutes while we prepare your table?] | Stand there;

# What’s your name?
Give me your name. | [May I have your name please?] | Who are you?;

# This is the menu.
[Here are your menus. Today’s special is grilled salmon.] | Take the menu. | Look at this;

# Follow me.
Walk after me. | [Please follow me. I’ll take you to your table.] | Come here.;

# We are full.
[I’m sorry we are fully booked at the moment.] | There’s no space. | All the tables are busy;

# Come in
Enter now | [Welcome to our restaurant! Please come in.] | You can go inside.;

# What do you want?
What can I do for you? | [How can I help you today?] | Tell me what you want.;

# There’s a problem.
[I’m sorry for the inconvenience. Let me see what I can do for you.] | Something’s wrong. | We have a problem.;
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

categorize_sample = """

ANIMALS = Lion | Chicken | Tiger | Dog | Cat;
FRUITS = Banana | apple | Pear | Orage | Dragon Fruit;
COLORS = Blue | Red | White | Green | Black;
CLASSROOM = Pencil | Notebook | School Bag | Computer | Eraser;

"""

select_sample = """
# Select all the verbs
I [am] someone who [knows] when everything
[turns] bad and destiny [decides] it's time
for trouble.;

# Select all the adjectives
We [never] considered such an [amazing] person
to be this [bad]. What could actually have been
just a [smooth] step in the middle turned out
to be [horrific].;
"""

blanks_sample = """
# Your mother's son
I *am|'m* your *brother|bro*;
He *is|'s* your *sister|sis*;

# Verb to be and fa____
We *are|'re* a *family|fam*;

# The place you go to study
Sc*hool*;

Some people *eat|[think | believe]|sleep* that we are together;
"""

