"""
Icon helper module utilizing native inline SVG vector icons (Zero Emoticons, Zero external scripts).
Renders seamlessly in Streamlit without depending on external web components or CDNs.
"""

# Lucide-standard vector paths (viewBox: 0 0 24 24)
SVG_PATHS = {
    "lucide:shield-check": (
        '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>'
        '<path d="m9 12 2 2 4-4"/>'
    ),
    "lucide:shield-alert": (
        '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>'
        '<path d="M12 8v4"/><path d="M12 16h.01"/>'
    ),
    "lucide:lock": (
        '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/>'
        '<path d="M7 11V7a5 5 0 0 1 10 0v4"/>'
    ),
    "lucide:unlock": (
        '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/>'
        '<path d="M7 11V7a5 5 0 0 1 9.9-1"/>'
    ),
    "lucide:key-round": (
        '<path d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"/>'
        '<circle cx="16.5" cy="7.5" r=".5" fill="currentColor"/>'
    ),
    "lucide:cpu": (
        '<rect width="16" height="16" x="4" y="4" rx="2"/>'
        '<rect width="6" height="6" x="9" y="9" rx="1"/>'
        '<path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/>'
        '<path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/>'
    ),
    "lucide:binary": (
        '<rect x="14" y="4" width="4" height="6" rx="2"/>'
        '<rect x="6" y="14" width="4" height="6" rx="2"/>'
        '<path d="M6 10h2v-6"/><path d="M14 20h2v-6"/>'
    ),
    "lucide:id-card": (
        '<rect width="20" height="14" x="2" y="5" rx="2"/>'
        '<circle cx="8" cy="12" r="2"/>'
        '<path d="M14 10h4"/><path d="M14 14h4"/>'
    ),
    "lucide:file-text": (
        '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/>'
        '<path d="M14 2v4a2 2 0 0 0 2 2h4"/>'
        '<path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>'
    ),
    "lucide:video": (
        '<path d="m22 8-6 4 6 4V8Z"/>'
        '<rect width="14" height="12" x="2" y="6" rx="2" ry="2"/>'
    ),
    "lucide:download": (
        '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>'
        '<polyline points="7 10 12 15 17 10"/>'
        '<line x1="12" x2="12" y1="15" y2="3"/>'
    ),
    "lucide:upload-cloud": (
        '<path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"/>'
        '<path d="M12 12v9"/><path d="m16 16-4-4-4 4"/>'
    ),
    "lucide:user": (
        '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/>'
        '<circle cx="12" cy="7" r="4"/>'
    ),
    "lucide:user-check": (
        '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>'
        '<circle cx="9" cy="7" r="4"/>'
        '<polyline points="16 11 18 13 22 9"/>'
    ),
    "lucide:log-out": (
        '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>'
        '<polyline points="16 17 21 12 16 7"/>'
        '<line x1="21" x2="9" y1="12" y2="12"/>'
    ),
    "lucide:scale": (
        '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/>'
        '<path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/>'
        '<path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>'
    ),
    "lucide:activity": (
        '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>'
    ),
    "lucide:fingerprint": (
        '<path d="M12 10a2 2 0 0 0-2 2c0 1.02-.1 2.51-.26 3"/>'
        '<path d="M14 13.12c0 2.38 0 6.38-1 8.88"/>'
        '<path d="M17.29 21.02c.12-.6.43-2.3.5-3.02"/>'
        '<path d="M2 12a10 10 0 0 1 18-6"/>'
        '<path d="M2 16h.01"/><path d="M21.8 16c.2-2 .131-5.354 0-6"/>'
        '<path d="M5 19.5C5.5 18 6 15 6 12a6 6 0 0 1 .34-2"/>'
        '<path d="M8.65 22c.21-.66.45-1.32.57-2"/>'
        '<path d="M9 6.8a6 6 0 0 1 9 5.2v2"/>'
    ),
    "lucide:check-circle-2": (
        '<circle cx="12" cy="12" r="10"/>'
        '<path d="m9 12 2 2 4-4"/>'
    ),
    "lucide:alert-triangle": (
        '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>'
        '<line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/>'
    ),
    "lucide:zap": (
        '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>'
    ),
    "lucide:archive": (
        '<rect width="20" height="5" x="2" y="3" rx="1"/>'
        '<path d="M4 8v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8"/>'
        '<path d="M10 12h4"/>'
    ),
    "lucide:arrow-right": (
        '<line x1="5" y1="12" x2="19" y2="12"/>'
        '<polyline points="12 5 19 12 12 19"/>'
    ),
    "lucide:search": (
        '<circle cx="11" cy="11" r="8"/>'
        '<line x1="21" y1="21" x2="16.65" y2="16.65"/>'
    ),
    "lucide:eye": (
        '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/>'
        '<circle cx="12" cy="12" r="3"/>'
    )
}

def icon(name: str, size: int = 18, color: str = "currentColor", extra_class: str = "") -> str:
    """
    Renders an inline SVG vector element.
    Example: icon("lucide:shield-check", size=20, color="#1d4ed8")
    """
    path = SVG_PATHS.get(name, "")
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round" class="{extra_class}" '
        f'style="vertical-align: -0.15em; display: inline-block; flex-shrink: 0;">'
        f'{path}'
        f'</svg>'
    )

# Standard icon constants for SecureReport
ICON_SHIELD_CHECK = "lucide:shield-check"
ICON_SHIELD_ALERT = "lucide:shield-alert"
ICON_LOCK = "lucide:lock"
ICON_UNLOCK = "lucide:unlock"
ICON_KEY = "lucide:key-round"
ICON_CPU = "lucide:cpu"
ICON_BINARY = "lucide:binary"
ICON_ID_CARD = "lucide:id-card"
ICON_FILE_TEXT = "lucide:file-text"
ICON_VIDEO = "lucide:video"
ICON_DOWNLOAD = "lucide:download"
ICON_UPLOAD = "lucide:upload-cloud"
ICON_USER = "lucide:user"
ICON_USER_CHECK = "lucide:user-check"
ICON_LOG_OUT = "lucide:log-out"
ICON_SCALE = "lucide:scale"
ICON_ACTIVITY = "lucide:activity"
ICON_FINGERPRINT = "lucide:fingerprint"
ICON_CHECK_CIRCLE = "lucide:check-circle-2"
ICON_ALERT_TRIANGLE = "lucide:alert-triangle"
ICON_ZAP = "lucide:zap"
ICON_ARCHIVE = "lucide:archive"
ICON_ARROW_RIGHT = "lucide:arrow-right"
ICON_SEARCH = "lucide:search"
ICON_EYE = "lucide:eye"
