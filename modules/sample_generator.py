"""
Sample Evidence Generator Module
Generates high-fidelity synthetic crime scene imagery, CCTV frames, and audio assets
for instant 1-click capstone demonstration and reliable fallback testing.
"""

import os
import io
import math
import struct
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2

def create_sample_crime_scene_image() -> Image.Image:
    """
    Synthesizes a realistic crime scene photograph featuring:
    - Pried entry door with tool marks
    - Shattered glass counter
    - Blood spatter transfer stain
    - Suspect silhouette with firearm
    - Forensic yellow evidence markers
    """
    width, height = 960, 640
    img = Image.new("RGB", (width, height), color=(18, 22, 30))
    draw = ImageDraw.Draw(img)
    
    # 1. Background Scene - Commercial Jewelry / Pawn Store at Night
    # Back wall & panels
    draw.rectangle([(0, 0), (width, 380)], fill=(28, 34, 46))
    # Wall baseboard
    draw.rectangle([(0, 375), (width, 395)], fill=(45, 52, 68))
    # Tile floor with perspective lines
    draw.rectangle([(0, 395), (width, height)], fill=(32, 38, 50))
    for x in range(-200, width + 400, 110):
        draw.line([(x, 395), (x + int((x - width/2) * 0.9), height)], fill=(22, 26, 36), width=2)
    for y in range(400, height, 45):
        draw.line([(0, y), (width, y)], fill=(22, 26, 36), width=2)
        
    # 2. Forced Entry Point - Pried Heavy Door & Frame (Left)
    # Door frame
    draw.rectangle([(40, 90), (220, 520)], fill=(40, 48, 62), outline=(80, 95, 120), width=3)
    draw.rectangle([(55, 105), (205, 505)], fill=(20, 26, 38), outline=(60, 75, 95), width=2)
    # Pried lock area with damage marks
    draw.rectangle([(195, 270), (225, 340)], fill=(90, 70, 40), outline=(230, 180, 50), width=2)
    draw.line([(190, 280), (225, 300)], fill=(255, 215, 0), width=3)
    draw.line([(195, 310), (228, 335)], fill=(200, 150, 30), width=2)
    # Forensic Evidence Marker #1 (Doorway)
    draw.polygon([(60, 510), (95, 510), (77, 475)], fill=(255, 215, 0), outline=(0, 0, 0))
    draw.text((72, 485), "1", fill=(0, 0, 0))
    
    # 3. Shattered Display Counter (Center Right)
    draw.rectangle([(460, 280), (880, 480)], fill=(40, 50, 68), outline=(100, 120, 150), width=2)
    # Broken glass cracks
    glass_center = (660, 360)
    for angle in [15, 45, 80, 120, 160, 210, 250, 290, 330]:
        rad = math.radians(angle)
        ex = int(glass_center[0] + 160 * math.cos(rad))
        ey = int(glass_center[1] + 90 * math.sin(rad))
        draw.line([glass_center, (ex, ey)], fill=(180, 220, 255), width=2)
        # Secondary branches
        bx = int(glass_center[0] + 80 * math.cos(rad) + 15 * math.sin(rad))
        by = int(glass_center[1] + 50 * math.sin(rad) + 15 * math.cos(rad))
        draw.line([(bx, by), (bx + 30, by + 20)], fill=(150, 200, 240), width=1)
    # Forensic Evidence Marker #2 (Display Case)
    draw.polygon([(480, 490), (515, 490), (497, 455)], fill=(255, 215, 0), outline=(0, 0, 0))
    draw.text((492, 465), "2", fill=(0, 0, 0))
    
    # 4. Blood Spatter Transfer & Impact Droplets (Floor Center-Left)
    blood_core = (340, 470)
    # Main puddle / smear
    draw.ellipse([(blood_core[0]-35, blood_core[1]-15), (blood_core[0]+45, blood_core[1]+20)], fill=(138, 7, 7))
    draw.ellipse([(blood_core[0]-15, blood_core[1]-25), (blood_core[0]+25, blood_core[1]+10)], fill=(160, 10, 10))
    # Satellite spatter droplets with trajectory tails
    droplets = [
        (310, 440, 6), (290, 430, 4), (275, 420, 3), (360, 445, 5),
        (380, 435, 4), (400, 425, 3), (330, 505, 5), (350, 515, 4)
    ]
    for dx, dy, r in droplets:
        draw.ellipse([(dx-r, dy-r), (dx+r, dy+r)], fill=(178, 14, 14))
        # Cast-off tail pointing away from center
        draw.line([(dx, dy), (dx + int((dx - blood_core[0])*0.2), dy + int((dy - blood_core[1])*0.2))], fill=(138, 7, 7), width=2)
    # Forensic Evidence Marker #3 (Blood Spatter)
    draw.polygon([(260, 490), (295, 490), (277, 455)], fill=(255, 215, 0), outline=(0, 0, 0))
    draw.text((272, 465), "3", fill=(0, 0, 0))
    
    # 5. Suspect Silhouette with Drawn Firearm (Right Center)
    # Head & Mask
    draw.ellipse([(680, 120), (740, 185)], fill=(20, 22, 28))
    # Hoodie outline
    draw.polygon([(650, 170), (770, 170), (790, 360), (630, 360)], fill=(25, 28, 35))
    # Arms and Hands holding handgun
    draw.line([(660, 200), (600, 250), (550, 250)], fill=(25, 28, 35), width=18)
    # Handgun silhouette
    draw.rectangle([(510, 235), (555, 252)], fill=(15, 15, 20)) # Barrel & slide
    draw.rectangle([(538, 250), (552, 285)], fill=(12, 12, 18)) # Grip
    # Forensic Evidence Marker #4 (Suspect Weapon Position)
    draw.polygon([(780, 370), (815, 370), (797, 335)], fill=(255, 215, 0), outline=(0, 0, 0))
    draw.text((792, 345), "4", fill=(0, 0, 0))
    
    # 6. CCTV Metadata Overlay (Top Left & Top Right)
    draw.rectangle([(15, 15), (420, 52)], fill=(0, 0, 0, 180), outline=(0, 229, 255), width=1)
    draw.text((25, 22), "CAM-02 ENTRANCE/SALES FLOOR [REC] 29.97 FPS", fill=(0, 229, 255))
    draw.text((25, 36), "TIMESTAMP: 2026-10-25 02:14:32.481 UTC", fill=(200, 225, 255))
    
    # Forensic Scale Ruler (Bottom Right)
    draw.rectangle([(width - 220, height - 35), (width - 20, height - 15)], fill=(240, 240, 240), outline=(0, 0, 0), width=1)
    for i in range(10):
        sx = width - 220 + i * 20
        fill_col = (0, 0, 0) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([(sx, height - 35), (sx + 20, height - 25)], fill=fill_col)
    draw.text((width - 205, height - 13), "FORENSIC 10CM SCALE", fill=(180, 200, 220))
    
    return img

