import os
import glob
from rspec_to_python import *
from helpers import *


def read_content(file_path):
    try:
        with open(file_path, 'r') as file:
            print(f"Reading file: {file_path}")
            content=file.read()
    except Exception as e:
        print(e)
    return content

def read_rspec_files(test_dir):
    """
    Reads all RSpec .rb files in the specified test directory and prints their contents.
    
    :param test_dir: The directory containing the RSpec .rb files
    """
    # Get all .rb files in the test directory
    rspec_files = glob.glob(os.path.join(test_dir, '*.rb'))
    all_files=[]
    # Read each file and print its contents
    for file_path in rspec_files:
        try:
            file_name=file_path.split("\\")[-1]
            file_name=file_name.replace(".rb","")
            all_files.append({file_name:file_path})
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
    return all_files

if __name__ == "__main__":
    config_path = '../config.json'
      # specify the path to your config file
    config = read_config(config_path)
    directories = config.get('directories', {})  # Get the 'directories' section, default to an empty dict if not found
    input_dir = directories.get('input_dir')
    output_dir = directories.get('output_dir')
    all_files=read_rspec_files(input_dir)

    for file in all_files:
        #print(file)
        file_name = next(iter(file.keys()))
        content = next(iter(file.values()))
        rspec_content=read_content(content)
        parsed_tests = parse_rspec(rspec_content)
        python_test_code = generate_python_tests(parsed_tests)
        
        write_python_code_to_file(python_test_code,file_name,output_dir=output_dir)
