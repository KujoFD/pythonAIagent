import os
from dotenv import load_dotenv
from prompts import system_prompt
from call_function import available_functions

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key == None:
    raise RuntimeError("api key is none")
else:
    print("api key is good")

from google import genai

import argparse
from google.genai import types

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model ='gemini-2.5-flash',
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
        ),
)
if response.usage_metadata == None:
    raise RuntimeError("Failed API request")
else:
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        print("Prompt tokens: " + str(prompt_tokens))
        print("Response tokens: " + str(response_tokens))
    print("Response:")
    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(response.text)
