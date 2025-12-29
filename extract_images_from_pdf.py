import PyPDF2
import os

def extract_images(pdf_path, output_dir):
    try:
        reader = PyPDF2.PdfReader(pdf_path)
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        count = 0
        for i, page in enumerate(reader.pages):
            for image_file_object in page.images:
                with open(os.path.join(output_dir, f"logo_{count}_{image_file_object.name}"), "wb") as fp:
                    fp.write(image_file_object.data)
                count += 1
                
        print(f"Successfully extracted {count} images to {output_dir}")
        
    except Exception as e:
        print(f"Error extracting images: {e}")

if __name__ == "__main__":
    extract_images("UNIVERSITIES LOGOS.pdf", "logos")
