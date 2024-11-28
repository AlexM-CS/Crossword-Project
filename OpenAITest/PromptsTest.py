system_message = """
    You are a expert crossword hint creator.
    Your role is to create crossword hints 
    """

def generate_Prompt(topic):
    prompt = """Generate a crossword hint for
     {topic}
     , making it cryptic/simple. 
     Keep the response a single line, with only the hint being returned. 
     Do not include number of letters in the word.""".format(topic=topic)
    return prompt
