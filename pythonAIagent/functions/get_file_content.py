import os
from google.genai import types
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads file contents in a specified file path relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read contents from, relative to the working directory",
            ),
        },
        required=["file_path"]
    ),
)

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if valid_target_file == False:
            return(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        if os.path.isfile(target_file) == False:
            return(f'Error: File not found or is not a regular file: "{file_path}"')
        
        from config import MAX_CHARS
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
    except Exception as e:
        return(f"Error: {e}")