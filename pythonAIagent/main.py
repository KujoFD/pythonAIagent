import os
from dotenv import load_dotenv
from prompts import system_prompt
from call_function import available_functions, call_function

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

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model ='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )
    if response.usage_metadata is None:
        raise RuntimeError("Failed API request")

    else:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
    if verbose:
        
        print("Prompt tokens: " + str(prompt_tokens))
        print("Response tokens: " + str(response_tokens))
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)



    if not response.function_calls and response.text:
        print("Response:")
        print(response.text)
        return response.text
   
    function_calls_list =[]
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose)
        if not function_call_result.parts:
            raise Exception("function_call_result.parts is empty")
        else:
            part = function_call_result.parts[0]
            if part.function_response is None:
                raise Exception("part.function_response is None")
            if part.function_response.response is None:
                raise Exception("part.function_response.response is None")
            function_calls_list.append(part)
            if verbose:
                print(f"->{part.function_response.response}")
    messages.append(types.Content(role="user", parts=function_calls_list))
    return None
iters=0
MAX_ITERS=20

while iters < MAX_ITERS:
    iters+=1
    try:
        final_text = generate_content(client, messages, args.verbose)
        if final_text:
            break
    except Exception as e:
        print(f"Error in generate_content: {e}")
        break
if iters >= MAX_ITERS and not final_text:
    print(f"Maximum iterations ({MAX_ITERS}) reached.")