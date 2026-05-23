import os
from django.conf import settings

def list_entries():
    entries_dir = os.path.join(settings.BASE_DIR, "entries")
    if not os.path.exists(entries_dir):
        os.makedirs(entries_dir)
    _, _, filenames = next(os.walk(entries_dir))
    filenames = [f for f in filenames if f.endswith(".md")]
    return [f[:-3] for f in filenames]

def save_entry(title, content):
    filename = f"{title}.md"
    filepath = os.path.join(settings.BASE_DIR, "entries", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def get_entry(title):
    try:
        filename = f"{title}.md"
        filepath = os.path.join(settings.BASE_DIR, "entries", filename)
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None
