import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key == None:
    raise RunTimeError("api key is none")
else:
    print("api key is good")

from google import genai

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model ='gemini-2.5-flash', contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
)
if response.usage_metadata == None:
    raise RuntimeError("Failed API request")
else:
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    print("Prompt tokens: " + str(prompt_tokens))
    print("Response tokens: " + str(response_tokens))
    print("Response:")
    print(response.text)
