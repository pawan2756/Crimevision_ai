"""
CrimeVision AI - Intelligent Multimodal Forensic Analysis Platform
Skill Wallet Capstone Project 2
Senior Forensic Systems Architect: Production Streamlit Architecture
"""

import datetime
import io
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="CrimeVision AI — Multimodal Forensic Analysis Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Imports from Modular Architecture
from config import (
    APP_NAME, APP_SUBTITLE, APP_VERSION, CLASSIFICATION_BANNER, FORENSIC_CSS
)
from modules.auth_security import (
    initialize_security_state, render_security_sidebar, log_custody_transfer
)
from modules.visual_tagger import (
    render_visual_tagger_tab, get_simulated_rtdetr_detections
)
from modules.audio_transcriber import (
    render_audio_transcriber_tab, get_simulated_audio_forensics
)
from modules.cctv_analyzer import (
    render_cctv_analyzer_tab
)
from modules.multimodal_fusion import (
    render_multimodal_fusion_tab
)
from modules.pdf_exporter import (
    render_pdf_exporter_tab
)
from modules.sample_generator import (
    create_sample_crime_scene_image, create_sample_audio_wav, generate_sample_cctv_keyframes
)

# 3. Inject Forensic CSS Styling
st.markdown(FORENSIC_CSS, unsafe_allow_html=True)

# 4. Initialize Forensic Session State
initialize_security_state()

# Helper: Auto-load entire capstone dossier in 1 click
def load_entire_capstone_case():
    """Loads synchronized evidence across all 5 modules simultaneously."""
    # Tab 1: Image
    sample_img = create_sample_crime_scene_image()
    buf = io.BytesIO()
    sample_img.save(buf, format="JPEG")
    st.session_state.current_image = sample_img
    st.session_state.current_image_bytes = buf.getvalue()
    st.session_state.image_evidence_id = "IMG-EV-2026-0891"
    st.session_state.visual_analysis = get_simulated_rtdetr_detections()
    
    # Tab 2: Audio
    audio_bytes = create_sample_audio_wav()
    st.session_state.current_audio_bytes = audio_bytes
    st.session_state.audio_evidence_id = "AUD-EV-2026-0891"
    st.session_state.audio_analysis = get_simulated_audio_forensics()
    
    # Tab 3: CCTV
    st.session_state.cctv_evidence_id = "VID-EV-2026-0891"
    st.session_state.cctv_keyframes = generate_sample_cctv_keyframes()
    st.session_state.cctv_raw_bytes = b"CCTV_CAPSTONE_VIDEO_MOCK_STREAM_0891"
    
    # Sign-off
    st.session_state.investigator_signoff = True
    
    # Audit log
    log_custody_transfer(
        evidence_id="CASE-2026-CR-0891",
        action="FULL MULTIMODAL DOSSIER INGESTION",
        notes="Capstone Case #0891 ingested across Photographic, Acoustic, and CCTV modalities with Investigator Sign-off."
    )

# 5. Render Sidebar Navigation & Credentials
render_security_sidebar()

# 6. Top Forensic Header & Case Intelligence Banner
utc_now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

st.markdown(f"""
<div class="forensic-banner">
    <span>🛡️ {CLASSIFICATION_BANNER}</span>
    <span>SYSTEM CLOCK: {utc_now}</span>
</div>
""", unsafe_allow_html=True)

head_col1, head_col2 = st.columns([3, 1])
with head_col1:
    st.markdown(f"""
    <div style="margin-bottom: 8px;">
        <h1 style="margin: 0; padding: 0; font-size: 2.1rem; color: #F8FAFC; letter-spacing: -0.5px;">
            🔍 {APP_NAME} <span style="font-size: 1.1rem; color: #00E5FF; font-weight: 400;">v{APP_VERSION}</span>
        </h1>
        <p style="margin: 4px 0 0 0; color: #94A3B8; font-size: 0.95rem;">
            {APP_SUBTITLE} • <em>Skill Wallet Capstone Project 2</em>
        </p>
    </div>
    """, unsafe_allow_html=True)

with head_col2:
    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
    if st.button("🚀 Load Complete Case Dossier #0891", use_container_width=True, type="primary"):
        load_entire_capstone_case()
        st.toast("✅ Multimodal Case Dossier #0891 synchronized across all modules!", icon="🛡️")
        st.rerun()

