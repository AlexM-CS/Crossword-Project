# Created: 9-30-2024
# Last updated: 10-15-2024
# Alexander Myska, Oliver Strauss, and Brandon Knautz

# This file handles all file access and writing done by the project.

# External imports:
import os
import random

# When running from here, use these imports:
# from Cell import LetterCell

# When running from main, use these imports:
from BackEnd.Cell import LetterCell

def convertBase() -> None:
    """
    Credit: Oliver Strauss
    Was used to convert a raw database (githubList) into a structured file directory (Words)
    @return: None
    """
    alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']

    for letter in alph:
        with open("../githubList/sortedGithubList.txt", "r") as file:
            content = file.read()  # Read the entire content
            words = content.split()  # Split the content into words

        # Base directory for the letters
        base_directory = "Words"

        # Create the base directory if it doesn't exist
        try:
            os.mkdir(base_directory)
            print(f"Base directory '{base_directory}' created.")
        except FileExistsError:
            print(f"Base directory '{base_directory}' already exists.")

        # Create a dictionary to hold words by their starting letters
        words_by_letter = {letter : [] for letter in alph}

        # Organize words by their starting letters
        for word in words:
            first_letter = word[0].lower()  # Get the first letter in lowercase
            if first_letter in words_by_letter:
                words_by_letter[first_letter].append(word)

        # Create directories and write words to files based on their starting letters
        for letter in alph:
            # Create a directory for the current letter
            letter_directory = os.path.join(base_directory, f"{letter}-Words")
            try:
                os.mkdir(letter_directory)
                print(f"Directory '{letter_directory}' created.")
            except FileExistsError:
                print(f"Directory '{letter_directory}' already exists.")

            # Create a dictionary to hold words by their lengths for the current letter
            words_by_length = {}

            # Organize words by their lengths for the current letter
            for word in words_by_letter[letter]:
                word_length = len(word)
                if word_length not in words_by_length:
                    words_by_length[word_length] = []
                words_by_length[word_length].append(word)

            # Write words grouped by length into separate files
            for length, words_list in words_by_length.items():
                # Change the file path to correctly save in the letter-specific folder
                file_path = os.path.join(letter_directory, f"words_{length}.txt")
                with open(file_path, 'w') as word_file:
                    word_file.write('\n'.join(words_list))  # Write all words, separated by newlines
                    print(f"File '{file_path}' created with {len(words_list)} words of length {length}.")

def findWord(letterCells) -> tuple[list[str], bool]:
    """
    Credit: Oliver Strauss, Alexander Myska
    Takes in a list of Cells, and finds a word for them
    @param letterCells: the list of cells to get a word for
    @return: a tuple with a string and boolean. The boolean tells if a word was found
    """

    # List of tuples containing an index and a possible letter
    indices = []

    # Only search for words the same length as the list
    wordLength = len(letterCells)

    # Initializes indices
    for i, cell in enumerate(letterCells):
        indices.append((i, cell.letter))

    # The list of words that meet our requirements
    finalWords = []

    # filePath = "../Words/" # Use this path when testing from here
    filePath = "Words/" # Use this path when testing from main

    # This flag lets use know if a word was found or not
    flag = False

    # If the first letter is filled, we need to look in a specific file:
    if (indices[0][1] != ""):
        # Makes filepath according to first letter
        filePath += f"{indices[0][1].lower()}-Words/words_{wordLength}.txt"
        try:
            finalWords, flag = genWord(filePath, indices)

        except FileNotFoundError:
            print("File not found")
            return [], flag

    else: # Otherwise, we can search in any file:
        # List used to see if letter was already checked
        alph = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
                "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        # Iterate until we get a working list, or until the alphabet is empty
        while (alph) and not (flag):
            random_letter = random.choice(alph)
            alph.remove(random_letter)

            # Makes filepath
            filePath += f"{random_letter.lower()}-Words/words_{wordLength}.txt"
            try:
                # Generate a word from this file:
                finalWords, flag = genWord(filePath, indices)

            except FileNotFoundError:
                # If the file does not exist, skip over it
                continue

    # Returns list of words and boolean determining if words were found
    return finalWords, flag

def genWord(filePath, indices):
    """
    Finds a random word that meets specific criteria
    @param filePath: the filepath to search for a word in
    @param indices:
    @return:
    """
    # Credit: Oliver Strauss
    #List of words found
    finalWords = []

    with open(filePath, 'r') as file:
        # Split the content by newlines
        words = file.read().splitlines()

    for i in range(len(words)):

        flag = True
        for indexs in indices:
            # If wordcell is blank, skip checking if it matches word
            if indexs[1] == '':
                continue
            # If not, check if letters align. If not, word won't be added
            if words[i][indexs[0]].lower() != indexs[1].lower():

                flag = False
        #If words valid it gets added here
        if flag:
            finalWords.append(words[i])

    #flag set to true if word was found
    flag = len(finalWords) > 0

    #Returns list of valid words and flag determining if something was found or not
    return finalWords , flag

def main():

    convert_githubList(35, 15, [" ", "," "'"])
    #quit()

    #Test code for findWord





   # convertBase()


    #Cell4 = LetterCell(4, 0)

    #Cell5 = LetterCell(5, 0)
    #Cell5.setLetter("a")
    #Cell6 = LetterCell(6, 0)
   # Cell7 = LetterCell(7, 0)
    #Cell8 = LetterCell(8, 0)
    #Cell9 =LetterCell(9, 0)
    #Cell9.setLetter("r")


   # Cell5 = LetterCell(4, 0)
    #Cell5.setLetter("N")
    wordlist = [LetterCell(0,0),LetterCell(0,0),LetterCell(0,0),LetterCell(0,0),LetterCell(0,0),LetterCell(0,0),LetterCell(0,0),LetterCell(0,0)]

    words,wordCheck =  findWord(wordlist)

    print(words)
    print(wordCheck)

def notify(word: str, disallowed: str, alwaysRemove = True, alwaysModify = True):
    if (alwaysRemove):
        return ""
    if (alwaysModify):
        return modify(word, disallowed)
    print()
    print("Found a word '" + word + "' that contains the disallowed character '" + disallowed + "'.")
    print("Press 1 to skip writing this word.")
    print("Press 2 to write this word anyway.")
    print("Press 3 to modify this word before writing.")
    choice = input("Input: ")

    while (choice != '1' and choice != '2' and choice != '3'):
        print("Invalid input.")
        choice = input("Input: ")

    print()

    if (choice == '1'):
        return word
    elif (choice == '2'):
        return ""
    elif (choice == '3'):
        return modify(word, disallowed)

def modify(word: str, disallowed: str):
    newWord = ""
    for letter in word:
        if letter == disallowed:
            continue
        newWord += letter
    return newWord

def convert_githubList(requiredScore: int, lengthCap: int, disallowed: list):
    database = open("../githubList/crossword_wordlist.txt", "r")
    writeToFile = open("../githubList/sortedGithubList.txt", "w")
    for line in database:
        line = line.strip()
        data = line.split(";")
        if (int(data[1]) >= requiredScore and len(data[0]) <= lengthCap):
            for char in disallowed:
                if char in data[0]:
                    data[0] = notify(data[0], char, False)
            if (len(data[0]) > 0):
                writeToFile.write(data[0].upper() + "\n")


if __name__ == "__main__":
    main()