class Sorter:
    # Initializes a sorter with a filepath
    def __init__(self, filepath):
        self.data = open(filepath, "r").read().split(" ")

    # Override the default string representation of this object
    def __str__(self):
        return self.data.__str__()

    # Checks a database of vulgar words to ensure none appear in the list
    def vulgarCheck(self):
        pass

    # Checks to see if words in the list contain "-ing"
    def ingWords(self):
        pass

    # Checks to see if a word and its plural both appear in a list
    def pluralCheck(self):
        pass

    # Checks the length of each word in the list
    def lengthCheck(self):
        pass

    # Checks a database of proper nouns to see if they are in the list
    def properNounsCheck(self):
        pass