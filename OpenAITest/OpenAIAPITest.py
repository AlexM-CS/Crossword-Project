import os

import openai
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from pyexpat.errors import messages

import PromptsTest

#load env file

_ = load_dotenv(find_dotenv())
#client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
client = OpenAI()
model = "gpt-4o"
temperature = 0.3
max_tokens = 100
topic = "baberuth"
# prompts

system_message = PromptsTest.system_message
prompt = PromptsTest.generate_Prompt(topic)

messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": prompt}
]

def get_hint():
    completion = client.chat.completions.create(
        model = model,
        messages = messages,
        temperature = temperature,
        max_tokens = max_tokens
    )
    return completion.choices[0].message.content

def main():
    print("API Key:", os.environ.get("OPENAI_API_KEY"))
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello, OpenAI!"}]
        )
        print(response.choices[0].message["content"])
    except Exception as e:
        print("Error:", e)
    #returner = get_hint()
    #print(returner)

if __name__ == "__main__":
    main()

"""
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)
"""
