import os
import json


def read_config(config_path):
    """
    Reads the YAML configuration file and returns the configuration dictionary.

    :param config_path: Path to the YAML configuration file
    :return: Configuration dictionary
    """
    with open(config_path, 'r') as file:
        config=json.loads(file.read())
    return config
def write_python_code_to_file(code_str, filename, output_dir='output'):
    """
    Writes the provided Python code string to a .py file in the specified output directory.

    :param code_str: The Python code to write to the file
    :param filename: The name of the file (without extension) to write the code to
    :param output_dir: The directory to store the output file
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Construct the full file path
    file_path = os.path.join(output_dir, f"{filename}.py")
    
    # Write the code string to the file
    try:
        with open(file_path, 'w') as file:
            file.write(code_str)
        print(f"Code successfully written to {file_path}")
    except Exception as e:
        print(f"Error writing to file {file_path}: {e}")