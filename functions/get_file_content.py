import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        # Create the full path
        full_path = os.path.join(working_directory, file_path)
        
        # Get absolute paths for security validation
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(full_path)
        
        # Security check: ensure file is within working directory
        if not abs_file_path.startswith(abs_working_dir + os.sep) and abs_file_path != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # Check if file exists and is a file
        if not os.path.exists(abs_file_path) or not os.path.isfile(abs_file_path):
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