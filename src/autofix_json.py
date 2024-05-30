import json

def autofix_json_string(json_str):
    """
    Attempts to fix an improperly closed JSON string by adding the missing closing brackets or braces.
    """
    # Stack to keep track of opening brackets and braces
    stack = []
    
    for char in json_str:
        if char in ['{', '[']:
            stack.append(char)
        elif char in ['}', ']']:
            if stack and ((char == '}' and stack[-1] == '{') or (char == ']' and stack[-1] == '[')):
                stack.pop()
    
    # Add the missing closing brackets or braces
    missing_closures = ''.join('}' if c == '{' else ']' for c in reversed(stack))
    
    # Return the fixed JSON string
    fixed_json_str = json_str + missing_closures
    return fixed_json_str

# # Test the function with both correctly and incorrectly closed JSON strings
# json_strings = [
#     '{ "item": { "name": "item3" }',
#     '{ "item": { "name": "item3" }}',
#     '[1, 2, 3',
#     '[1, 2, 3]'
# ]

# for json_str in json_strings:
#     try:
#         # Attempt to parse the original string
#         print("Original:", json_str)
#         parsed = json.loads(json_str)
#         print("Parsed Successfully:", parsed)
#     except json.JSONDecodeError:
#         # If parsing fails, attempt to fix the string
#         fixed_json_str = autofix_json_string(json_str)
#         print("Fixed:", fixed_json_str)
#         parsed = json.loads(fixed_json_str)
#         print("Parsed Successfully After Fix:", parsed)
#     print()
