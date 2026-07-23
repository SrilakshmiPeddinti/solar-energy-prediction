import os
import math
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
    x1, y1, x2, y2 = bbox
    # Fill
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill)
    # Outer primary sketchy border
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, outline=outline, width=4)
    # Inner offset sketchy border for whiteboard doodle look
    draw.rounded_rectangle([x1+3, y1+2, x2-2, y2-3], radius=radius-2, outline=outline, width=2)

def draw_sketchy_arrow(draw, start, end):
    sx, sy = start
    ex, ey = end
    draw.line([(sx, sy), (ex, ey)], fill=ARROW_BLACK, width=4)
    
    angle = math.atan2(ey - sy, ex - sx)
    arrow_len = 15
    left_x = ex - arrow_len * math.cos(angle - math.pi / 6)
    left_y = ey - arrow_len * math.sin(angle - math.pi / 6)
    right_x = ex - arrow_len * math.cos(angle + math.pi / 6)
    right_y = ey - arrow_len * math.sin(angle + math.pi / 6)
    draw.polygon([(ex, ey), (left_x, left_y), (right_x, right_y)], fill=ARROW_BLACK)

def create_padded_doodle_diagram(filename, title_text, blocks_data):
    """
    Creates a 1250x780 high-res hand-drawn whiteboard doodle diagram with wide outer margins
    so nothing ever gets cut off on the sides.
    """
    width, height = 1250, 780
    img = Image.new("RGBA", (width, height), BG_CREAM)
    draw = ImageDraw.Draw(img)
    
    font_title = get_font(30)
    font_box_title = get_font(20)
    font_box_sub = get_font(15)
    
    # Title Banner with generous margin
    draw_sketchy_rounded_rect(draw, [150, 25, 1100, 85], fill=PASTEL_YELLOW, radius=12)
    draw.text((180, 42), title_text, fill=BORDER_BLACK, font=font_title)
    
    # Coordinates with generous 70px side padding and clear box gaps
    # Row 1 (y: 140 -> 350)
    # Row 2 (y: 460 -> 670)
    coords = [
        (70, 140, 390, 350),    # Block 1
        (460, 140, 780, 350),   # Block 2
        (850, 140, 1170, 350),  # Block 3
        (260, 470, 580, 680),   # Block 4
        (670, 470, 990, 680),   # Block 5
    ]
    
    for i, data in enumerate(blocks_data):
        x1, y1, x2, y2 = coords[i]
        draw_sketchy_rounded_rect(draw, [x1, y1, x2, y2], fill=data["color"], radius=20)
        
        # Draw Box Title (split lines)
        title_lines = data["title"].split("\n")
        ty = y1 + 30
        for line in title_lines:
            draw.text((x1 + 20, ty), line, fill=BORDER_BLACK, font=font_box_title)
            ty += 26
            
        # Draw Subtitle
        draw.text((x1 + 20, y2 - 40), data["sub"], fill=(70, 70, 70, 255), font=font_box_sub)
        
    # Arrows
    draw_sketchy_arrow(draw, (390, 245), (460, 245))
    draw_sketchy_arrow(draw, (780, 245), (850, 245))
    draw_sketchy_arrow(draw, (1010, 350), (890, 470))
    draw_sketchy_arrow(draw, (670, 575), (580, 575))
    draw_sketchy_arrow(draw, (380, 470), (230, 350))
    
    img.save(f"docs/images/{filename}")
    print(f"Successfully generated padded diagram docs/images/{filename}")

if __name__ == "__main__":
    # 1. Asset Health CV Workflow (Fixed for user)
    create_padded_doodle_diagram(
        "asset_health_cv_workflow.png",
        "🚁 Computer Vision Drone IR & Predictive Asset Maintenance",
        [
            {"title": "Autonomous Drone\nRadiometric IR", "sub": "Aerial Thermal Scans", "color": PASTEL_PINK},
            {"title": "YOLOv8 Thermal\nHotspot AI", "sub": "Panel Anomaly Vision", "color": PASTEL_MINT},
            {"title": "EL Scan Microcrack\nClassifier", "sub": "Silicon Crack AI", "color": PASTEL_PURPLE},
            {"title": "Inverter RUL\nPrognostics", "sub": "Capacitor & IGBT Wear", "color": PASTEL_YELLOW},
            {"title": "Dynamic Panel\nWashing Scheduler", "sub": "Cleaning Optimization", "color": PASTEL_CYAN},
        ]
    )
    
    # 2. System Architecture
    create_padded_doodle_diagram(
        "system_architecture_diagram.png",
        "☀️ Enterprise Solar Platform - End-to-End Architecture",
        [
            {"title": "1. Edge Telemetry\nCollector", "sub": "Modbus / OPC-UA / MQTT", "color": PASTEL_MINT},
            {"title": "2. Satellite AI\nNowcasting", "sub": "GOES-16 & 3D LiDAR", "color": PASTEL_PINK},
            {"title": "3. Physics-Informed\nML Engine", "sub": "PyTorch PINN & TFT", "color": PASTEL_PURPLE},
            {"title": "4. BESS Storage\n& Arbitrage", "sub": "MILP & Market Bids", "color": PASTEL_YELLOW},
            {"title": "5. Zero-Trust\nSecurity & SCADA", "sub": "mTLS & Cloud Dashboard", "color": PASTEL_CYAN},
        ]
    )

    # 3. Edge SCADA Flow
    create_padded_doodle_diagram(
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

    # 4. Physics MLOps Pipeline
    create_padded_doodle_diagram(
        "physics_mlops_pipeline.png",
        "🧠 Physics-Informed AI & MLOps Governance Pipeline",
        [
            {"title": "Telemetry & GIS\nData Feeds", "sub": "Feast Feature Store", "color": PASTEL_MINT},
            {"title": "PINN Thermal\nBalance Loss", "sub": "PyTorch Physical Bounds", "color": PASTEL_PURPLE},
            {"title": "Quantile Loss\nP10/P50/P90", "sub": "Probabilistic Curves", "color": PASTEL_PINK},
            {"title": "TreeSHAP Model\nExplainability", "sub": "Feature Attribution", "color": PASTEL_YELLOW},
            {"title": "Shadow Deploy\n& A/B Testing", "sub": "Automated Validation", "color": PASTEL_CYAN},
        ]
    )

    # 5. VPP Financial Risk
    create_padded_doodle_diagram(
        "vpp_financial_risk_architecture.png",
        "💼 Virtual Power Plant & Monte Carlo Financial Risk",
        [
            {"title": "Virtual Power Plant\nAggregator", "sub": "C&I Solar Asset Pooling", "color": PASTEL_PINK},
            {"title": "50k Monte Carlo\nYield Risk", "sub": "Stochastic Revenue VaR", "color": PASTEL_MINT},
            {"title": "PPA Automated\nBilling Engine", "sub": "Monthly Energy Invoicing", "color": PASTEL_PURPLE},
            {"title": "OpEx vs CapEx\nROI Calculator", "sub": "NPV & Payback Engine", "color": PASTEL_YELLOW},
            {"title": "Weather Derivative\nHedge Insurance", "sub": "Shortfall Payout Claims", "color": PASTEL_CYAN},
        ]
    )
