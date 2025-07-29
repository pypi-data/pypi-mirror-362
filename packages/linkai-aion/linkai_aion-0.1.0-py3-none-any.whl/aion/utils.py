### aion/utils.py
def format_bytes(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

def format_duration(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes} min {seconds} sec"

def random_string(length=8):
    import random, string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def slugify(text):
    return text.strip().lower().replace(" ", "-")
