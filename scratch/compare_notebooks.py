import os
import re

def clean_name(name):
    # Remove extension, prefix, and part suffix
    name = re.sub(r'^new_', '', name)
    name = re.sub(r'_part\d+$', '', name)
    name = re.sub(r'\.md$', '', name)
    return name.lower().strip()

def slugify(text):
    # Convert title to a slug that might match filenames
    text = text.lower()
    # Replace spaces and special chars with underscores
    text = re.sub(r'[^a-z0-9]+', '_', text).strip('_')
    return text

def check_notebook_diff():
    with open('/Users/sergej/StudioProjects/LightRAG/temp/notebook_sources.txt', 'r', encoding='utf-8') as f:
        notebook_titles = [line.strip() for line in f if line.strip()]

    local_files = os.listdir('/Users/sergej/StudioProjects/LightRAG/docs/notebook_content')
    local_names = set(clean_name(f) for f in local_files if f.endswith('.md'))

    missing = []
    found = []

    for title in notebook_titles:
        slug = slugify(title)
        
        # Exact slug match
        if slug in local_names:
            found.append(title)
            continue
            
        # Partial match (if slug is part of local name or vice versa)
        match = False
        for lname in local_names:
            if lname in slug or slug in lname:
                match = True
                break
        
        if match:
            found.append(title)
        else:
            missing.append(title)

    print(f"Total Notebook Titles: {len(notebook_titles)}")
    print(f"Found Locally: {len(found)}")
    print(f"Missing Locally: {len(missing)}")
    
    if missing:
        print("\n--- POSSIBLY MISSING OR UNMATCHED ---")
        for m in missing:
            print(f"- {m}")

if __name__ == "__main__":
    check_notebook_diff()
