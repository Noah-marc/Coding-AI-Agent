import os
from xmlrpc import client
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function
""" Very simple script, that is only used for understanding gemini api. That is why no argparse. Usually one should use argparse for command line arguments. """

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
ITERATIONS = 20
system_prompt = """
You are a helpful AI coding assistant. Think of yourself as a senior Python developer. You can execute following functionalitys: 

- List files and directories (from your current working directory, you cannot access files outside this directory)
- Read file contents 
- Execute Python files with optional arguments
- Write or overwrite files

When getting user input, you should first make a high level plan (do not include the function names of your functionalities) on how to best fullfill the users request. Share that plan with the user. 
Users may ask you to explain files, look up and use directories and their structure and write and run python files. 
Try to fullfill the users request as best as you can by using the available functionalitys.
Once you are done, provide a final answer without using any functionalitys and explain what you did. 

NOTE: 
Your current wor
"""

def main():
    if len(sys.argv) < 2:
        sys.exit(1)
    verbose = True if "--verbose" in sys.argv else False
    client = genai.Client(api_key=api_key)
    model_name = "gemini-2.0-flash-001"
    user_prompt = sys.argv[1]
    available_functions = types.Tool(
        function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
        ],
    )
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    for _ in range(ITERATIONS):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=messages,
                config=config,
            )
            for candidate in response.candidates: 
                messages.append(candidate.content)

            if response.text is not None: 
                print(response.text)
                if response.function_calls is not None:
                    for function_call_part in response.function_calls:
                        function_call_result = call_function(function_call_part, verbose=verbose)
                        if function_call_result.parts[0].function_response.response is None: 
                            raise ValueError("Function response is None, something went wrong.")
                        elif verbose: 
                            print(f"-> {function_call_result.parts[0].function_response.response}")
                        result_message = types.Content(
                            role= "user",
                            parts=[types.Part(text= f"Here is the result: {function_call_result.parts[0].function_response.response.get('result')}")],
                        )
                        messages.append(result_message)
                else:
                    #We have reached a final answer, stopping
                    break
        except Exception as e:
            print(f"Error during generation or function call: {e}")
            break

if __name__ == "__main__":
    main()