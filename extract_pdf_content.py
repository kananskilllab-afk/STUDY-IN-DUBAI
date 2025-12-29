import PyPDF2
import json

def extract_pdf_content(pdf_path):
    """Extract text content from each page of the PDF"""
    content = {}
    
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        total_pages = len(reader.pages)
        
        print(f"Total pages in PDF: {total_pages}\n")
        print("="*80)
        
        for page_num in range(total_pages):
            page = reader.pages[page_num]
            text = page.extract_text()
            
            content[f"Page_{page_num + 1}"] = text
            
            print(f"\n--- PAGE {page_num + 1} ---")
            print(text)
            print("="*80)
            
            # Check for images
            if '/XObject' in page['/Resources']:
                xobjects = page['/Resources']['/XObject'].get_object()
                images_count = sum(1 for obj in xobjects if xobjects[obj]['/Subtype'] == '/Image')
                if images_count > 0:
                    print(f"[IMAGES DETECTED: {images_count} image(s) on this page]")
                    print("="*80)
    
    # Save to JSON file
    with open('pdf_content.json', 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)
    
    print(f"\n\nContent saved to pdf_content.json")

if __name__ == "__main__":
    extract_pdf_content("Your_Global_Career_Starts_in_Dubai.pdf")