def create_sample_audio_wav() -> bytes:
    """
    Generates a valid PCM 16-bit WAV file containing a simulated police radio / 911 dispatch
    beeping chime and background ambient noise so it plays seamlessly in st.audio().
    """
    sample_rate = 8000
    duration_sec = 4.0
    num_samples = int(sample_rate * duration_sec)
    
    # Synthesize two-tone dispatch alert (853 Hz & 960 Hz) followed by radio squelch
    raw_bytes = bytearray()
    for i in range(num_samples):
        t = float(i) / sample_rate
        if t < 0.6:
            # First alert beep 853 Hz
            sample = 0.4 * math.sin(2.0 * math.pi * 853.0 * t)
        elif 0.7 < t < 1.3:
            # Second alert beep 960 Hz
            sample = 0.4 * math.sin(2.0 * math.pi * 960.0 * (t - 0.7))
        elif 1.4 < t < duration_sec:
            # Simulated radio carrier hum + voice frequency harmonics
            hum = 0.15 * math.sin(2.0 * math.pi * 440.0 * t)
            modulation = 0.1 * math.sin(2.0 * math.pi * 220.0 * t) * math.cos(2.0 * math.pi * 3.0 * t)
            noise = 0.05 * (np.random.random() * 2.0 - 1.0)
            sample = hum + modulation + noise
        else:
            sample = 0.0
            
        sample_int = int(max(-32767, min(32767, sample * 32767)))
        raw_bytes.extend(struct.pack('<h', sample_int))
        
    # Build standard WAV RIFF header
    riff_header = bytearray()
    riff_header.extend(b'RIFF')
    total_data_len = len(raw_bytes)
    riff_header.extend(struct.pack('<I', total_data_len + 36))
    riff_header.extend(b'WAVE')
    riff_header.extend(b'fmt ')
    riff_header.extend(struct.pack('<I', 16)) # Subchunk1Size for PCM
    riff_header.extend(struct.pack('<H', 1))  # AudioFormat 1 = PCM
    riff_header.extend(struct.pack('<H', 1))  # NumChannels 1 = Mono
    riff_header.extend(struct.pack('<I', sample_rate))
    byte_rate = sample_rate * 1 * 2
    riff_header.extend(struct.pack('<I', byte_rate))
    riff_header.extend(struct.pack('<H', 2))  # BlockAlign
    riff_header.extend(struct.pack('<H', 16)) # BitsPerSample
    riff_header.extend(b'data')
    riff_header.extend(struct.pack('<I', total_data_len))
    
    return bytes(riff_header + raw_bytes)

