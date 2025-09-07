import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Available functions for the LLM
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

# System prompt that instructs the LLM on how to use functions
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Map function names to actual functions
function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(function_call_part, verbose=False):
    """
    Execute a function call and return the result as a types.Content object.
    
    Args:
        function_call_part: A types.FunctionCall with .name and .args properties
        verbose: Whether to print detailed information about the function call
    
    Returns:
        types.Content object with the function response
    """
    function_name = function_call_part.name
    function_args = dict(function_call_part.args)
    
    # Print function call information
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    
    # Check if function exists
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    # Add working directory to arguments
    function_args["working_directory"] = "./calculator"
    
    # Call the function
    function_to_call = function_map[function_name]
    function_result = function_to_call(**function_args)
    
    # Return the result as a types.Content object
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )

def main():
    if len(sys.argv) < 2:
        print("Error: Please provide a prompt as a command line argument.")
        sys.exit(1)
    
    prompt = sys.argv[1]
    
    verbose = "--verbose" in sys.argv
    
    if verbose:
        print(f"User prompt: {prompt}")
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt
        ),
    )
    
    # Check if the LLM wants to call a function
    if response.function_calls:
        for function_call_part in response.function_calls:
            # Actually call the function
            function_call_result = call_function(function_call_part, verbose)
            
            # Verify the response structure
            if not function_call_result.parts or not hasattr(function_call_result.parts[0], 'function_response'):
                raise Exception("Invalid function response structure")
            
            # Print the result if verbose
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        # Print normal text response
        print(response.text)
    
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()