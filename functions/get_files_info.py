import os

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
        full_path = os.path.join(working_directory, directory)
        
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_dir = os.path.abspath(full_path)
        
        try:
            common_path = os.path.commonpath([abs_working_dir, abs_target_dir])
            if common_path != abs_working_dir:
                return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        except ValueError:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.exists(abs_target_dir):
            return f'Error: "{directory}" does not exist'
        
        if not os.path.isdir(abs_target_dir):
            return f'Error: "{directory}" is not a directory'
        
        entries = []
        for item in os.listdir(abs_target_dir):
            item_path = os.path.join(abs_target_dir, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            entries.append(f" - {item}: file_size={file_size} bytes, is_dir={is_dir}")
        
        return "\n".join(entries)
        
    except Exception as e:
        return f"Error: {str(e)}"