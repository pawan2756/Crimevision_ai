"""
CrimeVision AI - Forensic Systems Configuration & Taxonomies
Skill Wallet Capstone Project 2
"""

APP_NAME = "CrimeVision AI"
APP_SUBTITLE = "Intelligent Multimodal Forensic Analysis Platform"
APP_VERSION = "2.4.0-PROD"
CLASSIFICATION_BANNER = "RESTRICTED LAW ENFORCEMENT SENSITIVE (LES) // CJIS COMPLIANT"

# Forensic Threat Taxonomy
THREAT_LEVELS = {
    "LOW": {"color": "#00E676", "bg": "rgba(0, 230, 118, 0.12)", "border": "#00E676", "badge": "🟢 LOW THREAT"},
    "MEDIUM": {"color": "#FFD600", "bg": "rgba(255, 214, 0, 0.12)", "border": "#FFD600", "badge": "🟡 MEDIUM THREAT"},
    "HIGH": {"color": "#FF9100", "bg": "rgba(255, 145, 0, 0.15)", "border": "#FF9100", "badge": "🟠 HIGH THREAT"},
    "CRITICAL": {"color": "#FF1744", "bg": "rgba(255, 23, 68, 0.20)", "border": "#FF1744", "badge": "🔴 CRITICAL THREAT"},
}

# Scene Classification Taxonomy
SCENE_CLASSES = [
    "Burglary (Forced Entry)",
    "Homicide Investigation",
    "Armed Robbery in Progress",
    "Aggravated Assault with Deadly Weapon",
    "Felony Vandalism & Property Destruction",
    "Suspicious Death Unattended"
]

# RT-DETR Visual Evidence Classes & Visualization Palette
DETECTION_CLASSES = {
    "Person (Suspect)": {"color": "#FF5252", "hex": "#FF5252", "icon": "👤"},
    "Person (Victim)": {"color": "#448AFF", "hex": "#448AFF", "icon": "👥"},
    "Firearm (Handgun)": {"color": "#FF1744", "hex": "#FF1744", "icon": "🔫"},
    "Firearm (Rifle)": {"color": "#D50000", "hex": "#D50000", "icon": "🎯"},
    "Edged Weapon (Knife)": {"color": "#FF3D00", "hex": "#FF3D00", "icon": "🔪"},
    "Blood Spatter (Impact)": {"color": "#E91E63", "hex": "#E91E63", "icon": "🩸"},
    "Forced Entry (Pried Lock)": {"color": "#FFEA00", "hex": "#FFEA00", "icon": "🚪"},
    "Shattered Glass": {"color": "#00E5FF", "hex": "#00E5FF", "icon": "🪟"},
    "Getaway Vehicle": {"color": "#7C4DFF", "hex": "#7C4DFF", "icon": "🚗"},
}

# Penal Code Violations Taxonomy
PENAL_CODES = {
    "PC 459": {
        "title": "Commercial Burglary (Felony)",
        "statute": "Cal. Penal Code § 459",
        "description": "Unauthorized entry into building with intent to commit grand theft or felony.",
        "severity": "FELONY CLASS B"
    },
    "PC 245(a)(2)": {
        "title": "Assault with a Firearm",
        "statute": "Cal. Penal Code § 245(a)(2)",
        "description": "Assault upon another person with a firearm or deadly weapon.",
        "severity": "VIOLENT FELONY"
    },
    "PC 211": {
        "title": "Second Degree Robbery",
        "statute": "Cal. Penal Code § 211",
        "description": "Felonious taking of personal property in possession of another by means of force or fear.",
        "severity": "STRIKE FELONY"
    },
    "PC 594(b)(1)": {
        "title": "Felony Vandalism (Damage > $400)",
        "statute": "Cal. Penal Code § 594(b)(1)",
        "description": "Malicious defacement, damage, or destruction of commercial property.",
        "severity": "FELONY CLASS D"
    },
    "VC 2800.2": {
        "title": "Reckless Evading of Peace Officer",
        "statute": "Cal. Veh. Code § 2800.2",
        "description": "Fleeing pursuing peace officer with willful or wanton disregard for safety.",
        "severity": "FELONY/MISDEMEANOR WOBBLER"
    },
    "PC 187(a)": {
        "title": "Murder Investigation Pre-Charge",
        "statute": "Cal. Penal Code § 187(a)",
        "description": "Unlawful killing of human being with malice aforethought.",
        "severity": "CAPITAL FELONY"
    }
}

# Custom Dark Forensic Theme CSS
FORENSIC_CSS = """
<style>
/* Main Background & Clean Typography */
.stApp {
    background-color: #0A0E17;
    color: #E2E8F0;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
}

/* Header & Banner Styling */
.forensic-banner {
    background: linear-gradient(90deg, #10192C 0%, #17243F 50%, #10192C 100%);
    border: 1px solid #1E293B;
    border-left: 4px solid #00E5FF;
    padding: 10px 18px;
    border-radius: 6px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 0.82rem;
    letter-spacing: 1.5px;
    color: #00E5FF;
    text-transform: uppercase;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    box-shadow: 0 4px 14px rgba(0, 229, 255, 0.08);
}

.forensic-title-card {
    background: linear-gradient(135deg, #131C31 0%, #0F172A 100%);
    border: 1px solid #1E293B;
    border-radius: 10px;
    padding: 20px 24px;
    margin-bottom: 20px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
}

/* Forensic Status Cards */
.forensic-card {
    background: #111827;
    border: 1px solid #1F2937;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
}

.forensic-card-highlight {
    background: #111B2E;
    border: 1px solid #00E5FF;
    border-radius: 8px;
    padding: 16px;
    box-shadow: 0 0 15px rgba(0, 229, 255, 0.15);
}

/* Threat Badges */
.threat-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 4px;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 1px;
    font-family: 'Consolas', monospace;
    text-transform: uppercase;
}

/* Evidence ID Chips */
.evidence-chip {
    background: #1E293B;
    color: #38BDF8;
    border: 1px solid #38BDF8;
    border-radius: 4px;
    padding: 2px 8px;
    font-family: 'Consolas', monospace;
    font-size: 0.8rem;
    font-weight: 600;
}

/* Custom Tab Highlighting */
button[data-baseweb="tab"] {
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding-top: 10px !important;
    padding-bottom: 10px !important;
    transition: all 0.2s ease-in-out;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #00E5FF !important;
    border-bottom-color: #00E5FF !important;
}

/* Metric card styling */
div[data-testid="stMetric"] {
    background: #111827;
    border: 1px solid #1F2937;
    border-radius: 8px;
    padding: 12px 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

div[data-testid="stMetricLabel"] {
    color: #94A3B8;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

div[data-testid="stMetricValue"] {
    color: #F8FAFC;
    font-family: 'Consolas', monospace;
}

/* Table aesthetic */
.stDataFrame {
    border: 1px solid #1E293B;
    border-radius: 8px;
    overflow: hidden;
}

/* Custom forensic scrollbar */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #0A0E17;
}
::-webkit-scrollbar-thumb {
    background: #1E293B;
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: #00E5FF;
}
</style>
"""
