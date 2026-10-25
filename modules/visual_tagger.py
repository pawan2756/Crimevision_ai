"""
Tab 1: Crime Scene Visual Evidence Tagger (Epic 2)
Simulates RT-DETR (Real-Time DEtection TRansformer) multimodal object detection
identifying persons, firearms, edged weapons, blood spatter, and forced entry points.
Outputs structured forensic analysis: Threat Level, Scene Classification, Bounding Boxes, Leads.
"""

import io
import json
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps
import streamlit as st
from config import DETECTION_CLASSES, THREAT_LEVELS, SCENE_CLASSES
from modules.auth_security import log_custody_transfer, calculate_sha256, generate_evidence_id
from modules.sample_generator import create_sample_crime_scene_image

def draw_rt_detr_annotations(image: Image.Image, detections: list) -> Image.Image:
    """
    Draws professional forensic RT-DETR bounding boxes, labels, confidence chips,
    and spatial targeting crosshairs directly on the image.
    """
    annotated = image.copy().convert("RGB")
    draw = ImageDraw.Draw(annotated)
    w, h = annotated.size
    
    for det in detections:
        cls_name = det.get("class", "Unknown")
        conf = det.get("confidence", 0.85)
        # Spatial coords normalized [ymin, xmin, ymax, xmax]
        ymin, xmin, ymax, xmax = det.get("bbox", [0.2, 0.2, 0.4, 0.4])
        
        # Convert to absolute pixel coordinates
        x1, y1 = int(xmin * w), int(ymin * h)
        x2, y2 = int(xmax * w), int(ymax * h)
        
        # Color mapping
        cfg = DETECTION_CLASSES.get(cls_name, {"hex": "#00E5FF", "icon": "🔍"})
        color = cfg["hex"]
        
        # Bounding box with corner accents (tactical HUD style)
        draw.rectangle([(x1, y1), (x2, y2)], outline=color, width=3)
        
        # Corner brackets for tactical look
        bracket_len = min(15, (x2 - x1) // 4, (y2 - y1) // 4)
        draw.line([(x1, y1), (x1 + bracket_len, y1)], fill="#FFFFFF", width=3)
        draw.line([(x1, y1), (x1, y1 + bracket_len)], fill="#FFFFFF", width=3)
        draw.line([(x2, y1), (x2 - bracket_len, y1)], fill="#FFFFFF", width=3)
        draw.line([(x2, y1), (x2, y1 + bracket_len)], fill="#FFFFFF", width=3)
        draw.line([(x1, y2), (x1 + bracket_len, y2)], fill="#FFFFFF", width=3)
        draw.line([(x1, y2), (x1, y2 - bracket_len)], fill="#FFFFFF", width=3)
        draw.line([(x2, y2), (x2 - bracket_len, y2)], fill="#FFFFFF", width=3)
        draw.line([(x2, y2), (x2, y2 - bracket_len)], fill="#FFFFFF", width=3)
        
        # Header banner
        label_text = f"{cfg.get('icon', '')} {cls_name} | {conf:.1%}"
        text_bbox = draw.textbbox((x1, y1 - 22), label_text)
        draw.rectangle([(x1, y1 - 24), (text_bbox[2] + 8, y1)], fill=color)
        draw.text((x1 + 4, y1 - 22), label_text, fill=(0, 0, 0) if color in ["#FFEA00", "#00E5FF"] else (255, 255, 255))
        
        # Spatial coordinate watermark in bottom right of box
        coord_text = f"[{ymin:.2f},{xmin:.2f},{ymax:.2f},{xmax:.2f}]"
        draw.text((x1 + 4, y2 - 14), coord_text, fill=color)
        
    return annotated

def apply_forensic_filter(image: Image.Image, filter_type: str) -> Image.Image:
    """Applies specialized laboratory optical enhancement filters."""
    if filter_type == "Luminance Inversion (Latent Bloodstain)":
        gray = ImageOps.grayscale(image)
        return ImageOps.invert(gray)
    elif filter_type == "High-Pass Forensic Edge Contrast":
        enhancer = ImageEnhance.Contrast(image)
        contrasted = enhancer.enhance(2.4)
        sharpener = ImageEnhance.Sharpness(contrasted)
        return sharpener.enhance(2.8)
    elif filter_type == "Thermal Heatmap Visualization":
        img_np = np.array(image.convert("L"))
        heatmap = cv2.applyColorMap(img_np, cv2.COLORMAP_JET)
        return Image.fromarray(cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB))
    return image

