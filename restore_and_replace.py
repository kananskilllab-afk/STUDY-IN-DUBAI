import shutil
import os

# 1. Restore Originals
backup_dir = 'images/logos_backup'
target_dir = 'images/logos'

print("Restoring original logos...")
if os.path.exists(backup_dir):
    for f in os.listdir(backup_dir):
        src = os.path.join(backup_dir, f)
        dst = os.path.join(target_dir, f)
        shutil.copy2(src, dst)
else:
    print("Warning: Backup directory not found!")

# 2. Apply Replacements (Accumulated Batches)
replacements = {
    # Batch 1
    "uploaded_image_0_1766971819752.png": "logo_1.png",   # Amity
    "uploaded_image_1_1766971819752.png": "logo_6.png",   # De Montfort
    "uploaded_image_2_1766971819752.png": "logo_10.png",  # Hult
    "uploaded_image_3_1766971819752.png": "logo_13.png",  # Middlesex
    
    # Batch 2
    "uploaded_image_0_1766972117255.png": "logo_4.png",   # Canadian
    "uploaded_image_1_1766972117255.png": "logo_5.png",   # Curtin
    "uploaded_image_2_1766972117255.png": "logo_9.png",   # Emirates Aviation
    "uploaded_image_3_1766972117255.png": "logo_16.png",  # Symbiosis

    # Batch 3
    "uploaded_image_0_1766972613617.png": "logo_20.png",  # Stirling
    "uploaded_image_1_1766972613617.png": "logo_18.png",  # University of Dubai
    "uploaded_image_2_1766972613617.png": "logo_19.png",  # UE
    "uploaded_image_3_1766972613617.png": "logo_21.png",  # West London
    "uploaded_image_4_1766972613617.png": "logo_22.png",  # Wollongong

    # Batch 4
    "uploaded_image_0_1766972858764.png": "logo_23.png",  # Westford
    "uploaded_image_1_1766972858764.png": "logo_26.png",  # Success Point
    "uploaded_image_2_1766972858764.png": "logo_27.png",  # RIT
    "uploaded_image_3_1766972858764.png": "logo_29.png",  # Woolwich
    "uploaded_image_4_1766972858764.png": "logo_31.png",  # UKCBC

    # Batch 5 (Current)
    "uploaded_image_0_1766973151476.png": "logo_33.png",  # Heriot-Watt
    "uploaded_image_1_1766973151476.png": "logo_34.png"   # Birmingham
}

source_base = r"C:/Users/mahim/.gemini/antigravity/brain/10be67a4-a85e-421a-866a-51808f2649d7"

print("\nAppling all logo replacements...")
for src_file, dest_file in replacements.items():
    src_path = os.path.join(source_base, src_file)
    dest_path = os.path.join(target_dir, dest_file)
    
    try:
        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
            print(f"Updated {dest_file}")
        else:
            print(f"Missing source: {src_file}")
    except Exception as e:
        print(f"Error updating {dest_file}: {e}")
