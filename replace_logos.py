import shutil
import os

# Define mappings
replacements = {
    "uploaded_image_0_1766971819752.png": "logo_1.png",   # Amity
    "uploaded_image_1_1766971819752.png": "logo_6.png",   # De Montfort
    "uploaded_image_2_1766971819752.png": "logo_10.png",  # Hult
    "uploaded_image_3_1766971819752.png": "logo_13.png"   # Middlesex
}

source_dir = r"C:/Users/mahim/.gemini/antigravity/brain/10be67a4-a85e-421a-866a-51808f2649d7"
dest_dir = "images/logos"

print("Replacing logos...")
for src_file, dest_file in replacements.items():
    src_path = os.path.join(source_dir, src_file)
    dest_path = os.path.join(dest_dir, dest_file)
    
    try:
        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
            print(f"Replaced {dest_file} with {src_file}")
        else:
            print(f"Source not found: {src_path}")
    except Exception as e:
        print(f"Error copying {src_file}: {e}")
