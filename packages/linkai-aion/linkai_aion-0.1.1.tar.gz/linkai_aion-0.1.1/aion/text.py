### aion/text.py

def count_words(text):
    return len(text.split())

def count_lines(text):
    return len(text.splitlines())

def summarize_text(text, max_lines=3):
    lines = text.split(". ")
    return ". ".join(lines[:max_lines]) + "."

def extract_emails(text):
    import re
    return re.findall(r'\b[\w.-]+?@\w+?\.\w+?\b', text)

def extract_urls(text):
    import re
    return re.findall(r'https?://\S+', text)

def highlight_keywords(text, words):
    for word in words:
        text = text.replace(word, f"**{word}**")
    return text