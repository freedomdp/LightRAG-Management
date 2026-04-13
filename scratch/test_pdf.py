import fitz
import sys
import os

def test_fitz_extraction(pdf_path):
    if not os.path.exists(pdf_path):
        print("File not found")
        return
    
    doc = fitz.open(pdf_path)
    print(f"--- FITS EXTRACTION TEST: {os.path.basename(pdf_path)} ---")
    # Just print first page to see the difference
    page = doc[0]
    text = page.get_text("text") 
    print(text[:1000])

if __name__ == "__main__":
    test_fitz_extraction("/Users/sergej/StudioProjects/LightRAG/docs/knowledge/AI-INTEGRATOR.pdf")
