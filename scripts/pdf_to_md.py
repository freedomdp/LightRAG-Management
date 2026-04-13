import os
import pypdf
import sys
from datetime import datetime

def convert_pdf_to_md(pdf_path, output_dir):
    """
    Extracts text from a PDF file and saves it as a Markdown file.
    """
    try:
        if not os.path.exists(pdf_path):
            print(f"Error: File not found {pdf_path}")
            return False

        filename = os.path.basename(pdf_path)
        # Handle URL encoded characters in filename if needed
        clean_filename = filename.replace("%20", " ").replace(".pdf", ".md")
        output_path = os.path.join(output_dir, clean_filename)

        print(f"Converting: {filename} -> {clean_filename}")

        reader = pypdf.PdfReader(pdf_path)
        content = []
        
        # Header Metadata
        content.append(f"# {clean_filename.replace('.md', '')}")
        content.append(f"\n**Source:** {filename}")
        content.append(f"**Extracted at:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content.append(f"**Pages:** {len(reader.pages)}")
        content.append("\n---\n")

        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                content.append(f"## Page {i+1}")
                content.append(text)
                content.append("\n")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(content))

        print(f"Success: Saved to {output_path}")
        return True
    except Exception as e:
        print(f"Error converting {pdf_path}: {e}")
        return False

if __name__ == "__main__":
    KNOWLEDGE_DIR = "docs/knowledge"
    OUTPUT_DIR = "docs/knowledge"
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Specific files requested by user
    files_to_convert = [
        "AI-INTEGRATOR.pdf",
        "TOP-10%20avtomatizats%C4%B1i%20dlya%20pochatk%C4%B1vts%C4%B1v.pdf",
        "TOP-20%20sfer,%20de%20AI-avtomatizats%C4%B1ya%20zaraz%20naib%C4%B1ls%CC%A7e%20zatrebuvana.pdf"
    ]

    for f in files_to_convert:
        path = os.path.join(KNOWLEDGE_DIR, f)
        convert_pdf_to_md(path, OUTPUT_DIR)
