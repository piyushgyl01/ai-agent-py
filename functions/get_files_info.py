import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    """
    List the contents of a directory with file sizes and directory status.
    
    Args:
        working_directory: The base directory that acts as a security boundary
        directory: The relative path within working_directory to list (default is current dir)
    
    Returns:
        A formatted string listing directory contents or an error message
    """
    try:
        # Create the full path by joining working_directory and directory
        full_path = os.path.join(working_directory, directory)
        
        # Get absolute paths for security validation
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_dir = os.path.abspath(full_path)
        
        # Check if target directory is within working directory boundaries
        try:
            # Check if abs_target_dir is within abs_working_dir
            common_path = os.path.commonpath([abs_working_dir, abs_target_dir])
            if common_path != abs_working_dir:
                return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        except ValueError:
            # commonpath raises ValueError if paths are on different drives (Windows)
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # Check if the path exists and is a directory
        if not os.path.exists(abs_target_dir):
            return f'Error: "{directory}" does not exist'
        
        if not os.path.isdir(abs_target_dir):
            return f'Error: "{directory}" is not a directory'
        
        # List directory contents
        entries = []
        for item in os.listdir(abs_target_dir):
            item_path = os.path.join(abs_target_dir, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            entries.append(f" - {item}: file_size={file_size} bytes, is_dir={is_dir}")
        
        return "\n".join(entries)
        
    except Exception as e:
        return f"Error: {str(e)}"

# Function schema for LLM
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