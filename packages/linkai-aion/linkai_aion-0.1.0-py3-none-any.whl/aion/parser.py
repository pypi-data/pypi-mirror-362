### aion/parse.py
def extract_json(text):
    import json
    import re
    matches = re.findall(r'{.*?}', text, re.DOTALL)
    for match in matches:
        try:
            return json.loads(match)
        except:
            continue
    return {}

def clean_text(text):
    return " ".join(text.split())

def to_snake_case(text):
    import re
    text = re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()
    return text