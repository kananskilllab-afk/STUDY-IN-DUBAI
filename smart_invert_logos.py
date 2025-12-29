import os
import shutil
from PIL import Image
import numpy as np
import colorsys

logo_dir = 'images/logos'
backup_dir = 'images/logos_original' # Use original backup

files = sorted([f for f in os.listdir(logo_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

print(f"Scanning {len(files)} images for Dark Backgrounds...")

for f in files:
    path = os.path.join(logo_dir, f)
    try:
        img = Image.open(path).convert('RGB')
        arr = np.array(img)
        
        # Check corners to detect background color
        h, w, _ = arr.shape
        corners = [
            arr[0, 0], arr[0, w-1],
            arr[h-1, 0], arr[h-1, w-1]
        ]
        avg_corner = np.mean(corners, axis=0)
        avg_corner_bri = np.mean(avg_corner) # brightness component
        
        if avg_corner_bri < 50: # Dark Background Detected
            print(f"Processing {f}: Dark BG detected (Brit={avg_corner_bri:.1f})")
            
            # Smart Invert: Invert Lightness (Value) of Low-Saturation pixels
            # 1. Convert to float 0-1
            arr_norm = arr.astype(float) / 255.0
            
            # 2. Iterate pixels (vectorized manual HSV conversion is hard, using simpler logic)
            # Actually, separating into HSV is best.
            # Using PIL HSV support might be easier but it doesn't give float precision easily.
            # Let's do pixel-wise or simplified array math.
            
            # Vectorized approach:
            r, g, b = arr_norm[:,:,0], arr_norm[:,:,1], arr_norm[:,:,2]
            
            # Value (Brightness) = max(r,g,b)
            v = np.max(arr_norm, axis=2)
            
            # Chroma = max - min
            c = v - np.min(arr_norm, axis=2)
            
            # Saturation: if v=0, s=0, else c/v
            with np.errstate(divide='ignore', invalid='ignore'):
                s = np.where(v == 0, 0, c / v)
                
            # Mask: Low Saturation (Gray/White/Black)
            # Threshold: 0.2 (20%)
            low_sat_mask = s < 0.2
            
            # Invert Logic for Low Saturation Pixels:
            # We want to map Brightness 0 -> 1 (White) and 1 -> 0 (Black).
            # Current Brightness is 'v'.
            # We also need to preserve RGB ratios if it's not perfectly gray, 
            # but if it's low sat, it's mostly gray.
            # Simple Inversion: New_RGB = 1.0 - RGB.
            # This works for Black(0)->White(1) and White(1)->Black(0).
            # And Gray(0.5)->Gray(0.5).
            
            # Apply inversion only to low_sat_mask
            arr_norm[low_sat_mask] = 1.0 - arr_norm[low_sat_mask]
            
            # What about High Saturation pixels? (Colors)
            # Keeping them as-is on a new White background might result in low contrast 
            # if they were "Light Colors on Dark". (e.g. Yellow on Black).
            # Yellow on White is hard to see.
            # But "University of Dubai" is Dark Blue on Black. Blue on White is good.
            # "Europe" is Red on Black. Red on White is good.
            # "Westford" Cyan on Black. Cyan on White is okay-ish.
            
            # Let's start with just Low-Sat Inversion.
            
            # Convert back to uint8
            res_arr = (arr_norm * 255).clip(0, 255).astype(np.uint8)
            res_img = Image.fromarray(res_arr)
            
            res_img.save(path)
            print("  -> Applied Smart Invert.")
            
    except Exception as e:
        print(f"Error {f}: {e}")
