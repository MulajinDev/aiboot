import os
from config import MAX_CHARS
from google.genai import types 

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path and file to read from, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        path = os.path.abspath(os.path.join(working_directory, file_path))
        if not path.startswith(os.path.abspath(working_directory)):
            return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"
        if not os.path.isfile(path):
            return f"Error: File not found or is not a regular file: \"{file_path}\""
    except Exception as e:
        return f"Error: {e}"
    
    try:
        with open(path, "r") as f:
            file_content = f.read(MAX_CHARS)
    except Exception as e:
        return f"Error: {e}"
    
    if len(file_content) == 10000:
        file_content += f" [...File \"{file_path}\" truncated at 10000 characters]"

    return file_content