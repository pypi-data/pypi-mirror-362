import argparse
from PIL import Image
from rembg import remove
import sys
import io
import numpy as np
import cv2
import re

# Helper to parse color names/hex to BGR tuple
COLOR_NAME_TO_RGB = {
    'white': (255, 255, 255),
    'yellow': (255, 255, 0),
    'blue': (0, 0, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
    'black': (0, 0, 0),
}

def parse_color(color_str):
    color_str = color_str.lower()
    if color_str in COLOR_NAME_TO_RGB:
        rgb = COLOR_NAME_TO_RGB[color_str]
    elif re.match(r'^#?[0-9a-f]{6}$', color_str):
        hex_str = color_str.lstrip('#')
        rgb = tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
    else:
        raise ValueError(f"Invalid color: {color_str}")
    # Convert RGB to BGR for OpenCV
    return (rgb[2], rgb[1], rgb[0])

def enhance_face(
    input_path, output_path,
    brightness=1.08, contrast=8, saturation=1.10,
    smooth_d=7, smooth_sigma_color=60, smooth_sigma_space=60,
    sharpen=1.7, glow_size=25, glow_blur=16, glow_color="#FFFFFF"
):
    # Load image
    img = Image.open(input_path)

    # Remove background
    img_no_bg = remove(img)
    if isinstance(img_no_bg, bytes):
        img_no_bg = Image.open(io.BytesIO(img_no_bg))

    # Convert to OpenCV format (RGBA)
    img_cv = np.array(img_no_bg)
    if img_cv.shape[2] == 3:
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2RGBA)

    # Separate alpha channel
    bgr = img_cv[..., :3][..., ::-1]  # RGB to BGR
    alpha = img_cv[..., 3]

    # 1. Gentle brightness/contrast (avoid overexposure)
    bgr = cv2.convertScaleAbs(bgr, alpha=brightness, beta=contrast)

    # 2. Lowered saturation boost (convert to HSV)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] *= saturation
    hsv[..., 1] = np.clip(hsv[..., 1], 0, 255)
    bgr = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

    # 3. Skin smoothing (bilateral filter)
    bgr = cv2.bilateralFilter(bgr, d=smooth_d, sigmaColor=smooth_sigma_color, sigmaSpace=smooth_sigma_space)

    # 4. Sharpening (unsharp mask)
    gaussian = cv2.GaussianBlur(bgr, (0, 0), 1.2)
    sharpened = cv2.addWeighted(bgr, sharpen, gaussian, -(sharpen-1), 0)

    # 5. Final light sharpening pass
    final_gaussian = cv2.GaussianBlur(sharpened, (0, 0), 0.8)
    final_sharpened = cv2.addWeighted(sharpened, 1.15, final_gaussian, -0.15, 0)

    # 6. Color balance: reduce red, add blue/green
    balanced = final_sharpened.astype(np.float32)
    balanced[..., 2] *= 0.96  # Red channel (BGR order)
    balanced[..., 1] *= 1.02  # Green channel
    balanced[..., 0] *= 1.04  # Blue channel
    balanced = np.clip(balanced, 0, 255).astype(np.uint8)

    # Merge alpha back
    result = cv2.cvtColor(balanced, cv2.COLOR_BGR2RGBA)
    result[..., 3] = alpha

    # --- Add background glow ---
    mask = alpha.copy()
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (glow_size, glow_size))
    dilated = cv2.dilate(mask, kernel, iterations=1)
    glow_mask = cv2.GaussianBlur(dilated, (0, 0), glow_blur)
    # Parse glow color
    bgr_glow = parse_color(glow_color)
    # Create a colored RGBA background
    color_bg = np.zeros_like(result)
    color_bg[..., 0] = bgr_glow[0]
    color_bg[..., 1] = bgr_glow[1]
    color_bg[..., 2] = bgr_glow[2]
    color_bg[..., 3] = glow_mask
    # Composite: put colored glow behind the person
    fg = result.astype(np.float32) / 255.0
    bg = color_bg.astype(np.float32) / 255.0
    alpha_fg = fg[..., 3:4]
    alpha_bg = bg[..., 3:4] * (1 - alpha_fg)
    out_rgb = fg[..., :3] * alpha_fg + bg[..., :3] * alpha_bg
    out_alpha = alpha_fg + alpha_bg
    out = np.concatenate([out_rgb, out_alpha], axis=-1)
    out = np.clip(out * 255, 0, 255).astype(np.uint8)

    # Save result (preserve transparency)
    out_img = Image.fromarray(out)
    out_img.save(output_path)
    print(f"Enhanced image saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Enhance a face image for YouTube thumbnails with background removal and glow.")
    parser.add_argument('-i', '--input', required=True, help='Input image path')
    parser.add_argument('-b', '--brightness', type=float, default=1.08, help='Brightness/contrast alpha (default: 1.08)')
    parser.add_argument('-c', '--contrast', type=float, default=8, help='Brightness/contrast beta (default: 8)')
    parser.add_argument('-s', '--saturation', type=float, default=1.10, help='Saturation multiplier (default: 1.10)')
    parser.add_argument('--smooth_d', type=int, default=7, help='Bilateral filter diameter (default: 7)')
    parser.add_argument('--smooth_sigma_color', type=float, default=60, help='Bilateral filter sigmaColor (default: 60)')
    parser.add_argument('--smooth_sigma_space', type=float, default=60, help='Bilateral filter sigmaSpace (default: 60)')
    parser.add_argument('--sharpen', type=float, default=1.7, help='Sharpening strength (default: 1.7)')
    parser.add_argument('--glow_size', type=int, default=25, help='Glow dilation kernel size (default: 25)')
    parser.add_argument('--glow_blur', type=float, default=16, help='Glow blur sigma (default: 16)')
    parser.add_argument('--glow_color', type=str, default="#FFFFFF", help='Glow color (hex or name, default: #FFFFFF)')
    parser.add_argument('output', help='Output image path (required, always last argument)')
    args = parser.parse_args()

    enhance_face(
        input_path=args.input,
        output_path=args.output,
        brightness=args.brightness,
        contrast=args.contrast,
        saturation=args.saturation,
        smooth_d=args.smooth_d,
        smooth_sigma_color=args.smooth_sigma_color,
        smooth_sigma_space=args.smooth_sigma_space,
        sharpen=args.sharpen,
        glow_size=args.glow_size,
        glow_blur=args.glow_blur,
        glow_color=args.glow_color
    )

if __name__ == "__main__":
    main() 