# Quick Status Chips Banner
chip1, chip2, chip3, chip4 = st.columns(4)
with chip1:
    st.markdown(f"""
    <div class="forensic-card" style="padding: 8px 12px; margin-bottom: 8px;">
        <div style="font-size: 0.7rem; color: #94A3B8;">CASE DOCKET</div>
        <div style="font-family: monospace; font-weight: 700; color: #00E5FF; font-size: 0.88rem;">
            {st.session_state.case_id}
        </div>
    </div>
    """, unsafe_allow_html=True)
with chip2:
    st.markdown(f"""
    <div class="forensic-card" style="padding: 8px 12px; margin-bottom: 8px;">
        <div style="font-size: 0.7rem; color: #94A3B8;">LEAD INVESTIGATOR</div>
        <div style="font-family: monospace; font-weight: 700; color: #F1F5F9; font-size: 0.88rem;">
            {st.session_state.investigator_name}
        </div>
    </div>
    """, unsafe_allow_html=True)
with chip3:
    st.markdown(f"""
    <div class="forensic-card" style="padding: 8px 12px; margin-bottom: 8px;">
        <div style="font-size: 0.7rem; color: #94A3B8;">ACTIVE ENGINE</div>
        <div style="font-family: monospace; font-weight: 700; color: {'#00E676' if not st.session_state.demo_mode else '#FFD600'}; font-size: 0.88rem;">
            {'LIVE API (' + st.session_state.api_provider.split()[0] + ')' if not st.session_state.demo_mode else 'DEMO FALLBACK'}
        </div>
    </div>
    """, unsafe_allow_html=True)
with chip4:
    sig_status = "AFFIRMED (28 USC §1746)" if st.session_state.investigator_signoff else "SIGNOFF PENDING"
    sig_color = "#00E676" if st.session_state.investigator_signoff else "#FFB300"
    st.markdown(f"""
    <div class="forensic-card" style="padding: 8px 12px; margin-bottom: 8px;">
        <div style="font-size: 0.7rem; color: #94A3B8;">CUSTODY INTEGRITY</div>
        <div style="font-family: monospace; font-weight: 700; color: {sig_color}; font-size: 0.88rem;">
            {sig_status}
        </div>
    </div>
    """, unsafe_allow_html=True)

# 7. Main Forensic Navigation Tabs
tab_vis, tab_aud, tab_cctv, tab_fusion, tab_pdf = st.tabs([
    "📸 Tab 1: Visual Evidence Tagger (Epic 2)",
    "🎙️ Tab 2: Witness Audio & Timeline (Epic 3)",
    "📹 Tab 3: CCTV Progression & Penal Codes (Epic 4)",
    "🧩 Tab 4: Multimodal Fusion & Grounded Chat (Epic 5)",
    "📄 Tab 5: Automated Forensic PDF Export (Epic 6)"
])

with tab_vis:
    render_visual_tagger_tab()

with tab_aud:
    render_audio_transcriber_tab()

with tab_cctv:
    render_cctv_analyzer_tab()

with tab_fusion:
    render_multimodal_fusion_tab()

with tab_pdf:
    render_pdf_exporter_tab()

# 8. Forensic Footer & Tamper-Evident Ledger Drawer
st.divider()

with st.expander(f"🔐 Chain-of-Custody Immutable Audit Ledger ({len(st.session_state.custody_ledger)} Verified Records)"):
    st.markdown("""
    Every user action, tensor localization, transcription run, and export operation is cryptographically hashed 
    with **SHA-256** under ISO 27037 digital evidence preservation standards.
    """)
    ledger_records = []
    for entry in st.session_state.custody_ledger:
        ledger_records.append({
            "Log ID": entry.get("log_id"),
            "UTC Timestamp": entry.get("timestamp"),
            "Evidence Ref": entry.get("evidence_id"),
            "Action Undertaken": entry.get("action"),
            "Investigator / System": entry.get("officer"),
            "SHA-256 Checksum": entry.get("hash"),
            "Operational Field Notes": entry.get("notes")
        })
    st.dataframe(ledger_records, use_container_width=True)

st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.78rem; padding: 18px 0 6px 0; font-family: monospace;">
    CRIMEVISION AI • SKILL WALLET CAPSTONE PROJECT 2 • ZERO EXTERNAL DB DEPENDENCY • STREAMLIT COMMUNITY CLOUD READY
</div>
""", unsafe_allow_html=True)
