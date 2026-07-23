import os
import random
from PIL import Image, ImageDraw, ImageFont

os.makedirs("docs/images", exist_ok=True)

BG_CREAM = (250, 247, 238, 255)      # #FAF7EE light cream
BORDER_BLACK = (25, 25, 25, 255)    # Sketchy black border
ARROW_BLACK = (20, 20, 20, 255)

PASTEL_PINK   = (255, 209, 220, 255) # #FFD1DC
PASTEL_MINT   = (200, 230, 201, 255) # #C8E6C9
PASTEL_PURPLE = (225, 190, 231, 255) # #E1BEE7
PASTEL_YELLOW = (255, 249, 196, 255) # #FFF9C4
PASTEL_CYAN   = (178, 235, 242, 255) # #B2EBF2

def get_font(size):
    for font_name in ["comic.ttf", "comicbd.ttf", "arial.ttf", "DejaVuSans.ttf"]:
        try:
            return ImageFont.truetype(font_name, size)
        except:
            pass
    return ImageFont.load_default()

def draw_sketchy_rounded_rect(draw, bbox, fill, outline=BORDER_BLACK, radius=18):
    """Draws a pastel filled rectangle with hand-drawn sketchy double borders."""
    x1, y1, x2, y2 = bbox
    # Fill
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill)
    
    # Outer primary sketchy border
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, outline=outline, width=3)
    
    # Inner offset sketchy border to simulate hand-drawn whiteboard doodle
    draw.rounded_rectangle([x1+3, y1+2, x2-2, y2-3], radius=radius-2, outline=outline, width=2)

def draw_sketchy_arrow(draw, start, end):
    """Draws a sketchy hand-drawn arrow connecting blocks."""
    sx, sy = start
    ex, ey = end
    
    # Line
    draw.line([(sx, sy), (ex, ey)], fill=ARROW_BLACK, width=4)
    
    # Arrow head logic
    import math
    angle = math.atan2(ey - sy, ex - sx)
    arrow_len = 16
    
    left_x = ex - arrow_len * math.cos(angle - math.pi / 6)
    left_y = ey - arrow_len * math.sin(angle - math.pi / 6)
    right_x = ex - arrow_len * math.cos(angle + math.pi / 6)
    right_y = ey - arrow_len * math.sin(angle + math.pi / 6)
    
    draw.polygon([(ex, ey), (left_x, left_y), (right_x, right_y)], fill=ARROW_BLACK)

def create_doodle_diagram(filename, title_text, blocks_data):
    """
    Creates a 1200x750 high-res hand-drawn whiteboard doodle diagram.
    blocks_data: list of 5 dicts: {"title": str, "sub": str, "color": tuple}
    """
    width, height = 1200, 750
    img = Image.new("RGBA", (width, height), BG_CREAM)
    draw = ImageDraw.Draw(img)
    
    font_title = get_font(32)
    font_box_title = get_font(22)
    font_box_sub = get_font(16)
    
    # Header Title Banner
    draw_sketchy_rounded_rect(draw, [200, 25, 1000, 85], fill=PASTEL_YELLOW, radius=12)
    draw.text((230, 40), title_text, fill=BORDER_BLACK, font=font_title)
    
    # Positions for 5 blocks (Top row 3 blocks, Bottom row 2 blocks)
    # Row 1 (y: 140 -> 340)
    # Row 2 (y: 450 -> 650)
    coords = [
        (60, 150, 380, 350),    # Block 1
        (460, 150, 780, 350),   # Block 2
        (840, 150, 1160, 350),  # Block 3
        (260, 480, 580, 680),   # Block 4
        (660, 480, 980, 680),   # Block 5
    ]
    
    # Draw blocks
    for i, data in enumerate(blocks_data):
        x1, y1, x2, y2 = coords[i]
        draw_sketchy_rounded_rect(draw, [x1, y1, x2, y2], fill=data["color"], radius=20)
        
        # Draw Box Title
        title_lines = data["title"].split("\n")
        ty = y1 + 35
        for line in title_lines:
            draw.text((x1 + 25, ty), line, fill=BORDER_BLACK, font=font_box_title)
            ty += 28
            
        # Draw Box Subtitle
        draw.text((x1 + 25, y2 - 45), data["sub"], fill=(70, 70, 70, 255), font=font_box_sub)
        
    # Draw Sketchy Arrow Connections
    # Block 1 -> Block 2
    draw_sketchy_arrow(draw, (380, 250), (460, 250))
    # Block 2 -> Block 3
    draw_sketchy_arrow(draw, (780, 250), (840, 250))
    # Block 3 -> Block 5 (Diagonal down)
    draw_sketchy_arrow(draw, (980, 350), (880, 480))
    # Block 5 -> Block 4 (Left)
    draw_sketchy_arrow(draw, (660, 580), (580, 580))
    # Block 4 -> Block 1 (Diagonal up)
    draw_sketchy_arrow(draw, (380, 480), (240, 350))
    
    img.save(f"docs/images/{filename}")
    print(f"Successfully generated docs/images/{filename}")

