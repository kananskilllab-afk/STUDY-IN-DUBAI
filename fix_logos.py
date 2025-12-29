import os
import shutil
from PIL import Image, ImageOps
import numpy as np

src_dir = 'images/logos'
backup_dir = 'images/logos_backup'

if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

files = [f for f in os.listdir(src_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

print(f"Processing {len(files)} images...")

for f in files:
    src_path = os.path.join(src_dir, f)
    backup_path = os.path.join(backup_dir, f)
    
    # Backup
    if not os.path.exists(backup_path):
        shutil.copy2(src_path, backup_path)
    
    try:
        img = Image.open(src_path).convert('RGBA')
        arr = np.array(img)
        
        # Analyze
        alpha = arr[:,:,3]
        rgb = arr[:,:,:3]
        
        visible_mask = alpha > 0
        if np.sum(visible_mask) == 0:
            print(f"Skipping empty image: {f}")
            continue
            
        visible_pixels = rgb[visible_mask]
        
        # Brightness
        avg_brightness = np.mean(visible_pixels)
        
        # Saturation
        sat = np.max(visible_pixels, axis=1) - np.min(visible_pixels, axis=1)
        avg_sat = np.mean(sat)
        
        # Invert Logic
        should_invert = False
        
        # Check transparency ratio (0 = solid, 1 = invisible)
        transparency_ratio = np.sum(alpha == 0) / alpha.size
        
        if avg_sat < 30: # Low saturation (mostly gray)
            
            # Case 1: White/Light Text (Bright)
            if avg_brightness > 200:
                print(f"{f}: White/Light Logo (Brit={avg_brightness:.1f}). Inverting.")
                should_invert = True
                
            # Case 2: Solid Dark Background (Dark AND Solid)
            elif avg_brightness < 100 and transparency_ratio < 0.1:
                print(f"{f}: Black/Dark Background (Brit={avg_brightness:.1f}). Inverting.")
                should_invert = True
                
        # Process
        if should_invert:
            r,g,b,a = img.split()
            rgb_img = Image.merge('RGB', (r,g,b))
            inverted_rgb = ImageOps.invert(rgb_img)
            img = Image.merge('RGBA', (*inverted_rgb.split(), a))
        
        # Flatten to White Background
        background = Image.new('RGBA', img.size, (255, 255, 255, 255))
        final_img = Image.alpha_composite(background, img)
        final_img = final_img.convert('RGB') # Remove alpha
        
        # Save
        final_img.save(src_path)
        print(f"Propagated White BG to {f}")

    except Exception as e:
        print(f"Failed {f}: {e}")

print("Done.")
