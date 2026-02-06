Note: Currently this is vibecoded and i am planning to change this to agentic coding approach as a more proper structured project 

# Image Converter

A professional Python-based CLI tool for converting brand assets into platform-specific icon formats and high-fidelity vectors. This tool is optimized for **Windows**, **macOS**, and **Web** development workflows.

## 🚀 Features

* **Windows Icon (`.ico`)**: Bundles multiple resolutions (16px, 32px, 48px, and custom) into a single file for crisp display across the Windows UI.
* **macOS App PNG (`-mac-png`)**: Generates a high-resolution PNG with an 82% scale factor to ensure the logo sits perfectly within the macOS "Squircle" safe area.
* **macOS Icon (`.icns`)**: Creates native Apple Icon Image files containing the full standard iconset (16px to 1024px).
* **Vector Tracing (`.svg`)**: Converts raster pixels into mathematical paths using the Rust-powered `vtracer` engine, preventing pixelation at any scale.
* **Smart Format Detection**: Automatically handles misnamed files (e.g., ICO files with .png extension) by converting to proper PNG before processing.
* **Brand-First Naming**: Optional brand name parameter to automatically format and name your output files (e.g., `tech-tell_mac_512.png`).

## 🛠️ Installation

### 1. Prerequisites
Ensure you have **Python 3.7+** installed. It is recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

The tool requires:
- `Pillow>=10.0.0` - Image processing library
- `icnsutil>=1.1.0` - macOS ICNS file creation
- `vtracer>=0.6.0` - Vector tracing for SVG conversion

## 📖 Usage

### Basic Syntax

```bash
python image-converter.py <image> <mode> [size] [brand_name]
```

### Modes

| Mode | Description | Output Format | Default Size |
|------|-------------|---------------|--------------|
| `-svg` | Vector trace to SVG | `.svg` | N/A |
| `-win` | Windows icon | `.ico` | 256 |
| `-mac` | macOS icon bundle | `.icns` | 256 |
| `-mac-png` | macOS app PNG with safe area | `.png` | 512 |

### Examples

#### Convert to SVG
```bash
python image-converter.py ./originalimages/logo.png -svg
```
Output: `logo.svg` (vector traced version). This conversion will happen without any pixelations

#### Convert to SVG with Brand Name
```bash
python image-converter.py ./originalimages/company-logo.png -svg "Company Logo"
```
Output: `company-logo.svg`

#### Create Windows Icon (256×256)
```bash
python image-converter.py ./originalimages/logo.png -win 256
```
Output: `logo.ico` (contains 16×16, 32×32, 48×48, and 256×256 sizes)

#### Create macOS Icon Bundle
```bash
python image-converter.py ./originalimages/logo.png -mac 1024
```
Output: `logo.icns` (contains all macOS icon sizes from 16×16 up to 1024×1024)

#### Create macOS App PNG with Brand Name
```bash
python image-converter.py ./originalimages/logo.png -mac-png 512 "Tech Tell"
```
Output: `tech-tell_mac_512.png` (512×512 with logo centered at 82% size)

### Parameters

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| `<image>` | ✅ Yes | Path to input image file | - |
| `<mode>` | ✅ Yes | Conversion mode (`-svg`, `-win`, `-mac`, `-mac-png`) | - |
| `[size]` | ⬜ No | Maximum output size in pixels | 256 (win/mac), 512 (mac-png) |
| `[brand_name]` | ⬜ No | Brand name for output filename | Original filename |

## 📂 Output Behavior

### File Naming
- **Without brand name**: Uses original filename
  - Input: `logo.png` → Output: `logo.svg`
- **With brand name**: Uses brand name (lowercase, spaces replaced with hyphens)
  - Input: `logo.png`, Brand: `"My Company"` → Output: `my-company.svg`

### Output Location
All output files are saved in the **same directory as the input file**.

### macOS PNG Sizing (`-mac-png`)
When using `-mac-png` mode, the tool:
1. Creates a transparent canvas of the specified size
2. Resizes the logo to **82% of canvas size** (maintains aspect ratio)
3. Centers the logo on the canvas
4. Ensures proper display in macOS app squircle masks and App Store requirements

## ⚙️ SVG Vector Tracing Settings

The SVG conversion uses the following optimized settings:
- **Color Mode**: Full color preservation
- **Hierarchical**: Cutout mode for proper layer handling
- **Spline Mode**: Smooth curves
- **Filter Speckle**: 4 (removes small artifacts)
- **Color Precision**: 6 (high color accuracy)
- **Layer Difference**: 16 (good layer separation)

## 🖼️ Supported Input Formats

- PNG (including misnamed ICO files with .png extension)
- JPG/JPEG
- ICO
- BMP
- GIF
- TIFF
- WebP
- And any format supported by Pillow

## 🔧 Troubleshooting

### "No image file found" Error
The tool automatically handles format mismatches (e.g., ICO files with .png extension) by converting to proper PNG before SVG tracing. If you still see this error, verify the file exists and is readable.

### File Permission Errors
Ensure you have write permissions in the directory containing your input image.

### Low Quality Output
- **For Windows/Mac icons**: Use high-resolution source images (at least 1024×1024 recommended)
- **For SVG**: Use images with clear, distinct colors for better vector tracing results

## 📚 Batch Processing Examples

### Convert Multiple Brand Logos to SVG
```bash
python image-converter.py ./originalimages/logo1.png -svg "Company One"
python image-converter.py ./originalimages/logo2.png -svg "Company Two"
python image-converter.py ./originalimages/logo3.png -svg "Company Three"
```

### Create macOS App PNGs at Different Sizes
```bash
python image-converter.py logo.png -mac-png 512 "My App"
python image-converter.py logo.png -mac-png 1024 "My App"
```

### Generate Complete Icon Set for Cross-Platform App
```bash
python image-converter.py logo.png -win 256
python image-converter.py logo.png -mac 1024
python image-converter.py logo.png -mac-png 512
python image-converter.py logo.png -svg
```

## 📋 Icon Size Reference

### Windows Icon Sizes (`.ico`)
- 16×16 - Small icons, list views
- 32×32 - Standard icons
- 48×48 - Large icons
- 256×256 (or custom) - High DPI displays

### macOS Icon Sizes (`.icns`)
- 16×16, 32×32 - Small UI elements
- 64×64, 128×128 - Standard icons
- 256×256, 512×512 - Retina displays
- 1024×1024 - High-resolution Retina displays

### macOS App Store Requirements
- Use `-mac-png 512` or `-mac-png 1024` for App Store submissions
- 82% sizing ensures logo fits within Apple's rounded square mask

## 📄 License

This tool uses the following open-source libraries:
- **Pillow** (PIL Fork) - Python Imaging Library
- **icnsutil** - macOS ICNS file handling
- **vtracer** - Rust-powered vector tracing engine

Please refer to their respective licenses for usage terms.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.
