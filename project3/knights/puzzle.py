from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
Astatement = And(AKnave,AKnight)
knowledge0 = And(
    Not(
        Biconditional(
        AKnave,
        AKnight
        )
    ),

    Biconditional(
        Not(Astatement),
        AKnave
    ),

    # TODO
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
Astatement = And(AKnave,BKnave)
knowledge1 = And(
    Not(
        Biconditional(
        AKnave,
        AKnight
        )
    ),

    Not(
        Biconditional(
        BKnave,
        BKnight
        ),

    ),

    Biconditional(
        Not(Astatement),
        AKnave
    )

    # TODO
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
Astatement = Biconditional(AKnave,BKnave)
Bstatement = Not(Biconditional(AKnave,BKnave))
knowledge2 = And(
    Not(
        Biconditional(
        AKnave,
        AKnight
        )
    ),

    Not(
        Biconditional(
        BKnave,
        BKnight
        )
    ),

    Biconditional(
        Astatement,
        AKnight
    ),

    Biconditional(
        Bstatement,
        BKnight
    )

    # TODO
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
Astatement = Or(AKnave,AKnight)
Bstatement2 = CKnave
Bstatement1 = BKnave
Cstatement = AKnight
knowledge3 = And(

    Not(
        Biconditional(
        AKnave,
        AKnight
        )
    ),

    Not(
        Biconditional(
        BKnave,
        BKnight
        )
    ),

    Not(
        Biconditional(
        CKnave,
        CKnight
        )
    ),

    Biconditional(
        Astatement,
        AKnight
    ),

    Biconditional(
        Bstatement1,
        AKnight
    ),

    Biconditional(
        Bstatement2,
        BKnight
    ),

    Biconditional(
        Cstatement,
        CKnight
    )
    # TODO
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:

                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
