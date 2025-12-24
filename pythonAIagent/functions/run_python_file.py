import os
import subprocess
from subprocess import PIPE, STDOUT
def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if valid_target_file == False:
            return(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        if os.path.isfile(target_file) == False:
            return(f'Error: "{file_path}" does not exist or is not a regular file')
        if target_file.endswith('.py') == False:
            return(f'Error: "{file_path}" is not a Python file')
        command = ["python", target_file]
        if args !=None:
            for arg in args:
                command.append(str(arg))
        ran_command = subprocess.run(command, stdout=PIPE, stderr=PIPE, timeout=30, cwd=working_directory, text=True)
        output_string = ""
        if ran_command.returncode!=0:
            output_string+= f'Process exited with code {ran_command.returncode}\n'
        if len(ran_command.stdout)==0 and len(ran_command.stderr)==0:
            output_string+= f'No output produced\n'
        else:
            if ran_command.stdout!="":
                output_string+= f'STDOUT: {ran_command.stdout}\n'
            if ran_command.stderr!="":
                output_string+= f'STDERR: {ran_command.stderr}\n'
        return output_string
    except Exception as e:
        return f'Error: executing python file: {e}'