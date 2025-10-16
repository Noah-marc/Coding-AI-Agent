import os
from functions.config import CHAR_LIMIT

def get_file_content(working_directory, file_path):
    try: 
        full_path = os.path.join(working_directory, file_path)

        if not os.path.isfile(os.path.abspath(full_path)): 
            return f'Error: "{file_path}" is not a file or'

        if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)): 
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        with open(full_path, 'r') as file:
            content = file.read(CHAR_LIMIT)
            if file.read(1) != "": 
                content= f"{content}\n[...File \"{file_path}\" truncated at {CHAR_LIMIT} characters]"
            return content
        
    except Exception as e:
        # Catch all errors and return as string for the LLM to handle
        return f'Error: {e}'