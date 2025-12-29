import PyPDF2
from PIL import Image
import os

def extract_images_better(pdf_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    reader = PyPDF2.PdfReader(pdf_path)
    count = 0

    for page_num, page in enumerate(reader.pages):
        try:
            if '/Resources' not in page:
                continue
            xobjects = page['/Resources'].get('/XObject')
            if not xobjects:
                continue
            xobjects = xobjects.get_object()

            for obj_name in xobjects:
                obj = xobjects[obj_name]
                if hasattr(obj, 'get_object'):
                    obj = obj.get_object()

                if obj.get('/Subtype') == '/Image':
                    filters = obj.get('/Filter', [])
                    # Ensure filters is a listing
                    if isinstance(filters, str): # Legacy/Single name
                        filters = [filters]
                    elif hasattr(filters, 'get_object'): # Indirect object
                         filters = [filters.get_object()] # Simplified
                        
                    width = obj.get('/Width')
                    height = obj.get('/Height')
                    
                    try:
                        data = obj.get_data()
                    except Exception as e:
                        print(f"Failed get_data for {obj_name}: {e}")
                        continue

                    if '/DCTDecode' in filters:
                        with open(os.path.join(output_dir, f"logo_{count}.jpg"), "wb") as f:
                            f.write(data)
                        print(f"Saved logo_{count}.jpg (JPEG)")
                        count += 1
                        
                    elif '/FlateDecode' in filters:
                        # Reconstruct image
                        color_space = obj.get('/ColorSpace')
                        if hasattr(color_space, 'get_object'):
                            color_space = color_space.get_object()
                            
                        mode = "RGB" # Default
                        if color_space == '/DeviceCMYK':
                            mode = "CMYK"
                        elif color_space == '/DeviceGray':
                            mode = "L"
                        elif isinstance(color_space, list) and len(color_space) > 0 and color_space[0] == '/ICCBased':
                             mode = "RGB" # Simplified assumption
                        
                        try:
                            img = Image.frombytes(mode, (width, height), data)
                            img.save(os.path.join(output_dir, f"logo_{count}.png"))
                            print(f"Saved logo_{count}.png ({mode})")
                            count += 1
                        except Exception as e:
                            print(f"Failed to reconstruct FlateDecode image {obj_name}: {e}")
        except Exception as e:
            print(f"Page error: {e}")

if __name__ == "__main__":
    extract_images_better("UNIVERSITIES LOGOS.pdf", "logos")