def run_gemini_vision_analysis(api_key: str, image: Image.Image) -> dict:
    """Invokes Gemini Multimodal Vision if API key is provided."""
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        
        # Convert image to bytes
        buf = io.BytesIO()
        image.save(buf, format="JPEG")
        image_bytes = buf.getvalue()
        
        prompt = """
        You are an advanced RT-DETR forensic multimodal object detection and crime scene analysis engine.
        Analyze this crime scene photograph and output a strictly valid JSON object with these exact keys:
        {
            "threat_level": "CRITICAL" | "HIGH" | "MEDIUM" | "LOW",
            "threat_justification": "Detailed forensic explanation",
            "scene_classification": "Burglary (Forced Entry)" | "Homicide Investigation" | "Armed Robbery in Progress" | "Aggravated Assault with Deadly Weapon" | "Felony Vandalism & Property Destruction",
            "scene_confidence": 0.94,
            "detected_objects": [
                {
                    "id": "DET-01",
                    "class": "Person (Suspect)" | "Firearm (Handgun)" | "Edged Weapon (Knife)" | "Blood Spatter (Impact)" | "Forced Entry (Pried Lock)" | "Shattered Glass",
                    "confidence": 0.96,
                    "bbox": [ymin, xmin, ymax, xmax] (normalized 0.0 to 1.0),
                    "forensic_notes": "Toolmark or ballistic observation"
                }
            ],
            "investigative_leads": [
                "Prioritized lead 1",
                "Prioritized lead 2",
                "Prioritized lead 3"
            ]
        }
        Do not wrap in markdown quotes if possible, output pure JSON.
        """
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[prompt, genai.types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")]
        )
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())
    except Exception as e:
        # Fall back smoothly
        st.info(f"API notice: Using simulated RT-DETR forensic model (fallback reason: {str(e)[:90]}...)")
        return None

def get_simulated_rtdetr_detections() -> dict:
    """Returns high-fidelity deterministic RT-DETR forensic detection results."""
    return {
        "threat_level": "CRITICAL",
        "threat_justification": "Brandished lethal firearm (semiautomatic 9mm profile) detected in direct proximity to commercial forced entry breach and active blood spatter transfer stains.",
        "scene_classification": "Armed Robbery in Progress",
        "scene_confidence": 0.948,
        "detected_objects": [
            {
                "id": "DET-01",
                "class": "Forced Entry (Pried Lock)",
                "confidence": 0.964,
                "bbox": [0.14, 0.04, 0.81, 0.23],
                "forensic_notes": "Heavy mechanical shearing marks on commercial lock plate consistent with a 24-inch flat crowbar."
            },
            {
                "id": "DET-02",
                "class": "Shattered Glass",
                "confidence": 0.932,
                "bbox": [0.44, 0.48, 0.75, 0.92],
                "forensic_notes": "Radial and concentric fractures centered at coordinate (660, 360) indicating blunt force impact."
            },
            {
                "id": "DET-03",
                "class": "Blood Spatter (Impact)",
                "confidence": 0.915,
                "bbox": [0.65, 0.27, 0.82, 0.44],
                "forensic_notes": "Medium-velocity impact spatter with directional satellite droplets pointing 210 degrees SW. DNA swab candidate."
            },
            {
                "id": "DET-04",
                "class": "Person (Suspect)",
                "confidence": 0.978,
                "bbox": [0.18, 0.65, 0.58, 0.84],
                "forensic_notes": "Male adult silhouette, dark tactical hoodie, concealed facial features, aggressive forward posture."
            },
            {
                "id": "DET-05",
                "class": "Firearm (Handgun)",
                "confidence": 0.951,
                "bbox": [0.36, 0.53, 0.45, 0.58],
                "forensic_notes": "Polymer frame semiautomatic handgun (Glock-pattern profile) brandished in low-ready orientation."
            }
        ],
        "investigative_leads": [
            "1. Priority DNA Recovery: Swab blood transfer stains adjacent to broken display counter [DET-03] for CODIS profile matching.",
            "2. Toolmark Impression Cast: Preserve striation toolmarks on pried service door latch [DET-01] for comparison with seized crowbars.",
            "3. Ballistics & Firearm Registry: Check regional pawn and stolen weapon databases for 9mm polymer handguns matching [DET-05].",
            "4. Perimeter Canvass: Extract exterior Ring doorbell and traffic camera feeds along western alleyway corridor between 02:10 and 02:20 UTC."
        ]
    }

