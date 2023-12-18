from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from openai.types.chat.chat_completion import ChatCompletion

_ : bool = load_dotenv(find_dotenv())

client : OpenAI = OpenAI()



def chat_completion(prompt1 : str, prompt2 : str)->str:
  completion : ChatCompletion = client.chat.completions.create(
    model  = "gpt-3.5-turbo-1106",
    messages= [
      {"role": "system", "content": prompt1},
      {"role": "user", "content": prompt2}
    ]
  )

  return completion.choices[0].message.content


userPrompt1  = input("Wxplain what you want this AI model to pretend: ")
userPrompt2  = input("Enter your prompt: ")

result = chat_completion(userPrompt1, userPrompt2)
print("AI's response:", result)
