import unittest
import json
import os,sys
print(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from src import autofix_json as af
from src import rpsec_to_python as rp


class TestJsonAutofix(unittest.TestCase):

    def test_correct_json(self):
        json_str = '{ "item": { "name": "item3" }}'
        self.assertEqual(json.loads(json_str), json.loads(af.autofix_json_string(json_str)))
    
    def test_missing_closing_brace(self):
        json_str = '{ "item": { "name": "item3" }'
        fixed_str = af.autofix_json_string(json_str)
        self.assertEqual(json.loads(fixed_str), {"item": {"name": "item3"}})
    
    def test_missing_closing_bracket(self):
        json_str = '[1, 2, 3'
        fixed_str = af.autofix_json_string(json_str)
        self.assertEqual(json.loads(fixed_str), [1, 2, 3])

class TestRubyToJsonConversion(unittest.TestCase):

    def test_simple_ruby_hash(self):
        ruby_hash = "{ item: 'item3' }"
        expected = {"item": "item3"}
        self.assertEqual(rp.ruby_to_json(ruby_hash), expected)
    
    def test_nested_ruby_hash(self):
        ruby_hash = "{ item: { name: 'item3' } }"
        expected = {"item": {"name": "item3"}}
        self.assertEqual(rp.ruby_to_json(ruby_hash), expected)
    
    def test_ruby_hash_with_numbers(self):
        ruby_hash = "{ count: 5, items: [1, 2, 3] }"
        expected = {"count": 5, "items": [1, 2, 3]}
        self.assertEqual(rp.ruby_to_json(ruby_hash), expected)

class TestRSpecParsing(unittest.TestCase):

    def setUp(self):
        self.rspec_content = """
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

    def test_parse_rspec(self):
        expected_tests = [
            {
                'method': 'get',
                'url': '/api/items',
                'params': None,
                'status': '200',
                'body': ['item1', 'item2']
            },
            {
                'method': 'post',
                'url': '/api/items',
                'params': {"item": {"name": "item3"}},
                'status': '201',
                'body': ['item3']
            }
        ]
        self.assertEqual(rp.parse_rspec(self.rspec_content), expected_tests)

class TestPythonTestGeneration(unittest.TestCase):

    def setUp(self):
        self.parsed_tests = [
            {
                'method': 'get',
                'url': '/api/items',
                'params': None,
                'status': '200',
                'body': ['item1', 'item2']
            },
            {
                'method': 'post',
                'url': '/api/items',
                'params': {"item": {"name": "item3"}},
                'status': '201',
                'body': ['item3']
            }
        ]
    
    def test_generate_python_tests(self):
        expected_python_code = """import requests
import requests_mock

def test_api():
    with requests_mock.Mocker() as mocker:
        mocker.get('http://localhost:3000/api/items', status_code=200, json=["item1", "item2"])
        mocker.post('http://localhost:3000/api/items', status_code=201, json=["item3"])

        response = requests.get('http://localhost:3000/api/items')
        assert response.status_code == 200
        assert all(item in response.json() for item in ["item1", "item2"])

        response = requests.post('http://localhost:3000/api/items', json={"item": {"name": "item3"}})
        assert response.status_code == 201
        assert all(item in response.json() for item in ["item3"])
"""
        self.assertEqual(rp.generate_python_tests(self.parsed_tests).strip(), expected_python_code.strip())
        
if __name__ == '__main__':
    unittest.main()
