import os
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        
        if not os.path.isdir(full_path): 
            return f'Error: "{directory}" is not a directory'

        if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)): 
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        
        contents = []
        for path in os.listdir(full_path):
            path = os.path.join(full_path, path)
            is_dir = not(os.path.isfile(path))
            size = os.path.getsize(path)
            contents.append(f"{path}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(contents)
    except Exception as e:
        #Catch all errors and return as string for the LLM to handle
        return f'Error: {e}'
