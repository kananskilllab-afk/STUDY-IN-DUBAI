import os
from PIL import Image
import numpy as np

logo_dir = 'images/logos'
files = sorted([f for f in os.listdir(logo_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

print("Checking for dark backgrounds...")
for f in files:
    path = os.path.join(logo_dir, f)
    try:
        img = Image.open(path).convert('RGBA')
        arr = np.array(img)
        
        alpha = arr[:,:,3]
        total_pixels = alpha.size
        transparent_pixels = np.sum(alpha == 0)
        transparency_ratio = transparent_pixels / total_pixels
        
        if transparency_ratio < 0.1: # Mostly solid
            visible_rgb = arr[:,:,:3] # All pixels roughly
            avg_brightness = np.mean(visible_rgb)
            
            if avg_brightness < 50: # Very dark
                print(f"DARK_BG_FOUND: {f} (Brit: {avg_brightness:.1f})")
                
    except Exception:
        pass
