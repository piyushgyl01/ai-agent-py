import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    """
    Read the contents of a file within the working directory.
    
    Args:
        working_directory: The base directory that acts as a security boundary
        file_path: The relative path to the file within working_directory
    
    Returns:
        The file contents as a string, or an error message
    """
    try:
        # Create the full path by joining working_directory and file_path
        full_path = os.path.join(working_directory, file_path)
        
        # Get absolute paths for security validation
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(full_path)
        
        # Check if target file is within working directory boundaries
        try:
            # Check if abs_file_path is within abs_working_dir
            common_path = os.path.commonpath([abs_working_dir, abs_file_path])
            if common_path != abs_working_dir:
                return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        except ValueError:
            # commonpath raises ValueError if paths are on different drives (Windows)
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # Check if the path exists and is a file
        if not os.path.exists(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Read the file content
        with open(abs_file_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)
        
        # Check if we need to add truncation message
        with open(abs_file_path, "r", encoding="utf-8") as f:
            full_content = f.read()
            if len(full_content) > MAX_CHARS:
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        
        return content
        
    except Exception as e:
        return f"Error: {str(e)}"

# Function schema for LLM
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the contents of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)