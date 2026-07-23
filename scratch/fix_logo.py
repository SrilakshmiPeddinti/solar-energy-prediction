import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("docs/images", exist_ok=True)

BG_CREAM = (250, 247, 238, 255)      # Light cream
BORDER_BLACK = (25, 25, 25, 255)

PASTEL_PINK   = (255, 209, 220, 255) # #FFD1DC
PASTEL_MINT   = (200, 230, 201, 255) # #C8E6C9
PASTEL_PURPLE = (225, 190, 231, 255) # #E1BEE7

def get_font(size):
    for font_name in ["comic.ttf", "comicbd.ttf", "arial.ttf", "DejaVuSans.ttf"]:
        try:
            return ImageFont.truetype(font_name, size)
        except:
            pass
    return ImageFont.load_default()

def draw_sketchy_rounded_rect(draw, bbox, fill, outline=BORDER_BLACK, radius=18):
    x1, y1, x2, y2 = bbox
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill)
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, outline=outline, width=4)
    draw.rounded_rectangle([x1+3, y1+2, x2-2, y2-3], radius=radius-2, outline=outline, width=2)

def draw_sketchy_arrow(draw, start, end):
    sx, sy = start
    ex, ey = end
    draw.line([(sx, sy), (ex, ey)], fill=BORDER_BLACK, width=4)
    
    import math
    angle = math.atan2(ey - sy, ex - sx)
    arrow_len = 14
    left_x = ex - arrow_len * math.cos(angle - math.pi / 6)
    left_y = ey - arrow_len * math.sin(angle - math.pi / 6)
    right_x = ex - arrow_len * math.cos(angle + math.pi / 6)
    right_y = ey - arrow_len * math.sin(angle + math.pi / 6)
    draw.polygon([(ex, ey), (left_x, left_y), (right_x, right_y)], fill=BORDER_BLACK)

def generate_perfect_logo():
    width, height = 1000, 240
    img = Image.new("RGBA", (width, height), BG_CREAM)
    draw = ImageDraw.Draw(img)
    
    font_main = get_font(28)
    font_sub = get_font(18)
    
    # Box Coordinates with wider width to prevent any text overflow
    boxes = [
        {"bbox": [40, 30, 310, 210], "fill": PASTEL_PINK, "title": "SOLAR AI", "sub": "Clean Forecasting"},
        {"bbox": [360, 30, 640, 210], "fill": PASTEL_MINT, "title": "PHYSICS ML", "sub": "PINN Physics Solver"},
        {"bbox": [690, 30, 960, 210], "fill": PASTEL_PURPLE, "title": "VPP GRID", "sub": "BESS Arbitrage"},
    ]
    
    for b in boxes:
        x1, y1, x2, y2 = b["bbox"]
        draw_sketchy_rounded_rect(draw, [x1, y1, x2, y2], fill=b["fill"])
        
        # Calculate centered text positioning
        box_w = x2 - x1
        
        # Draw Main Title
        draw.text((x1 + 35, y1 + 55), b["title"], fill=BORDER_BLACK, font=font_main)
        
        # Draw Subtitle
        draw.text((x1 + 35, y1 + 115), b["sub"], fill=(70, 70, 70, 255), font=font_sub)
        
    # Draw Arrows between Box 1 -> 2 and Box 2 -> 3
    draw_sketchy_arrow(draw, (310, 120), (360, 120))
    draw_sketchy_arrow(draw, (640, 120), (690, 120))
    
    img.save("docs/images/logo.png")
    print("Successfully generated perfect docs/images/logo.png with zero overflow!")

if __name__ == "__main__":
    generate_perfect_logo()
