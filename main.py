import os
from xmlrpc import client
from dotenv import load_dotenv
from google import genai
import sys

""" Very simple script, that is only used for understanding gemini api. That is why no argparse. Usually one should use argparse for command line arguments. """

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


def main():
    client = genai.Client(api_key=api_key)
    try: 
        user_prompt = sys.argv[1]
        
        from google.genai import types

        messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),
            ]
        response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)
        if "--verbose" in sys.argv: 
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    except IndexError: 
        print("Please provide a prompt as a command-line argument.")
        sys.exit(1)



if __name__ == "__main__":
    main()
