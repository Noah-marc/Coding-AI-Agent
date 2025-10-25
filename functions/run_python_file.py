import os
import subprocess
from sys import stdout
from functions.config import TIMEOUT_LIMIT

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a Python file in a specified working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of arguments to pass to the Python file when executing it. If known arguments were supplied (or you do not know them), then do not fill out this field. ",
            ),
        },
        required=["file_path"],
    ),
)


def run_python_file(working_directory, file_path, args=[]):
    try: 
        full_path = os.path.join(working_directory, file_path)

        if not os.path.isfile(os.path.abspath(full_path)): 
            return f'Error: File "{file_path}" not found.'
        
        if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)): 
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not full_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'

        args = ["uv", "run", os.path.abspath(full_path)] + args
        result = subprocess.run(args=args, timeout=TIMEOUT_LIMIT, cwd=working_directory, capture_output=True, )
        returncode_str = None
        stdout = None
        stderr = None

        if result.stdout == b'' and result.stderr == b'': 
            return "No output produced."
        if result.stdout != b'':  
            stdout = f"STDOUT: {result.stdout.decode().strip()}"
        if result.stderr != b'': 
            stderr = f"STDERR: {result.stderr.decode().strip()}"

        if result.returncode != 0:
            returncode_str = f"Process exited with code {result.returncode}."

        return "\n".join(filter(None, [stdout, stderr, returncode_str]))

    except Exception as e:
        return f'Error: Executing python file: {e}'