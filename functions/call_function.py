import os
from google.genai import types 
from functions.get_files_info import *
from functions.get_file_content import *
from functions.write_file import *
from functions.run_python import *

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    print(f"Calling function: {function_call_part.name}")
    
    name = function_call_part.name
    
    working_dir = "./calculator"

    function_mapper = {
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
        "get_files_info": get_files_info,
    }

    args = dict(function_call_part.args)
    args["working_directory"] = working_dir

    if name not in function_mapper:
            print("unknown---")
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=name,
                        response={"error": f"Unknown function: {name}"},
                    )
                ],
            )
    result = function_mapper[name](**args)
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=name,
                response={"result": result},
            )
        ],
    )   
