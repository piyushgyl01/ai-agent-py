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

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, analyze what you need to do and use the available functions step by step to accomplish the task. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments  
- Write or overwrite files

Work methodically through the problem:
1. First, explore and understand the codebase if needed
2. Gather the necessary information
3. Make any required changes
4. Test your changes if appropriate
5. Provide a clear final summary of what you accomplished

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

When you have completed the user's request, provide a final response explaining what you did.
"""

function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = dict(function_call_part.args)
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    
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
    
    function_args["working_directory"] = "./calculator"
    
    function_to_call = function_map[function_name]
    function_result = function_to_call(**function_args)
    
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
    
    user_prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv
    
    if verbose:
        print(f"User prompt: {user_prompt}")
    
    messages = [
        types.Content(role="user", parts=[types.Part.from_text(text=user_prompt)])
    ]
    
    max_iterations = 20
    
    try:
        for iteration in range(max_iterations):
            if verbose:
                print(f"\n--- Iteration {iteration + 1} ---")
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], 
                    system_instruction=system_prompt
                ),
            )
            
            for candidate in response.candidates:
                messages.append(candidate.content)
            
            if response.function_calls:
                for function_call_part in response.function_calls:
                    function_result = call_function(function_call_part, verbose)
                    
                    messages.append(function_result)
                    
                    if verbose:
                        print(f"-> {function_result.parts[0].function_response.response}")
                
                continue
            
            elif response.text:
                print("Final response:")
                print(response.text)
                break
            
            else:
                print("No response from model. Ending conversation.")
                break
        
        else:
            print(f"Reached maximum iterations ({max_iterations}). Ending conversation.")
    
    except Exception as e:
        print(f"Error during agent execution: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
    
    if verbose:
        print(f"\nConversation ended after {min(iteration + 1, max_iterations)} iterations.")


if __name__ == "__main__":
    main()