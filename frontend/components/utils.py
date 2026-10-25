def clean_html(html_str: str) -> str:
    """
    Strips all leading and trailing whitespace from every line to ensure
    Streamlit's Markdown parser never misinterprets indented HTML as
    indented code blocks (<pre><code>).
    """
    if not html_str:
        return ""
    return "\n".join(line.strip() for line in html_str.splitlines() if line.strip())
