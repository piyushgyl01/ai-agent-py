import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Available functions for the LLM
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

# System prompt that instructs the LLM on how to use functions
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

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
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        # Print normal text response
        print(response.text)
    
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()