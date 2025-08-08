exercise = """

    apple = red;
    pear   = green;
    grape  = purple;
    banana = yellow;
    = [blank, white];


"""


exercise = exercise.replace("\n", "")
exercise = exercise.strip().split(";")
exercise = [sn.strip() for sn in exercise if "=" in sn and sn.strip()]

for sn in exercise:
    left, right = sn.strip().split("=", 1)
    left, right = left.strip(), right.strip()

    if left == "":
        print("Extra answers: ", right)
    else:
        print(f"Left: {left} - Right: {right}")




