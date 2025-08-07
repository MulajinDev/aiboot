import os
from google.genai import types 

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the specified content to the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path and file to write to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the specified file in \"file_path\""
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        path = os.path.abspath(os.path.join(working_directory, file_path))
        if not path.startswith(os.path.abspath(working_directory)):
            return f"Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory"
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
        #if not os.path.isfile(path):
        #    return f"Error: File not found or is not a regular file: \"{file_path}\""
    except Exception as e:
        return f"Error: {e}"
    
    try:
        with open(path, "w") as f:
            f.write(content)
            return f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)"
    except Exception as e:
        return f"Error {e}"
    
    return "Unknown Error"