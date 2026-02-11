**Note:** Currently this is vibecoded and i am planning to change this to agentic coding approach as a more proper structured project 

# Image Converter

A professional Python-based CLI tool for converting brand assets into platform-specific icon formats and high-fidelity vectors. This tool is optimized for **Windows**, **macOS**, and **Web** development workflows.

## 🚀 Features

* **Windows Icon (`.ico`)**: Creates Windows 11-style icons with subtle rounded corners (8% radius) at 100% coverage for modern, professional app icons at any size.
* **macOS App PNG (`-mac-png`)**: Generates a high-resolution PNG with an 82% scale factor to ensure the logo sits perfectly within the macOS "Squircle" safe area.
* **macOS App PNG with Squircle Rounded Corners (`-mac-png-rounded`)**: Applies mathematically accurate Apple squircle mask with 82% coverage and subtle shadow - perfect for App Store submissions.
* **macOS Icon (`.icns`)**: Creates native Apple Icon Image files containing the full standard iconset (16px to 1024px) with proper retina naming conventions.
* **Vector Tracing (`.svg`)**: Converts raster pixels into mathematical paths using the Rust-powered `vtracer` engine, preventing pixelation at any scale. Default 64px (favicon size) with configurable dimensions.
* **Smart Format Detection**: Automatically handles misnamed files (e.g., ICO files with .png extension) by converting to proper PNG before processing.
* **Brand-First Naming**: Optional brand name parameter to automatically format and name your output files (e.g., `test_mac_512.png`).

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
| `-svg` | Vector trace to SVG | `.svg` | 64 |
| `-win` | Windows 11 icon with rounded corners | `.ico` | 256 |
| `-mac` | macOS icon bundle | `.icns` | 256 |
| `-mac-png` | macOS app PNG with safe area | `.png` | 512 |
| `-mac-png-rounded` | macOS app PNG with squircle mask & shadow | `.png` | 1024 |

### Examples

#### Convert to SVG (Default 64px for favicon size)
```bash
python image-converter.py ./originalimages/logo.png -svg
```
Output: `logo.svg` (64×64 vector traced version). This conversion will happen without any pixelations

#### Convert to SVG with Custom Size
```bash
python image-converter.py ./originalimages/logo.png -svg 128
```
Output: `logo.svg` (128×128 vector traced version)

#### Convert to SVG with Brand Name
```bash
python image-converter.py ./originalimages/company-logo.png -svg 64 "Company Logo"
```
Output: `company-logo.svg`

#### Create Windows Icon with Rounded Corners (256×256)
```bash
python image-converter.py ./originalimages/logo.png -win 256
```
Output: `logo.ico` (256×256 with Windows 11-style rounded corners at 8% radius, 100% coverage)

#### Create Windows Icon with Custom Size
```bash
python image-converter.py ./originalimages/logo.png -win 512
```
Output: `logo.ico` (512×512 with rounded corners)

#### Create macOS Icon Bundle
```bash
python image-converter.py ./originalimages/logo.png -mac 1024
```
Output: `logo.icns` (contains all macOS icon sizes from 16×16 up to 1024×1024)

#### Create macOS App PNG with Brand Name
```bash
python image-converter.py ./originalimages/logo.png -mac-png 512 "Test"
```
Output: `test_mac_512.png` (512×512 with logo centered at 82% size)

#### Create macOS App PNG with Squircle Rounded Corners
```bash
python image-converter.py ./originalimages/logo.png -mac-png-rounded 1024
```
Output: `logo_mac_rounded.png` (1024×1024 with mathematically accurate Apple squircle mask, 82% coverage, and subtle shadow)

**Apple Squircle Technology:** Uses superellipse formula (|x|^4.5 + |y|^4.5 ≤ 1) for continuous curvature matching macOS design standards, with 7% opacity shadow for depth.

### Parameters

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| `<image>` | ✅ Yes | Path to input image file | - |
| `<mode>` | ✅ Yes | Conversion mode (`-svg`, `-win`, `-mac`, `-mac-png`, `-mac-png-rounded`) | - |
| `[size]` | ⬜ No | Maximum output size in pixels | 64 (svg), 256 (win/mac), 512 (mac-png), 1024 (mac-png-rounded) |
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

### macOS PNG with Squircle Rounded Corners (`-mac-png-rounded`)
When using `-mac-png-rounded` mode, the tool:
1. Creates a transparent canvas of the specified size (default 1024×1024)
2. Resizes the logo to **82% of canvas size** (macOS safe area)
3. Applies **mathematically accurate Apple squircle** mask using superellipse formula (power=4.5)
4. Adds **subtle shadow** (7% opacity, dark grey) for depth
5. Centers the logo on the canvas

This mode is ideal for:
- App Store icon submissions requiring Apple's squircle specification
- Creating professional macOS app icons with accurate curvature
- Ensuring consistency with macOS system icons

### Windows Icon with Rounded Corners (`-win`)
When using `-win` mode, the tool:
1. Creates a transparent canvas of the specified size (default 256×256)
2. Resizes the logo to **100% coverage** for maximum visibility
3. Applies **Windows 11-style rounded corners** with 8% radius
4. Saves as a single-size ICO file

This mode creates modern Windows 11-style app icons with professional rounded corners.

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
python image-converter.py ./originalimages/logo1.png -svg 64 "Company One"
python image-converter.py ./originalimages/logo2.png -svg 64 "Company Two"
python image-converter.py ./originalimages/logo3.png -svg 128 "Company Three"
```

### Create macOS App PNGs at Different Sizes
```bash
python image-converter.py logo.png -mac-png 512 "My App"
python image-converter.py logo.png -mac-png 1024 "My App"
python image-converter.py logo.png -mac-png-rounded 1024 "My App"
```

### Generate Complete Icon Set for Cross-Platform App
```bash
python image-converter.py logo.png -win 256
python image-converter.py logo.png -mac 1024
python image-converter.py logo.png -mac-png-rounded 1024
python image-converter.py logo.png -svg 64
```

## 📋 Icon Size Reference

### Windows Icon Sizes (`.ico`)
- **256×256 (default)** - Modern Windows 11 standard with rounded corners
- **512×512 or custom** - High DPI displays and large taskbar icons
- Uses 100% coverage with 8% corner radius for professional appearance

### macOS Icon Sizes (`.icns`)
- 16×16, 32×32 - Small UI elements
- 64×64, 128×128 - Standard icons
- 256×256, 512×512 - Retina displays
- 1024×1024 - High-resolution Retina displays

### macOS App Store Requirements
- Use `-mac-png 512` or `-mac-png 1024` for App Store submissions without rounded corners
- Use `-mac-png-rounded 1024` for App Store submissions with Apple's squircle specification
- 82% sizing ensures logo fits within Apple's rounded square mask
- Squircle uses superellipse formula (power=4.5) for continuous curvature matching Apple design standards

## 📄 License

This tool uses the following open-source libraries:
- **Pillow** (PIL Fork) - Python Imaging Library
- **icnsutil** - macOS ICNS file handling
- **vtracer** - Rust-powered vector tracing engine

Please refer to their respective licenses for usage terms.

## Vibe Coding Resources
- Google Gemini 3
- Github Copilot (Claude Sonnet 4.5)

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.
