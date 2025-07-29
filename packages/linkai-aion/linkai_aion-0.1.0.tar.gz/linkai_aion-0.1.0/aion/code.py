
### aion/code.py
def explain_code(code):
    if "for" in code and "in" in code:
        return "This is a loop."
    elif "def" in code:
        return "This is a function definition."
    return "Code pattern not recognized."

def extract_functions(code):
    import re
    return re.findall(r'def (\w+)\(', code)

def strip_comments(code):
    return "\n".join([line for line in code.splitlines() if not line.strip().startswith("#")])