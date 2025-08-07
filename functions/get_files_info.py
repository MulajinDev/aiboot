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
        path = os.path.abspath(os.path.join(working_directory, directory))
        if not path.startswith(os.path.abspath(working_directory)):
            return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
        if not os.path.isdir(path):
            return f"Error: \"{directory} is not a directory"
    except Exception as e:
        return f"Error: {e}"
    output = ""
    size = ""
    is_dir = False
    temppath = ""
    try:
        contents = os.listdir(path)
        for item in contents:
            temppath = os.path.join(path, item)
            size = os.path.getsize(temppath)
            is_dir = os.path.isdir(temppath)
            output += f"- {item}: file_size={size}, is_dir={is_dir}\n"
    except Exception as e:
        return f"Error: {e}"
    return output
    