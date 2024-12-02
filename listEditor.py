# Created: 12-2-2024
# Last updated: 12-2-2024
# Alexander Myska, Oliver Strauss, and Brandon Knautz

# This file rewrites the word database to remove some words we don't want in the database.
# Mainly words with non-alphabetic characters (like Q-TIP) or expletives.

defaultLetters = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")
defaultSizes = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "11")

def main(letters : tuple = defaultLetters, sizes : tuple = defaultSizes):
    for letter in letters:
        for size in sizes:
            filepath = f"Words/{letter}-Words/words_{size}.txt"
            try:
                f = open(filepath, "r")
                rewrite = ""
                while True:
                    word = f.readline()
                    if not (word):
                        break

                    word = word.strip()
                    if (check(word)):
                        if (rewrite != ""):
                            rewrite += "\n"
                        rewrite += word

                f.close()
                f = open(filepath, "w")
                f.write(rewrite)
                f.close()
            except FileNotFoundError:
                print(f"File '{filepath}' does not exist. Continuing...")

    print(f"All file rewrites successful.")

# Current checks:
# 1 - All words must be only alphabetic characters
def check(word : str) -> bool:
    if not (word.isalpha()):
        return False

    return True

if (__name__ == "__main__"):
    main()