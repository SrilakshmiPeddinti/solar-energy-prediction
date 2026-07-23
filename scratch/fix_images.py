import os
from PIL import Image, ImageDraw, ImageFont

# Ensure docs/images directory exists
os.makedirs("docs/images", exist_ok=True)

# 1. Create a hand-drawn doodle style logo (docs/images/logo.png)
def create_doodle_logo():
    width, height = 800, 240
    # Light cream background
    img = Image.new("RGBA", (width, height), (255, 253, 245, 255))
    draw = ImageDraw.Draw(img)

    # Soft pastel colors
    pink = (255, 204, 213, 255)
    mint = (204, 255, 221, 255)
    purple = (229, 204, 255, 255)

    # Draw rounded pastel boxes with sketchy double lines
    # Box 1: Mint
    draw.rounded_rectangle([30, 40, 230, 200], radius=20, fill=mint, outline=(20, 20, 20), width=3)
    draw.rounded_rectangle([33, 43, 227, 197], radius=18, outline=(20, 20, 20), width=2)

    # Box 2: Pink
    draw.rounded_rectangle([270, 40, 530, 200], radius=20, fill=pink, outline=(20, 20, 20), width=3)
    draw.rounded_rectangle([273, 43, 527, 197], radius=18, outline=(20, 20, 20), width=2)

    # Box 3: Purple
    draw.rounded_rectangle([570, 40, 770, 200], radius=20, fill=purple, outline=(20, 20, 20), width=3)
    draw.rounded_rectangle([573, 43, 767, 197], radius=18, outline=(20, 20, 20), width=2)

    # Try loading font or default
    try:
        font_large = ImageFont.truetype("arial.ttf", 36)
        font_sub = ImageFont.truetype("arial.ttf", 22)
    except:
        font_large = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Add text
    draw.text((70, 80), "☀️ SOLAR", fill=(20, 20, 20), font=font_large)
    draw.text((75, 130), "Prediction", fill=(50, 50, 50), font=font_sub)

    draw.text((320, 80), "🧠 PHYSICS AI", fill=(20, 20, 20), font=font_large)
    draw.text((345, 130), "Deep Engine", fill=(50, 50, 50), font=font_sub)

    draw.text((610, 80), "⚡ GRID", fill=(20, 20, 20), font=font_large)
    draw.text((615, 130), "VPP Analytics", fill=(50, 50, 50), font=font_sub)

    # Connecting arrows
    draw.line([(230, 120), (270, 120)], fill=(20, 20, 20), width=4)
    draw.polygon([(270, 120), (260, 112), (260, 128)], fill=(20, 20, 20))

    draw.line([(530, 120), (570, 120)], fill=(20, 20, 20), width=4)
    draw.polygon([(570, 120), (560, 112), (560, 128)], fill=(20, 20, 20))

    img.save("docs/images/logo.png")
    print("Logo created at docs/images/logo.png")

# 2. Fill empty box in asset_health_cv_workflow.png
def fix_asset_health_image():
    src_path = r"C:\Users\PHYSICS BOY\.gemini\antigravity-ide\brain\8d71ad2e-d145-4653-984f-d145408b0cfe\asset_health_cv_workflow_1784809240525.png"
    if not os.path.exists(src_path):
        print("Source image not found")
        return

    img = Image.open(src_path).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # The empty box is located roughly at bounding box [40, 715, 450, 935] on a ~1000x1000 image
    w, h = img.size
    print(f"Image dimensions: {w}x{h}")

    # Relative coordinates for bottom left box
    box_x1, box_y1 = int(w * 0.05), int(h * 0.72)
    box_x2, box_y2 = int(w * 0.45), int(h * 0.94)

    # Fill background of box with light purple pastel to match
    draw.rounded_rectangle([box_x1, box_y1, box_x2, box_y2], radius=25, fill=(235, 215, 255, 255), outline=(20, 20, 20), width=4)
    draw.rounded_rectangle([box_x1+3, box_y1+3, box_x2-3, box_y2-3], radius=23, outline=(20, 20, 20), width=2)

    try:
        font = ImageFont.truetype("comic.ttf", int(h * 0.038))
    except:
        try:
            font = ImageFont.truetype("arial.ttf", int(h * 0.038))
        except:
            font = ImageFont.load_default()

    text_line1 = "Asset Health"
    text_line2 = "Analyzer"

    # Calculate text placement
    cx = (box_x1 + box_x2) // 2
    cy = (box_y1 + box_y2) // 2

    draw.text((cx - int(w * 0.12), cy - int(h * 0.05)), text_line1, fill=(20, 20, 20), font=font)
    draw.text((cx - int(w * 0.09), cy + int(h * 0.01)), text_line2, fill=(20, 20, 20), font=font)

    img.save("docs/images/asset_health_cv_workflow.png")
    print("Fixed asset_health_cv_workflow.png saved to docs/images/asset_health_cv_workflow.png")

if __name__ == "__main__":
    create_doodle_logo()
    fix_asset_health_image()
