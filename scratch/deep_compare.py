import os
import json
import re

def get_local_titles():
    dir_path = '/Users/sergej/StudioProjects/LightRAG/docs/notebook_content'
    titles = set()
    for filename in os.listdir(dir_path):
        if filename.endswith('.md'):
            path = os.path.join(dir_path, filename)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Extract title from the markdown/json structure
                    # Format is usually: 1: { 2: "title": "...", 3: "content": "..." }
                    # But the line numbers are added by the view tool, so we look for raw content.
                    match = re.search(r'"title":\s*"(.*?)"', content)
                    if match:
                        title = match.group(1)
                        # Remove prefix 'new_' and suffix '(Часть X)'
                        title = re.sub(r'^new_', '', title)
                        title = re.sub(r'\s*\(Часть\s*\d+\)$', '', title)
                        titles.add(title.strip())
            except:
                continue
    return titles

def compare():
    with open('/Users/sergej/StudioProjects/LightRAG/temp/notebook_sources.txt', 'r', encoding='utf-8') as f:
        notebook_titles = [line.strip() for line in f if line.strip()]
    
    local_titles = get_local_titles()
    
    missing = []
    for title in notebook_titles:
        if title not in local_titles:
            # Try fuzzy match (slug based)
            match = False
            title_slug = re.sub(r'[^a-zA-Z0-9]+', '', title).lower()
            for lt in local_titles:
                lt_slug = re.sub(r'[^a-zA-Z0-9]+', '', lt).lower()
                if title_slug == lt_slug or title_slug in lt_slug or lt_slug in title_slug:
                    match = True
                    break
            if not match:
                missing.append(title)

    print(f"Total Sources in NotebookLM: {len(notebook_titles)}")
    print(f"Already Indexed: {len(notebook_titles) - len(missing)}")
    print(f"Missing: {len(missing)}")
    
    if missing:
        print("\n--- MISSING DOCUMENTS ---")
        for m in missing:
            print(f"- {m}")

if __name__ == "__main__":
    compare()
