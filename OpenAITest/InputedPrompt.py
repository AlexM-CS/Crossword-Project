system_message = """
    You are a expert crossword hint creator.
    Your role is to create crossword hints 
    """

def generate_Prompt(topic):
    prompt = """Generate a crossword hint for following separated by commas
     {topic}
     , making each simple, yet concise. 
     Keep each hint to on the same line, with only the the hints being returned. Separate each hint by the letter
     "Ɇ". After finding a hint for the last word, do not add a "Ɇ"
     Do not include number of letters in the word.""".format(topic=topic)
    return prompt