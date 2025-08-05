import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()

    verbose = False

    args = sys.argv[1:]

    if not args:
        print("Usage: main.py \"prompt\"")
        sys.exit(1)

    for i in range(0,len(args)):
        if args[i] == "--verbose" or args[1] == "--v":
            verbose = True
            args.pop(i)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]


    ai_response = client.models.generate_content(model="gemini-2.0-flash-001",contents=messages)
    print(ai_response.text)

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {ai_response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {ai_response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