def generate_sample_cctv_keyframes() -> list:
    """
    Generates a sequence of 6 progressive CCTV surveillance keyframes
    illustrating the suspect's chronological trajectory across 12 seconds:
    - Frame 01 (T=01s): Suspect approaches alleyway door
    - Frame 02 (T=03s): Forced pry attack on exterior lock
    - Frame 03 (T=06s): Interior breach, brandishing 9mm pistol
    - Frame 04 (T=08s): Shattering glass display counter
    - Frame 05 (T=10s): Grabbing electronics/valuables
    - Frame 06 (T=12s): Suspect flees to dark gray sedan in alleyway
    """
    keyframes = []
    actions = [
        {"time": "02:14:20", "sec": 1, "action": "Suspect approaches rear service entrance from blind alley.", "x": 120, "y": 240, "code": "PC 594"},
        {"time": "02:14:23", "sec": 3, "action": "Suspect applies heavy pry tool to door jamb; lock failure.", "x": 180, "y": 250, "code": "PC 459"},
        {"time": "02:14:26", "sec": 6, "action": "Suspect breaches threshold into retail showroom with firearm.", "x": 360, "y": 260, "code": "PC 245(a)(2)"},
        {"time": "02:14:28", "sec": 8, "action": "Impact weapon strikes central glass jewelry display.", "x": 520, "y": 270, "code": "PC 211"},
        {"time": "02:14:30", "sec": 10, "action": "Suspect seizes gold trays; secondary blood transfer noted.", "x": 640, "y": 275, "code": "PC 487"},
        {"time": "02:14:32", "sec": 12, "action": "Suspect sprints to waiting silver Honda sedan; rapid departure.", "x": 780, "y": 290, "code": "VC 2800.2"}
    ]
    
    for i, meta in enumerate(actions):
        w, h = 640, 360
        img = Image.new("RGB", (w, h), color=(14, 18, 26))
        draw = ImageDraw.Draw(img)
        
        # Room background
        draw.rectangle([(0, 0), (w, 220)], fill=(22, 28, 40))
        draw.rectangle([(0, 220), (w, h)], fill=(30, 36, 48))
        
        # Grid camera lines
        for gx in range(0, w, 80):
            draw.line([(gx, 0), (gx, h)], fill=(20, 26, 36), width=1)
            
        # Draw past trajectory path
        for p_idx in range(i):
            prev_p = actions[p_idx]
            next_p = actions[p_idx + 1]
            draw.line([(prev_p["x"], prev_p["y"]), (next_p["x"], next_p["y"])], fill=(0, 229, 255), width=2)
            draw.ellipse([(prev_p["x"]-4, prev_p["y"]-4), (prev_p["x"]+4, prev_p["y"]+4)], fill=(0, 229, 255))
            
        # Current suspect position with bounding box
        cx, cy = meta["x"], meta["y"]
        bbox = [(cx - 35, cy - 70), (cx + 35, cy + 60)]
        draw.rectangle(bbox, outline=(255, 23, 68), width=2)
        # Class tag
        draw.rectangle([(cx - 35, cy - 88), (cx + 50, cy - 70)], fill=(255, 23, 68))
        draw.text((cx - 32, cy - 86), f"SUSPECT-01", fill=(255, 255, 255))
        
        # Suspect figure
        draw.ellipse([(cx - 15, cy - 65), (cx + 15, cy - 35)], fill=(40, 45, 55))
        draw.rectangle([(cx - 20, cy - 35), (cx + 20, cy + 30)], fill=(30, 35, 45))
        draw.line([(cx - 10, cy + 30), (cx - 15, cy + 55)], fill=(20, 25, 35), width=6)
        draw.line([(cx + 10, cy + 30), (cx + 15, cy + 55)], fill=(20, 25, 35), width=6)
        
        # HUD overlays
        draw.rectangle([(10, 10), (320, 42)], fill=(0, 0, 0, 200))
        draw.text((15, 14), f"CAM-03 CORRIDOR | T={meta['sec']:02d}s | {meta['time']} UTC", fill=(0, 229, 255))
        draw.text((15, 28), f"PENAL CLASSIFICATION: {meta['code']}", fill=(255, 215, 0))
        
        keyframes.append({
            "frame_idx": i + 1,
            "timestamp": meta["time"],
            "second": meta["sec"],
            "image": img,
            "action": meta["action"],
            "penal_code": meta["code"],
            "coords": f"({cx}, {cy})"
        })
        
    return keyframes
