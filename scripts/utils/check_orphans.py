import json
import os
import glob

STATUS_FILE = "rag_storage/kv_store_doc_status.json"
KNOWLEDGE_DIR = "docs/knowledge"

def main():
    if not os.path.exists(STATUS_FILE):
        print(f"Status file {STATUS_FILE} not found.")
        return

    with open(STATUS_FILE, 'r') as f:
        status_data = json.load(f)

    processed_files = set()
    for doc_id, info in status_data.items():
        if info.get('status') == 'processed':
            processed_files.add(info.get('file_path'))

    all_md_files = glob.glob(os.path.join(KNOWLEDGE_DIR, "**/*.md"), recursive=True)
    
    missing_files = []
    for filepath in all_md_files:
        if filepath not in processed_files:
            missing_files.append(filepath)

    print(f"Total MD files found: {len(all_md_files)}")
    print(f"Processed files in RAG: {len(processed_files)}")
    print(f"Missing/Orphaned files count: {len(missing_files)}")
    print("\nList of missing files:")
    for f in sorted(missing_files):
        print(f"- {f}")

if __name__ == "__main__":
    main()
