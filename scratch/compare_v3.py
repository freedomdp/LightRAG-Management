import os
import re

def get_notebook_titles():
    with open('/Users/sergej/StudioProjects/LightRAG/temp/notebook_sources.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def get_local_filenames():
    files = os.listdir('/Users/sergej/StudioProjects/LightRAG/docs/notebook_content')
    return set(f for f in files if f.endswith('.md'))

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text).strip('_')
    return text

def compare():
    notebook_titles = get_notebook_titles()
    local_files = get_local_filenames()
    
    # Pre-slugify local filenames (removing 'new_' and '_partX')
    local_slugs = set()
    for f in local_files:
        s = re.sub(r'^new_', '', f)
        s = re.sub(r'_part\d+\.md$', '', s)
        s = re.sub(r'\.md$', '', s)
        local_slugs.add(s)

    missing = []
    for title in notebook_titles:
        slug = slugify(title)
        if slug not in local_slugs:
            # Check for very close matches (slug within filename slug)
            found = False
            for ls in local_slugs:
                if slug in ls or ls in slug:
                    found = True
                    break
            if not found:
                missing.append(title)

    print(f"Total: {len(notebook_titles)}")
    print(f"Missing: {len(missing)}")
    for m in missing:
        print(f"- {m}")

if __name__ == "__main__":
    compare()
