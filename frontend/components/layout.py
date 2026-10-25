from components.utils import clean_html
from components.icons import icon, ICON_SHIELD_CHECK, ICON_CHECK_CIRCLE, ICON_LOCK, ICON_ACTIVITY

def step_badge(number: int, label: str) -> str:
    """Returns a numbered step badge with serif headline."""
    return clean_html(f"""
    <div style="display: flex; align-items: center; gap: 0.65rem; margin-bottom: 0.75rem;">
        <span style="width: 28px; height: 28px; border-radius: 50%; background-color: #eff6ff; border: 1.5px solid #bfdbfe; color: #1d4ed8; font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 0.85rem; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
            {number}
        </span>
        <span style="font-family: 'Merriweather', serif; font-size: 1.08rem; font-weight: 700; color: #0b0f19;">
            {label}
        </span>
    </div>
    """)

def section_head(title: str, subtitle: str = "") -> str:
    """Returns a clean section header with title and subtitle."""
    sub_markup = f'<p style="color: #64748b; font-size: 0.88rem; margin: 0.25rem 0 0 0;">{subtitle}</p>' if subtitle else ""
    return clean_html(f"""
    <div style="margin-bottom: 1.25rem;">
        <h2 style="font-family: 'Merriweather', serif; font-size: 1.45rem; color: #0b0f19; margin: 0;">{title}</h2>
        {sub_markup}
    </div>
    """)

def callout(title: str, message: str, icon_name: str = ICON_SHIELD_CHECK, variant: str = "blue") -> str:
    """
    Renders an institutional reassurance callout card.
    Variant: blue, green, amber
    """
    colors = {
        "blue": {"bg": "#eff6ff", "border": "#bfdbfe", "title": "#1e40af", "text": "#3b82f6", "icon": "#1d4ed8"},
        "green": {"bg": "#ecfdf5", "border": "#a7f3d0", "title": "#065f46", "text": "#047857", "icon": "#059669"},
        "amber": {"bg": "#fffbeb", "border": "#fde68a", "title": "#92400e", "text": "#b45309", "icon": "#d97706"},
    }.get(variant, {"bg": "#eff6ff", "border": "#bfdbfe", "title": "#1e40af", "text": "#3b82f6", "icon": "#1d4ed8"})

    return clean_html(f"""
    <div style="background-color: {colors['bg']}; border: 1.5px solid {colors['border']}; border-radius: 10px; padding: 1rem 1.25rem; margin-bottom: 1.25rem; display: flex; align-items: flex-start; gap: 0.85rem;">
        <div style="width: 34px; height: 34px; border-radius: 50%; background-color: #ffffff; border: 1px solid {colors['border']}; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 0.1rem;">
            {icon(icon_name, size=18, color=colors['icon'])}
        </div>
        <div>
            <div style="font-weight: 700; color: {colors['title']}; font-size: 0.95rem; margin-bottom: 0.2rem;">
                {title}
            </div>
            <div style="font-size: 0.84rem; color: {colors['text']}; line-height: 1.45;">
                {message}
            </div>
        </div>
    </div>
    """)

def stat_card(label: str, value: str, color: str = "#1d4ed8") -> str:
    """Renders a metric card with clean typography."""
    return clean_html(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value" style="color: {color};">{value}</div>
    </div>
    """)
