from google.genai import types

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file

callable_functions = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file
}

def call_function(function_call_part:types.FunctionCall, verbose=False):
    function_name = function_call_part.name
    if verbose: 
        print(f"Calling function: {function_name}({function_call_part.args})")
    else: 
        print(f" - Calling function: {function_name}")

    function = callable_functions.get(function_name)
    if function is None: 
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    else: 
        function_response = function(**function_call_part.args, working_directory="./calculator")
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_response},
                )
            ],
        )


      