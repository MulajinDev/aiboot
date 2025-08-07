import os
import subprocess
from config import FILE_IO_TIMEOUT
from google.genai import types 

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python file with optional argument[s].",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path and file to run (Python)",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="The arguments to be passed to the python file/script"
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    try:
        path = os.path.abspath(os.path.join(working_directory, file_path))
        cwd = os.path.abspath(working_directory)
        if not path.startswith(cwd):
            return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
        if not os.path.exists(path):
            return f"Error: File \"{file_path}\" not found"
        if not path.endswith(".py"):
            return f"Error: \"{file_path}\" is not a Python file"
        #if not os.path.isfile(path):
        #    return f"Error: File not found or is not a regular file: \"{file_path}\""
    except Exception as e:
        return f"Error: {e}"
    
    commands = ["uv","run", path]
    if args:
        commands.extend(args)
    
    try:
        run = subprocess.run(commands, cwd=cwd, capture_output=True, text=True, timeout=FILE_IO_TIMEOUT)
    except Exception as e:
        return f"Error: executing python file {e}"

    output = f"STDOUT:\n{run.stdout}"
    output += f"\nSTDERR:\n{run.stderr}"
    if run.returncode != 0:
        output += f"\nProcess exited with code {run.returncode}"
    if len(run.stdout) == 0:
        output += f"\nNo output produced."

    return output
    