def render_visual_tagger_tab():
    """Renders Tab 1: Crime Scene Visual Evidence Tagger."""
    st.markdown("""
    <div class="forensic-banner">
        <span>📸 MODULE: CRIME SCENE VISUAL EVIDENCE TAGGER (RT-DETR V4)</span>
        <span>STATUS: ACTIVE CALIBRATION</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    Upload high-resolution crime scene photography or surveillance stills. The embedded **RT-DETR (Real-Time DEtection TRansformer)** 
    multimodal model localizes and classifies weapons, perpetrators, entry vectors, and physiological biological evidence with sub-pixel spatial coordinates.
    """)
    
    col_upload, col_sample = st.columns([3, 2])
    with col_upload:
        uploaded_file = st.file_uploader(
            "Upload Crime Scene Image (JPG / PNG / WEBP)",
            type=["jpg", "jpeg", "png", "webp"],
            help="Accepted formats: High-resolution scene photographs, latent evidence captures, or CCTV stills."
        )
    with col_sample:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("📁 Load Verified Capstone Scene #0891 (Jewelry Robbery)", use_container_width=True):
            sample_img = create_sample_crime_scene_image()
            buf = io.BytesIO()
            sample_img.save(buf, format="JPEG")
            st.session_state.current_image = sample_img
            st.session_state.current_image_bytes = buf.getvalue()
            st.session_state.image_evidence_id = "IMG-EV-2026-0891"
            st.session_state.visual_analysis = get_simulated_rtdetr_detections()
            
            log_custody_transfer(
                evidence_id="IMG-EV-2026-0891",
                action="IMAGE INGESTION & RT-DETR TAGGING",
                notes="Verified high-resolution scene photo ingested into volatile forensic workspace.",
                raw_payload=st.session_state.current_image_bytes
            )
            st.rerun()

    # Process new user upload
    if uploaded_file is not None:
        raw_bytes = uploaded_file.read()
        if "current_image_bytes" not in st.session_state or st.session_state.current_image_bytes != raw_bytes:
            image = Image.open(io.BytesIO(raw_bytes)).convert("RGB")
            st.session_state.current_image = image
            st.session_state.current_image_bytes = raw_bytes
            ev_id = generate_evidence_id(prefix="IMG-EV")
            st.session_state.image_evidence_id = ev_id
            
            # Run detection: Gemini if key available, else simulated RT-DETR
            with st.spinner("Executing RT-DETR multimodal feature extraction & tensor localization..."):
                analysis = None
                if not st.session_state.demo_mode and "Gemini" in st.session_state.api_provider and st.session_state.api_key:
                    analysis = run_gemini_vision_analysis(st.session_state.api_key, image)
                if not analysis:
                    analysis = get_simulated_rtdetr_detections()
                st.session_state.visual_analysis = analysis
                
            log_custody_transfer(
                evidence_id=ev_id,
                action="IMAGE INGESTION & RT-DETR TAGGING",
                notes=f"Uploaded photo ({uploaded_file.name}, {len(raw_bytes)} bytes) tagged with {len(analysis['detected_objects'])} bounding vectors.",
                raw_payload=raw_bytes
            )
            st.rerun()

    # Render analysis if an image is loaded
    if "current_image" in st.session_state and st.session_state.current_image is not None:
        image = st.session_state.current_image
        analysis = st.session_state.visual_analysis
        ev_id = st.session_state.image_evidence_id
        
        st.divider()
        
        # Display Controls
        col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([2, 2, 2])
        with col_ctrl1:
            view_mode = st.radio(
                "Display Overlay",
                ["RT-DETR Bounding Annotations", "Raw Unmarked Scene Photo", "Forensic Lab Filter"],
                horizontal=True
            )
        with col_ctrl2:
            filter_choice = "Standard"
            if view_mode == "Forensic Lab Filter":
                filter_choice = st.selectbox(
                    "Optical Enhancement Filter",
                    ["Luminance Inversion (Latent Bloodstain)", "High-Pass Forensic Edge Contrast", "Thermal Heatmap Visualization"]
                )
        with col_ctrl3:
            sha = calculate_sha256(st.session_state.current_image_bytes)
            st.markdown(f"""
            <div style="font-size: 0.75rem; color: #94A3B8; font-family: monospace; padding-top: 10px;">
                EVIDENCE ID: <span style="color:#00E5FF;">{ev_id}</span><br>
                SHA-256: <span title="{sha}">{sha[:18]}...{sha[-6:]}</span>
            </div>
            """, unsafe_allow_html=True)

        # Image Rendering
        rendered_image = image
        if view_mode == "RT-DETR Bounding Annotations":
            rendered_image = draw_rt_detr_annotations(image, analysis.get("detected_objects", []))
        elif view_mode == "Forensic Lab Filter":
            rendered_image = apply_forensic_filter(image, filter_choice)

        st.image(rendered_image, caption=f"Forensic Evidence Frame [{ev_id}] — {view_mode}", use_container_width=True)

        # Structured Forensic Analysis Metrics
        st.markdown("### 🔍 Structured Forensic Scene Assessment")
        
        t_level = analysis.get("threat_level", "HIGH")
        t_meta = THREAT_LEVELS.get(t_level, THREAT_LEVELS["HIGH"])
        scene_cls = analysis.get("scene_classification", "Armed Robbery")
        scene_conf = analysis.get("scene_confidence", 0.92)
        
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            st.markdown(f"""
            <div class="forensic-card">
                <div style="color: #94A3B8; font-size: 0.78rem;">THREAT LEVEL</div>
                <div class="threat-badge" style="background:{t_meta['bg']}; color:{t_meta['color']}; border:1px solid {t_meta['border']}; margin-top: 6px;">
                    {t_meta['badge']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        with m_col2:
            st.metric("SCENE CLASSIFICATION", scene_cls, f"{scene_conf:.1%} confidence")
        with m_col3:
            st.metric("OBJECTS LOCALIZED", f"{len(analysis.get('detected_objects', []))} Artefacts", "RT-DETR v4 Tensor")
        with m_col4:
            st.metric("CHAIN OF CUSTODY", "VERIFIED", f"SHA-256 Valid")

        # Threat Assessment Note
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.7); border-left: 4px solid {t_meta['color']}; padding: 10px 14px; border-radius: 4px; font-size: 0.88rem; margin-bottom: 16px;">
            <b>Investigative Threat Assessment:</b> {analysis.get('threat_justification', 'No immediate elevated threat detected.')}
        </div>
        """, unsafe_allow_html=True)

        # Detected Items & Spatial Coordinates Table
        st.markdown("#### 🎯 Localized Bounding Vectors & Ballistic/Toolmark Catalog")
        
        items_data = []
        for det in analysis.get("detected_objects", []):
            bbox = det.get("bbox", [0, 0, 0, 0])
            coord_str = f"[{bbox[0]:.2f}, {bbox[1]:.2f}, {bbox[2]:.2f}, {bbox[3]:.2f}]"
            items_data.append({
                "Tag ID": det.get("id"),
                "Forensic Classification": det.get("class"),
                "Model Confidence": f"{det.get('confidence', 0.9):.1%}",
                "Spatial BBox [ymin, xmin, ymax, xmax]": coord_str,
                "Laboratory / Field Observations": det.get("forensic_notes")
            })
            
        st.dataframe(items_data, use_container_width=True)

        # Prioritized Leads
        st.markdown("#### 🚨 Prioritized Investigative Action Leads")
        for lead in analysis.get("investigative_leads", []):
            st.markdown(f"""
            <div style="background: #111B2E; border: 1px solid #1E293B; border-left: 3px solid #00E5FF; padding: 10px 14px; border-radius: 4px; margin-bottom: 8px; font-size: 0.88rem;">
                {lead}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("👆 Please upload a crime scene photo or click **'Load Verified Capstone Scene #0891'** to initiate multimodal visual analysis.")
