# https://playbook.ebay.com/foundations/color/using-color-in-illustration
COLOR_BANDS = {
    "CORAL": [
        "#FFA78A",
        "#F3511B",
        "#D03706",
        "#5E1D08",
    ],
    "TEAL":[
        "#8EDFE5",
        "#1BBFCA",
        "#006F93",
        "#07465A",
    ],
    "Green":[
        "#D5F6AA",
        "#92C821",
        "#507D17",
        "#345110",
    ],
    "Avocado":[
        "#E9F5A0",
        "#4E4E0C",
        "#C1D737",
        "#68770D",
    ]
}

def get_percent_band_color(value, min_val=0.0, max_val=1.0):
    """Assign fixed banded colors to a float value between min and max."""
    try:
        value = float(value)
    except:
        return "#bbbbbb"  # fallback color for N/A or invalid

    if value <= min_val:
        return "#bbbbbb"

    # Normalize to 0-1 range
    ratio = (value - min_val) / (max_val - min_val)
    ratio = max(0, min(1, ratio))

    # PICK YOU COLOR BANDS
    color_bands = COLOR_BANDS["TEAL"]
    num_bands = len(color_bands)
    band_index = int(ratio * num_bands)
    band_index = min(band_index, num_bands - 1)  # avoid overflow

    return color_bands[band_index]

def render_colored_block(label, value, color_value):
    color = get_percent_band_color(color_value)
    return f"<div style='background-color:{color}; padding:10px; border-radius:4px;'><b>{label} :</b> {value}</div>"

def to_float(val):
        try:
            return float(str(val).strip('%')) / 100 if isinstance(val, str) and val.endswith('%') else float(val)
        except:
            return 0.0
