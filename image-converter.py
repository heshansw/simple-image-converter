import sys
import os
import tempfile
import shutil
import numpy as np
import icnsutil
from PIL import Image, ImageChops, ImageFilter, ImageOps

def create_squircle_mask(size, power=4.5):
    """
    Generates a mathematically accurate Apple Squircle (Superellipse).
    macOS icons use a power (n) between 4 and 5 for continuous curvature.
    """
    size = max(1, size)
    sampling = 4  # Oversampling for smooth anti-aliased edges
    actual_size = size * sampling
    res = np.linspace(-1, 1, actual_size)
    x, y = np.meshgrid(res, res)
    
    # Formula: |x|^n + |y|^n <= 1
    mask_array = (np.abs(x)**power + np.abs(y)**power <= 1.0)
    
    mask = Image.fromarray((mask_array * 255).astype(np.uint8), mode='L')
    return mask.resize((size, size), Image.Resampling.LANCZOS)

def apply_mac_rounded_corners(logo_img, canvas_size):
    """
    Applies squircle rounding with a 7% opacity dark grey shadow.
    Maintains the 82% safe-area proportions of the macOS grid.
    """
    # 1. Scaling: 82% of canvas for the icon body (creates the 'outer space')
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

    # 4. Refined Dark Grey Shadow (7% Opacity)
    # Tight blur and subtle offset to match the provided 'F' logo
    shadow_offset = max(1, int(canvas_size * 0.012)) 
    shadow_blur = max(1, int(canvas_size * 0.012))   
    
    shadow_mask_size = content_size + (shadow_blur * 4)
    shadow_mask = Image.new('L', (shadow_mask_size, shadow_mask_size), 0)
    shadow_mask.paste(mask, (shadow_blur * 2, shadow_blur * 2))
    shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(shadow_blur))
    
    # Color: Dark Grey (80, 80, 80) | Alpha: 18 (7% opacity)
    shadow = Image.new('RGBA', (shadow_mask_size, shadow_mask_size), (80, 80, 80, 18))
    shadow.putalpha(shadow_mask)

    # 5. Final Assembly
    final_canvas = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))
    
    # Paste Shadow with downward shift
    shadow_pos = (
        (canvas_size - shadow.width) // 2, 
        ((canvas_size - shadow.height) // 2) + shadow_offset
    )
    final_canvas.paste(shadow, shadow_pos, mask=shadow)
    
    # Paste Rounded Logo centered
    logo_pos = ((canvas_size - content_size) // 2, (canvas_size - content_size) // 2)
    final_canvas.paste(logo_resized, logo_pos, mask=logo_resized)
    
    return final_canvas

def convert_image(input_path, mode, size_val, brand_name=None):
    # Sanitize path to remove null bytes and extra quotes
    input_path = "".join(c for c in input_path if c != '\0').strip("'").strip('"')
    abs_input_path = os.path.abspath(input_path)
    
    try:
        if not os.path.exists(abs_input_path):
            print(f"Error: File not found at {abs_input_path}")
            return

        # Naming logic
        filename_base = brand_name.lower().replace(" ", "-") if brand_name else os.path.splitext(os.path.basename(abs_input_path))[0]
        output_dir = os.path.dirname(abs_input_path)
        
        # Load image and normalize to a square canvas
        raw_img = Image.open(abs_input_path).convert('RGBA')
        max_side = max(raw_img.size)
        square_logo = Image.new('RGBA', (max_side, max_side), (0, 0, 0, 0))
        square_logo.paste(raw_img, ((max_side - raw_img.width)//2, (max_side - raw_img.height)//2))

        target_size = int(size_val) if size_val else 1024

        if mode == '-svg':
            output_file = os.path.join(output_dir, f"{filename_base}.svg")
            temp_png = os.path.join(output_dir, f"{filename_base}_temp.png")
            try:
                img = Image.open(abs_input_path)
                img.convert('RGBA').save(temp_png, 'PNG')
                print(f"Tracing {brand_name or 'image'} to SVG...")
                vtracer.convert_image_to_svg_py(
                    str(temp_png), 
                    str(output_file),
                    colormode='color',
                    hierarchical='cutout',
                    mode='spline',
                    filter_speckle=4,
                    color_precision=6,
                    layer_difference=16
                )
                print(f"Successfully created: {output_file}")
            finally:
                if os.path.exists(temp_png):
                    os.remove(temp_png)
        elif mode == '-mac-png':
            try:
                size = int(size_or_output) if size_or_output else 512
            except:
                size = 512
                
            output_file = os.path.join(output_dir, f"{filename_base}_mac_{size}.png")
            img = Image.open(abs_input_path)
            
            if img.mode != 'RGBA':
                img = img.convert('RGBA')

            # Maintain proportions with 82% coverage for macOS squircle safe area
            logo_size = int(size * 0.82)
            img.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            canvas = Image.new("RGBA", (size, size), (255, 255, 255, 0))
            offset = ((size - img.width) // 2, (size - img.height) // 2)
            canvas.paste(img, offset, mask=img)
            
            canvas.save(output_file, "PNG")
            print(f"Successfully created {brand_name or 'Mac'} PNG ({size}x{size}): {output_file}")
        elif mode == '-mac-png-rounded':
            output_file = os.path.join(output_dir, f"{filename_base}_mac_rounded.png")
            final_icon = apply_mac_rounded_corners(square_logo, target_size)
            final_icon.save(output_file, "PNG")
            print(f"✓ Created precision-shaded icon: {output_file}")
        elif mode in ['-win', '-mac']:
            img = Image.open(abs_input_path)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            try:
                size = int(size_or_output) if size_or_output else 256
            except:
                size = 256

            if mode == '-win':
                output_file = os.path.join(output_dir, f"{filename_base}.ico")
                sizes = [(16, 16), (32, 32), (48, 48), (size, size)]
                img.save(output_file, format='ICO', sizes=sizes)
                print(f"Successfully created {brand_name or 'Windows'} icon: {output_file}")

            elif mode == '-mac':
                output_file = os.path.join(output_dir, f"{filename_base}.icns")
                img_icns = icnsutil.IcnsFile()
                
                # macOS icon sizes with proper retina naming
                icon_specs = [
                    (16, "icon_16x16.png"),
                    (32, "icon_16x16@2x.png"),
                    (32, "icon_32x32.png"),
                    (64, "icon_32x32@2x.png"),
                    (128, "icon_128x128.png"),
                    (256, "icon_128x128@2x.png"),
                    (256, "icon_256x256.png"),
                    (512, "icon_256x256@2x.png"),
                    (512, "icon_512x512.png"),
                    (1024, "icon_512x512@2x.png"),
                ]
                
                # Use temp directory for intermediate PNG files
                temp_dir = tempfile.mkdtemp()
                try:
                    used_names = set()
                    for s, name in icon_specs:
                        if s <= img.width or s <= size:
                            if name not in used_names:
                                resized = img.resize((s, s), Image.Resampling.LANCZOS)
                                temp_png = os.path.join(temp_dir, name)
                                resized.save(temp_png, "PNG")
                                img_icns.add_media(file=temp_png)
                                used_names.add(name)
                    
                    img_icns.write(output_file)
                    print(f"Successfully created {brand_name or 'macOS'} .icns: {output_file}")
                finally:
                    # Clean up temp directory
                    shutil.rmtree(temp_dir, ignore_errors=True)
        else:
            print("Invalid mode. Use -mac-png-rounded for the rounded PNG output.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python script.py <file_path> -mac-png-rounded <size> <brand_name>")
    else:
        size_val = sys.argv[3] if len(sys.argv) > 3 else None
        brand = sys.argv[4] if len(sys.argv) > 4 else None
        convert_image(sys.argv[1], sys.argv[2], size_val, brand)