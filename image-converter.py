import sys
import os
from PIL import Image, ImageOps
import icnsutil
import vtracer

def convert_image(input_path, mode, size_or_output, brand_name=None):
    try:
        clean_input = input_path.strip().strip("'").strip('"')
        abs_input_path = os.path.abspath(clean_input)
        
        if not os.path.exists(abs_input_path):
            print(f"Error: File not found at: {abs_input_path}")
            return

        # Use brand name for filename if provided, otherwise use original filename
        if brand_name:
            filename_base = brand_name.lower().replace(" ", "-")
        else:
            filename_base = os.path.splitext(os.path.basename(abs_input_path))[0]
        
        # Determine output directory (same as input file)
        output_dir = os.path.dirname(abs_input_path)

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
                mac_sizes = [16, 32, 64, 128, 256, 512, 1024]
                for s in mac_sizes:
                    if s <= img.width or s <= size:
                        resized = img.resize((s, s), Image.Resampling.LANCZOS)
                        img_icns.add_media(file=resized)
                img_icns.write(output_file)
                print(f"Successfully created {brand_name or 'macOS'} .icns: {output_file}")
        else:
            print("Invalid mode. Use -win, -mac, -mac-png, or -svg.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python image-converter.py <image> <mode> <size> <brand_name>")
        print("\nModes:")
        print("  -win      (Windows ICO)")
        print("  -mac      (macOS ICNS)")
        print("  -mac-png  (macOS App PNG)")
        print("  -svg      (Vector Tracing)")
        print("\nExample:")
        print("  python image-converter.py logo.png -mac-png 512 TechTell")
    else:
        size_val = sys.argv[3] if len(sys.argv) > 3 else None
        brand = sys.argv[4] if len(sys.argv) > 4 else None
        convert_image(sys.argv[1], sys.argv[2], size_val, brand)