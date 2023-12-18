import typing
from openai.types.chat.chat_completion import ChatCompletion
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os

_: bool = load_dotenv(find_dotenv())

client: OpenAI = OpenAI()

def chat_completion(prompt: str) -> typing.any:
    response: ChatCompletion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo-1106",
    )
    return response.choices[0].message.content


user_prompt = input("Enter your prompt: ")
result = chat_completion(user_prompt)
print("AI's response:", result)
