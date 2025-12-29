import PyPDF2
from PIL import Image
import io
import os

def extract_images_low_level(pdf_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    reader = PyPDF2.PdfReader(pdf_path)
    count = 0

    for page_num, page in enumerate(reader.pages):
        if '/Resources' not in page:
            continue
        
        resources = page['/Resources']
        if '/XObject' not in resources:
            continue
            
        xobjects = resources['/XObject']
        
        # We need to dereference the XObject if it's indirect
        # In PyPDF2 3.x, xobjects can be iterated directly if it's a dict, 
        # but likely we need to get the object.
        
        try:
            # xobjects might be an IndirectObject, get_object() gets the dict
            x_obj_dict = xobjects.get_object() 
        except Exception:
            # If it's not indirect, maybe it's already the dict
            x_obj_dict = xobjects

        for obj_name in x_obj_dict:
            try:
                obj = x_obj_dict[obj_name]
                # Dereference if needed
                if hasattr(obj, 'get_object'):
                    obj = obj.get_object()
                
                if obj.get('/Subtype') == '/Image':
                    
                    # Try to get data
                    try:
                        data = obj.get_data() # This usually returns bytes
                    except Exception as e:
                        print(f"Failed to get data for {obj_name}: {e}")
                        continue
                        
                    # Determine extension and save
                    # Note: PyPDF2's get_data() handles filters.
                    
                    filters = obj.get('/Filter', [])
                    if '/DCTDecode' in filters:
                        ext = ".jpg"
                        with open(os.path.join(output_dir, f"image_{count}{ext}"), "wb") as f:
                            f.write(data)
                    elif '/JPXDecode' in filters:
                        ext = ".jp2"
                        with open(os.path.join(output_dir, f"image_{count}{ext}"), "wb") as f:
                            f.write(data)
                    elif '/FlateDecode' in filters:
                        # This is likely a raw bitmap or PNG-like stream.
                        # We can try to use Pillow to open it.
                        try:
                            # We might need to construct the image from mode and size
                            width = obj.get('/Width')
                            height = obj.get('/Height')
                            color_space = obj.get('/ColorSpace')
                            
                            # Simple attempt: create image from bytes
                            # Usually requires knowing mode (RGB, CMYK, etc.)
                            # Since we don't want to overengineer, let's try reading as generic image if possible
                            # or just skip if too complex.
                            
                            # BUT, PyPDF2 has a helper now that we tried before. 
                            # If manual fails, let's just save raw and hope.
                            
                            # Let's try to let Pillow identify it if it has headers
                            img = Image.open(io.BytesIO(data))
                            img.save(os.path.join(output_dir, f"image_{count}.png"))
                            
                        except Exception as e:
                            print(f"Could not save FlateDecode image {obj_name} with Pillow: {e}")
                            # Fallback: just write bytes? Unlikely to work for FlateDecode without headers.
                            pass
                    else:
                        print(f"Unknown filter {filters} for {obj_name}")
                        continue
                        
                    print(f"Saved image_{count}")
                    count += 1
            except Exception as e:
                print(f"Error processing object {obj_name}: {e}")

if __name__ == "__main__":
    extract_images_low_level("UNIVERSITIES LOGOS.pdf", "logos")
