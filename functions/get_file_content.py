import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(full_path)
        
        try:
            common_path = os.path.commonpath([abs_working_dir, abs_file_path])
            if common_path != abs_working_dir:
                return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        except ValueError:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(abs_file_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)
        
        with open(abs_file_path, "r", encoding="utf-8") as f:
            full_content = f.read()
            if len(full_content) > MAX_CHARS:
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        
        return content
        
    except Exception as e:
        return f"Error: {str(e)}"

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