# Generate Logo
def generate_logo():
    width, height = 900, 220
    img = Image.new("RGBA", (width, height), BG_CREAM)
    draw = ImageDraw.Draw(img)
    
    font_main = get_font(36)
    font_sub = get_font(20)
    
    # 3 Pastel Header Cards
    draw_sketchy_rounded_rect(draw, [40, 35, 280, 185], fill=PASTEL_PINK)
    draw_sketchy_rounded_rect(draw, [320, 35, 580, 185], fill=PASTEL_MINT)
    draw_sketchy_rounded_rect(draw, [620, 35, 860, 185], fill=PASTEL_PURPLE)
    
    draw.text((70, 70), "☀️ SOLAR AI", fill=BORDER_BLACK, font=font_main)
    draw.text((75, 125), "Clean Forecast", fill=(60, 60, 60), font=font_sub)
    
    draw.text((345, 70), "🧠 PHYSICS ML", fill=BORDER_BLACK, font=font_main)
    draw.text((360, 125), "PINN Thermodynamics", fill=(60, 60, 60), font=font_sub)
    
    draw.text((650, 70), "⚡ VPP GRID", fill=BORDER_BLACK, font=font_main)
    draw.text((660, 125), "BESS Arbitrage", fill=(60, 60, 60), font=font_sub)
    
    # Arrows
    draw_sketchy_arrow(draw, (280, 110), (320, 110))
    draw_sketchy_arrow(draw, (580, 110), (620, 110))
    
    img.save("docs/images/logo.png")
    print("Successfully generated docs/images/logo.png")

if __name__ == "__main__":
    generate_logo()
    
    # 1. System Architecture
    create_doodle_diagram(
        "system_architecture_diagram.png",
        "☀️ Enterprise Solar Platform - End-to-End System Architecture",
        [
            {"title": "1. Edge Telemetry\nCollector", "sub": "Modbus / OPC-UA / MQTT", "color": PASTEL_MINT},
            {"title": "2. Satellite AI\nNowcasting", "sub": "GOES-16 & 3D LiDAR", "color": PASTEL_PINK},
            {"title": "3. Physics-Informed\nML Engine", "sub": "PyTorch PINN & TFT", "color": PASTEL_PURPLE},
            {"title": "4. BESS Storage\n& Arbitrage", "sub": "MILP & Market Bids", "color": PASTEL_YELLOW},
            {"title": "5. Zero-Trust Security\n& SCADA", "sub": "mTLS & Cloud Dashboard", "color": PASTEL_CYAN},
        ]
    )
    
    # 2. Edge SCADA Flow
    create_doodle_diagram(
        "edge_scada_bess_flow.png",
        "⚡ Sub-Second Telemetry & SCADA Closed-Loop Control",
        [
            {"title": "Edge Inverter\nSensors", "sub": "Modbus RTU / TCP", "color": PASTEL_PINK},
            {"title": "Apache Kafka\nStream Pipeline", "sub": "Sub-Second Ingestion", "color": PASTEL_MINT},
            {"title": "Kalman Filter\nDrift Detection", "sub": "Sensor Self-Calibration", "color": PASTEL_PURPLE},
            {"title": "SCADA / DERMS\nControl Loop", "sub": "IEC 61850 Curtailment", "color": PASTEL_YELLOW},
            {"title": "BESS Market\nArbitrage", "sub": "Day-Ahead Spot Bids", "color": PASTEL_CYAN},
        ]
    )
    
    # 3. Physics MLOps Pipeline
    create_doodle_diagram(
        "physics_mlops_pipeline.png",
        "🧠 Physics-Informed AI & MLOps Governance Pipeline",
        [
            {"title": "Telemetry & GIS\nData Feeds", "sub": "Feast Feature Store", "color": PASTEL_MINT},
            {"title": "PINN Thermal\nBalance Loss", "sub": "PyTorch Physical Bounds", "color": PASTEL_PURPLE},
            {"title": "Quantile Loss\nP10/P50/P90", "sub": "Probabilistic Curves", "color": PASTEL_PINK},
            {"title": "TreeSHAP Model\nExplainability", "sub": "Feature Attribution", "color": PASTEL_YELLOW},
            {"title": "Champion-Challenger\nShadow Deploy", "sub": "Automated A/B Testing", "color": PASTEL_CYAN},
        ]
    )
    
    # 4. Asset Health CV Workflow
    create_doodle_diagram(
        "asset_health_cv_workflow.png",
        "🚁 Computer Vision Drone IR & Predictive Asset Health",
        [
            {"title": "Autonomous Drone\nRadiometric IR", "sub": "Aerial Thermal Scans", "color": PASTEL_PINK},
            {"title": "YOLOv8 Thermal\nHotspot AI", "sub": "Panel Anomaly Vision", "color": PASTEL_MINT},
            {"title": "Electroluminescence\nEL Microcrack AI", "sub": "Silicon Crack Classifier", "color": PASTEL_PURPLE},
            {"title": "Inverter RUL\nPrognostics", "sub": "Capacitor & IGBT Wear", "color": PASTEL_YELLOW},
            {"title": "Dynamic Washing\nScheduler", "sub": "Cleaning Cost Optimizer", "color": PASTEL_CYAN},
        ]
    )
    
    # 5. VPP Financial Risk
    create_doodle_diagram(
        "vpp_financial_risk_architecture.png",
        "💼 Virtual Power Plant & Monte Carlo Financial Risk Engine",
        [
            {"title": "Virtual Power Plant\nAggregator", "sub": "C&I Solar Asset Pooling", "color": PASTEL_PINK},
            {"title": "50k Monte Carlo\nYield Risk", "sub": "Stochastic Revenue VaR", "color": PASTEL_MINT},
            {"title": "PPA Automated\nContract Settlement", "sub": "Monthly Energy Billing", "color": PASTEL_PURPLE},
            {"title": "OpEx vs CapEx\nROI Calculator", "sub": "NPV & Payback Engine", "color": PASTEL_YELLOW},
            {"title": "Weather Derivative\nHedge Insurance", "sub": "Shortfall Payout Claims", "color": PASTEL_CYAN},
        ]
    )
