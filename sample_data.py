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

