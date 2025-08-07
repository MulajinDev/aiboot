import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import SYSTEM_PROMPT, AI_MODEL_NAME
from functions.get_files_info import *
from functions.get_file_content import *
from functions.write_file import *
from functions.run_python import *

def main():
    load_dotenv()

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ]
    )

    verbose = False

    args = sys.argv[1:]

    if not args:
        print("Usage: main.py \"prompt\"")
        sys.exit(1)

    for i in range(0,len(args)):
        if args[i] == "--verbose" or args[i] == "--v":
            verbose = True
            args.pop(i)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]

    ai_cfg = genai.types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=SYSTEM_PROMPT
    )

    ai_response = client.models.generate_content(model=AI_MODEL_NAME,contents=messages, config=ai_cfg)
    ai_calls = ai_response.function_calls
    if ai_calls:
        for call in ai_calls:
            print(f"Calling function: {call.name}({call.args})")
    else:
        print(f"Response: {ai_response.text}")

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {ai_response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {ai_response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
