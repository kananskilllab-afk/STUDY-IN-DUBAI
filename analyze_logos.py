import os
from PIL import Image
import numpy as np

logo_dir = 'images/logos'
files = sorted([f for f in os.listdir(logo_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

print(f"Found {len(files)} images.")

for f in files:
    path = os.path.join(logo_dir, f)
    try:
        img = Image.open(path).convert('RGBA')
        arr = np.array(img)
        
        # Analyze Alpha
        alpha = arr[:,:,3]
        total_pixels = alpha.size
        transparent_pixels = np.sum(alpha == 0)
        transparency_ratio = transparent_pixels / total_pixels
        
        # Analyze Visible Pixels
        visible_mask = alpha > 0
        if np.sum(visible_mask) == 0:
            print(f"{f}: Empty/Fully Transparent")
            continue
            
        visible_rgb = arr[visible_mask][:, :3]
        avg_brightness = np.mean(visible_rgb)
        
        # Check for white-on-transparent
        # Brightness > 200 considered "light"
        is_light = avg_brightness > 200
        
        # Check for black background (no alpha or low alpha usage but corners are black)
        # Actually checking if it's solid rect with black bg
        
        report = f"{f}: Transp={transparency_ratio:.2f}, Brit={avg_brightness:.1f}"
        
        if is_light and transparency_ratio > 0.1:
            report += " -> LIKELY WHITE LOGO (Needs Invert on White BG)"
        elif avg_brightness < 50 and transparency_ratio < 0.1:
            report += " -> LIKELY DARK/BLACK BG (Needs cleanup?)"
            
        print(report)
        
    except Exception as e:
        print(f"Error processing {f}: {e}")
