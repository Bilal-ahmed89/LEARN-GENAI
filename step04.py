from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from openai.types.chat.chat_completion import ChatCompletion

_ : bool = load_dotenv(find_dotenv())

client : OpenAI = OpenAI()

userPrompt1  = input("Explain what you want this AI model to pretend: ")
userPrompt2  = input("Enter your prompt: ")

response = client.chat.completions.create(
  model="gpt-3.5-turbo-1106",
  response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": userPrompt1},
    {"role": "user", "content": userPrompt2}
  ]
)

print("AI's response:", response.choices[0].message.content)