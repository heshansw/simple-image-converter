import sys
import os
import numpy as np
from PIL import Image, ImageChops, ImageFilter, ImageOps
import icnsutil

def create_squircle_mask(size, power=4.5):
    """Generates the mathematically accurate Apple Squircle shape."""
    size = max(1, size)
    sampling = 4 
    actual_size = size * sampling
    res = np.linspace(-1, 1, actual_size)
    x, y = np.meshgrid(res, res)
    mask_array = (np.abs(x)**power + np.abs(y)**power <= 1.0)
    mask = Image.fromarray((mask_array * 255).astype(np.uint8), mode='L')
    return mask.resize((size, size), Image.Resampling.LANCZOS)

def apply_mac_rounded_corners(logo_img, canvas_size):
    """
    Applies squircle rounding with a 7% opacity dark grey shadow.
    Dark grey provides better definition than light grey without the harshness of black.
    """
    # 1. Scaling: 82% Safe Area (Standard macOS App Icon Proportion)
    content_size = max(1, int(canvas_size * 0.82))
    logo_resized = logo_img.resize((content_size, content_size), Image.Resampling.LANCZOS)
    
    # 2. Create the Squircle Mask
    mask = create_squircle_mask(content_size)
    
    # 3. Apply mask to logo alpha channel
    if 'A' in logo_resized.getbands():
        orig_alpha = logo_resized.getchannel('A')
        combined_alpha = ImageChops.darker(orig_alpha, mask)
        logo_resized.putalpha(combined_alpha)
    else:
        logo_resized.putalpha(mask)

    # 4. Dark Grey Shadow (7% Opacity)
    shadow_offset = max(1, int(canvas_size * 0.012)) 
    shadow_blur = max(1, int(canvas_size * 0.012))   
    
    shadow_mask_size = content_size + (shadow_blur * 4)
    shadow_mask = Image.new('L', (shadow_mask_size, shadow_mask_size), 0)
    shadow_mask.paste(mask, (shadow_blur * 2, shadow_blur * 2))
    shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(shadow_blur))
    
    # COLOR ADJUSTMENT: Darker grey (80, 80, 80)
    # OPACITY: Alpha 18 (7% of 255)
    shadow = Image.new('RGBA', (shadow_mask_size, shadow_mask_size), (80, 80, 80, 18))
    shadow.putalpha(shadow_mask)

    # 5. Final Assembly (Centered for perfect spacing)
    final_canvas = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))
    
    # Paste Shadow with downward offset
    shadow_pos = (
        (canvas_size - shadow.width) // 2, 
        ((canvas_size - shadow.height) // 2) + shadow_offset
    )
    final_canvas.paste(shadow, shadow_pos, mask=shadow)
    
    # Paste Logo Body centered
    logo_pos = ((canvas_size - content_size) // 2, (canvas_size - content_size) // 2)
    final_canvas.paste(logo_resized, logo_pos, mask=logo_resized)
    
    return final_canvas

def convert_image(input_path, mode, size_val, brand_name=None):
    try:
        abs_input_path = os.path.abspath(input_path.strip().strip("'").strip('"'))
        filename_base = brand_name.lower().replace(" ", "-") if brand_name else os.path.splitext(os.path.basename(abs_input_path))[0]
        output_dir = os.path.dirname(abs_input_path)
        
        raw_img = Image.open(abs_input_path).convert('RGBA')
        
        # Normalize to square canvas to prevent distortion
        max_side = max(raw_img.size)
        square_logo = Image.new('RGBA', (max_side, max_side), (0, 0, 0, 0))
        square_logo.paste(raw_img, ((max_side - raw_img.width)//2, (max_side - raw_img.height)//2))

        target_size = int(size_val) if size_val else 1024

        if mode == '-mac-png-rounded':
            output_file = os.path.join(output_dir, f"{filename_base}_mac_rounded.png")
            final_icon = apply_mac_rounded_corners(square_logo, target_size)
            final_icon.save(output_file, "PNG")
            print(f"✓ Created icon with darker grey 7% shading: {output_file}")

        elif mode == '-mac':
            output_file = os.path.join(output_dir, f"{filename_base}.icns")
            icns = icnsutil.IcnsFile()
            for s in [16, 32, 64, 128, 256, 512, 1024]:
                layer = apply_mac_rounded_corners(square_logo, s)
                icns.add_media(file=layer)
            icns.write(output_file)
            print(f"✓ Created .icns with darker grey 7% shading: {output_file}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <file> <mode> <size> <brand>")
    else:
        size_val = sys.argv[3] if len(sys.argv) > 3 else None
        brand = sys.argv[4] if len(sys.argv) > 4 else None
        convert_image(sys.argv[1], sys.argv[2], size_val, brand)