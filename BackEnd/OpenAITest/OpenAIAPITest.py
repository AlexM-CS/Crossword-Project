# Created:
# Last updated: 12-12-2024
# Alexander Myska, Oliver Strauss, and Brandon Knautz

# <File description here>

# External imports:
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from pyexpat.errors import messages

# When running from here, use these imports:
# from PromptsTest import system_message, generate_Prompt

# When running from main, use these imports:
from BackEnd.OpenAITest.PromptsTest import system_message, generate_Prompt

_ = load_dotenv(find_dotenv())
client = OpenAI()
model = "gpt-4o"
temperature = 0.3
max_tokens = 100
topic = "baberuth,berm,dorks"

def get_hints(topics: [str]):
    """
    Credit: Brandon Knautz
    Creates hints for a list of words
    @param topics: the list of topics to generate hints for
    @return:
    """
    sys_message = system_message
    prompt = generate_Prompt(topics)
    messages = [
        {"role": "system", "content": sys_message},
        {"role": "user", "content": prompt}
    ]
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    hints = completion.choices[0].message.content
    return hints.split("___")

def get_hint():
    """
    Credit: Brandon Knautz
    <Method description here>
    @return:
    """
    completion = client.chat.completions.create(
        model = model,
        messages = messages,
        temperature = temperature,
        max_tokens = max_tokens
    )
    return completion.choices[0].message.content

def main():
    returner = get_hints(["baberuth", "berm", "dorks"])
    print(returner)

if __name__ == "__main__":
    main()