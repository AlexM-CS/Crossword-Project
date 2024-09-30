import os

def main():
    # Open a file in read mode
    alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    for letter in alph:

        with open('Crossword Databases/'+letter+'_words_converted.txt', 'r') as file:
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
        alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

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

if __name__ == "__main__":
    main()