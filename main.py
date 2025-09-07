import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

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
        contents=prompt
    )
    
    print(response.text)
    
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()