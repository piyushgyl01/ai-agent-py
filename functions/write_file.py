import os

def write_file(working_directory, file_path, content):
    """
    Write content to a file within the working directory.
    
    Args:
        working_directory: The base directory that acts as a security boundary
        file_path: The relative path to the file within working_directory
        content: The content to write to the file
    
    Returns:
        A success message or an error string
    """
    try:
        # Create the full path by joining working_directory and file_path
        full_path = os.path.join(working_directory, file_path)
        
        # Get absolute paths for security validation
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(full_path)
        
        # Security check: ensure file is within working directory
        if not abs_file_path.startswith(abs_working_dir + os.sep) and abs_file_path != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # Create directory if it doesn't exist
        directory = os.path.dirname(abs_file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        # Write content to file
        with open(abs_file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        # Return success message with character count
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f"Error: {str(e)}"