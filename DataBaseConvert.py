import os
import random

from sys import flags
from Cell import LetterCell, IndexCell, BlockedCell
from version1 import WordCell


def convertBase():
    # Open a file in read mode
    alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']

    for letter in alph:

        with open('Crossword Databases/' + letter + '_words_converted.txt', 'r') as file:
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

        # List of alphabet letters
        alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']

        # Create a dictionary to hold words by their starting letters
        words_by_letter = {letter: [] for letter in alph}

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




def findWord(IndexCell):
    indices = []
    wordLength = len(IndexCell.body)
    print(wordLength)
    #Creates 2-d list of letters and their indexes
    for i, val in enumerate(IndexCell.body):
        if(isinstance(val, LetterCell)):
            indices.append([i, val.letter])



    finalWords = []
    filePath = "Words/"
    flag = False
    #Cheks to see if fist letter is filled
    if indices[0][0] == 0:
        #Makes filepath
        filePath+=indices[0][1].lower()+"-Words/words_"+str(wordLength)+".txt"
        finalWords,flag = genWord(filePath, indices)

    else:
        #If first letter is not given
        #Iterate until finds valid words
        while not flag:
            #Generate random starting letter
            random_num = random.randint(1, 26)
            random_letter = chr(random_num + 96)
            # Makes filepath

            filePath += random_letter.lower() + "-Words/words_" + str(wordLength) + ".txt"
            finalWords, flag = genWord(filePath, indices)


    print(finalWords)



#Iterates through and finds word that fits indices specifications
def genWord(filePath,indices):
    finalWords = []
    with open(filePath, 'r') as file:
        words = file.read().splitlines()  # Split the content by newlines

    for i in range(len(words)):

        flag = True
        for indexs in indices:

            if words[i][indexs[0]] != indexs[1]:
                flag = False
        if flag:
            finalWords.append(words[i])
    #flag set to true if word was found
    flag = len(finalWords) > 0
    #Returns list of valid words and flag determining if something was found or not
    return finalWords , flag



def main():
    c = IndexCell(0,0,True)

    Cell2 = BlockedCell(1,0)
    #Cell2.setLetter("B")

    Cell3 = BlockedCell(2, 0)


    Cell4 = BlockedCell(3, 0)


    Cell5 = LetterCell(4, 0)
    Cell5.setLetter("L")
    wordlist = [ Cell2, Cell3, Cell4, Cell5 ]

    c.setbody(wordlist)
    for val in c.body:
        print(val)



    findWord(c)


if __name__ == "__main__":
    main()