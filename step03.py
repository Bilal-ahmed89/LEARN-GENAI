import typing
from openai.types.chat.chat_completion import ChatCompletion
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os

_: bool = load_dotenv(find_dotenv())

client: OpenAI = OpenAI()

stream = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[{"role": "user", "content" : "this is a test"}],
    stream=True,
)

for part in stream:
    print(part.choices[0].delta.content or "")


