system_message = """
    You are a expert crossword hint creator.
    Your role is to create crossword hints 
    """

def generate_Prompt(topic):
    prompt = """Generate a crossword hint for following separated by commas
     {topic}
     , making each cryptic/simple. 
     Keep each hint to a single line, with only the hints being returned. Separate each hint by the word
     "___"
     Do not include number of letters in the word.""".format(topic=topic)
    return prompt
