import os
from PIL import Image, ImageOps, ImageDraw

def fix_asset_health_image():
    img_path = "docs/images/asset_health_cv_workflow.png"
    if not os.path.exists(img_path):
        print(f"File {img_path} not found.")
        return

    orig_img = Image.open(img_path).convert("RGBA")
    w, h = orig_img.size
    print(f"Original image size: {w}x{h}")

    # Create a padded 16:9 canvas with light cream background matching the whiteboard doodle style (#FAF7EE)
    padding_x = int(w * 0.15)
    padding_y = int(h * 0.15)
    
    new_w = w + (padding_x * 2)
    new_h = h + (padding_y * 2)
    
    # Cream background color from doodle diagrams: #FAF7EE
    bg_color = (250, 247, 238, 255)
    
    # Create canvas
    canvas = Image.new("RGBA", (new_w, new_h), bg_color)
    
    # Paste original image in center
    canvas.paste(orig_img, (padding_x, padding_y), orig_img)
    
    # Resize to standard high-res 1200x850 for markdown display
    target_w = 1200
    aspect = new_h / new_w
    target_h = int(target_w * aspect)
    
    resized_canvas = canvas.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    resized_canvas.save("docs/images/asset_health_cv_workflow.png")
    print(f"Successfully padded and scaled docs/images/asset_health_cv_workflow.png to {target_w}x{target_h}!")

if __name__ == "__main__":
    fix_asset_health_image()
