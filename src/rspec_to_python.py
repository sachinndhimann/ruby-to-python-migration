import re
import json
from autofix_json import autofix_json_string
# Sample RSpec test content
rspec_content = """
require 'rails_helper'

RSpec.describe 'API', type: :request do
  it 'returns a list of items' do
    get '/api/items'
    expect(response).to have_http_status(200)
    expect(response.body).to include('item1', 'item2')
  end

  it 'creates an item' do
    post '/api/items', params: { item: { name: 'item3' } }
    expect(response).to have_http_status(201)
    expect(response.body).to include('item3')
  end
end
"""

# Regular expressions to extract information
http_methods = ['get', 'post', 'put', 'delete', 'patch']
http_method_pattern = re.compile(rf"({'|'.join(http_methods)})\s+'(.*?)'(?:, params: (\{{.*?\}}))?")
status_pattern = re.compile(r"have_http_status\((\d+)\)")
body_pattern = re.compile(r"include\((.*?)\)")


def ruby_to_json(ruby_hash):
    # Replace Ruby hash rocket with colon
    ruby_hash = ruby_hash.replace('=>', ':')
    
    # Ensure proper double quoting for JSON keys and values
    ruby_hash = re.sub(r'([a-zA-Z0-9_]+):', r'"\1":', ruby_hash)
    ruby_hash = re.sub(r':\s*([a-zA-Z0-9_]+)', r': \1', ruby_hash)  # Avoid adding quotes to numeric values
    ruby_hash = re.sub(r':\s*([a-zA-Z_][a-zA-Z0-9_]*)', r': "\1"', ruby_hash)  # Add quotes to strings

    # Correctly handle nested structures and single quotes
    ruby_hash = ruby_hash.replace("'", '"')

    # Parse JSON string
    try:
        result = json.loads(ruby_hash)
    except json.JSONDecodeError:
        result = json.loads(autofix_json_string(ruby_hash))

    return result



def parse_rspec(rspec_content):
    tests = []
    http_method_pattern = re.compile(r'\b(get|post|put|patch|delete)\s+[\'"]([^\'"]+)[\'"](?:, params: (\{[^\}]+\}))?')
    status_pattern = re.compile(r'expect\(response\).to have_http_status\((\d+)\)')
    body_pattern = re.compile(r'expect\(response\.body\).to include\(([^)]+)\)')
    
    matches = http_method_pattern.findall(rspec_content)
    status_matches = status_pattern.findall(rspec_content)
    body_matches = body_pattern.findall(rspec_content)
    
    for i, (method, url, params) in enumerate(matches):
        status = status_matches[i] if i < len(status_matches) else None
        body = [match.strip('\'"') for match in body_matches[i].split(', ')] if i < len(body_matches) else []
        params_dict = ruby_to_json(params) if params else None
        tests.append({
            'method': method,
            'url': url,
            'params': params_dict,
            'status': status,
            'body': body
        })
    return tests


from helpers import read_config

def generate_python_tests(parsed_tests):
    config_path = '../config.json'
    config = read_config(config_path)
    url=config.get("url_to_be_used_in_test")
    python_code = """import requests
import requests_mock

def test_api():
    with requests_mock.Mocker() as mocker:
"""
    for test in parsed_tests:
        response_json = json.dumps(test['body']) if test['body'] else '[]'
        python_code += f"        mocker.{test['method']}('{url}{test['url']}', status_code={test['status']}, json={response_json})\n"
    
    for test in parsed_tests:
        if test['method'] in ['post', 'put', 'patch']:
            params_json = json.dumps(test['params'])
            python_code += f"        response = requests.{test['method']}('{url}{test['url']}', json={params_json})\n"
        else:
            python_code += f"        response = requests.{test['method']}('{url}{test['url']}')\n"
        python_code += f"        assert response.status_code == {test['status']}\n"
        if test['body']:
            body_json = json.dumps(test['body'])
            python_code += f"        assert all(item in response.json() for item in {body_json})\n"
        python_code += "\n"
    return python_code



# parsed_tests = parse_rspec(rspec_content)
# python_test_code = generate_python_tests(parsed_tests)
