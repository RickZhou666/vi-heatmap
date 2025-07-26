def get_shaded_blue(value, min_val=0.0, max_val=1.0):
    """Convert a percentage string like '99.7%' to a blue color hex code."""
    try:
        value = float(value)
    except:
        return "#bbbbbb"  # fallback for N/A or invalid
    
    if value == 0.0:
        return "#bbbbbb"  # light gray for 0.0 values

    # Normalize
    ratio = (value - min_val) / (max_val - min_val)
    ratio = max(0, min(1, ratio))

    # Blue color interpolation from light to dark
    # Light: #cfe2f3  → RGB(207,226,243)
    # Dark:  #08306b  → RGB(8,48,107)
    r = int(207 + (8 - 207) * ratio)
    g = int(226 + (48 - 226) * ratio)
    b = int(243 + (107 - 243) * ratio)
    return f"rgb({r},{g},{b})"

def render_colored_block(label, value, color_value):
    color = get_shaded_blue(color_value)
    return f"<div style='background-color:{color}; padding:10px; border-radius:4px;'><b>{label} :</b> {value}</div>"

def to_float(val):
        try:
            return float(str(val).strip('%')) / 100 if isinstance(val, str) and val.endswith('%') else float(val)
        except:
            return 0.0
