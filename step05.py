import json
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from openai.types.chat.chat_completion import ChatCompletion, ChatCompletionMessage

_: bool = load_dotenv(find_dotenv())

client: OpenAI = OpenAI()


def get_current_weather(location: str, unit: str = "fahrenheit") -> str:
    """Get the current weather in a given location"""
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": "celsius"})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": "fahrenheit"})
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": "celsius"})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})


def run_conversation(main_request: str) -> str:
    messages = [{"role": "user", "content": main_request}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
        }
    ]
      
    response: ChatCompletion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    response_message: ChatCompletionMessage = response.choices[0].message
    print("* First Response: ", dict(response_message))

    tool_calls = response_message.tool_calls
    print("* First Reponse Tool Calls: ", list(tool_calls))

    if tool_calls:
        available_functions = {
            "get_current_weather": get_current_weather,
        }
        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                location=function_args.get("location"),
                unit=function_args.get("unit"),
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )

        print("* Second Request Messages: ", list(messages))
        second_response: ChatCompletion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
        )
        print("* Second Response: ", dict(second_response))

        return second_response.choices[0].message.content



run_conversation( "What's the weather like in San Francisco, Tokyo?")      
