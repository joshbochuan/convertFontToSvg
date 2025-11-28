import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

FORBIDDEN = {
    '*': "symbol_asterisk",
    '/': "symbol_slash",
    '\\': "symbol_backslash",
    '|': "symbol_pipe",
    ':': "symbol_colon",
    '?': "symbol_question",
    '"': "symbol_quote",
    '<': "symbol_less",
    '>': "symbol_greater",
}

# scale factor for smaller glyphs
SCALE = 0.25

def safe_filename(ch):
    if ch in FORBIDDEN:
        return FORBIDDEN[ch]
    return ch

def glyph_to_svg(font, char, out_path, color="#FF0000"):
    cmap = font.getBestCmap()
    code = ord(char)
    if code not in cmap:
        return False

    glyph_set = font.getGlyphSet()
    glyph_name = cmap[code]
    glyph = glyph_set[glyph_name]

    pen = SVGPathPen(glyph_set)
    glyph.draw(pen)
    path_data = pen.getCommands()

    units_per_em = font["head"].unitsPerEm
    ascent = font["hhea"].ascent
    descent = font["hhea"].descent
    width = font["hmtx"][glyph_name][0]

    # apply scaling and shift
    svg_width = int(width * SCALE)
    svg_height = int(units_per_em * SCALE)


    svg = f"""<svg version="1.1" 
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink"
width="{svg_width}"
height="{svg_height}"
viewBox="0,0,{svg_width},{svg_height}">
<g transform="translate(0,{int(svg_height*0.75)}) scale({SCALE},-{SCALE})">
<g data-paper-data="{{&quot;isPaintingLayer&quot;:true}}" fill="{color}" fill-rule="nonzero" stroke="none" stroke-width="1" stroke-linecap="butt" stroke-linejoin="miter" stroke-miterlimit="10" stroke-dasharray="" stroke-dashoffset="0" style="mix-blend-mode: normal">
<path d="{path_data}"/>
</g></g></svg>"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)

    return True


def main():
    ttf_filename = input("input the ttf file you want to convert: ")
    color = input("input the color you want to use: ")

    root_dir = os.path.splitext(ttf_filename)[0]
    upper_dir = os.path.join(root_dir, "uppercase")
    lower_dir = os.path.join(root_dir, "lowercase")
    chinese_dir = os.path.join(root_dir, "chinese")
    symbol_dir = os.path.join(root_dir, "symbol")
    
    ascii_chars = [chr(i) for i in range(32, 127)]
    chinese_chars = [chr(i) for i in range(0x4E00, 0x9FFF + 1)]

    ALL_CHARS = ascii_chars + chinese_chars

    if not os.path.exists(ttf_filename):
        print(f"❌ {ttf_filename} not found.")
        return

    font = TTFont(ttf_filename)
    os.makedirs(root_dir, exist_ok=True)
    os.makedirs(upper_dir, exist_ok=True)
    os.makedirs(lower_dir, exist_ok=True)
    os.makedirs(symbol_dir, exist_ok=True)
    os.makedirs(chinese_dir, exist_ok=True)
    
    for ch in ALL_CHARS:
        filename = safe_filename(ch) + ".svg"

        if "A" <= ch <= "Z":
            out_path = os.path.join(upper_dir, filename)
        elif "a" <= ch <= "z":
            out_path = os.path.join(lower_dir, filename)
        elif ch <= "~":
            out_path = os.path.join(symbol_dir, filename)
        else:
            out_path = os.path.join(chinese_dir, filename)

        ok = glyph_to_svg(font, ch, out_path, color)
        if ok:
            print(f"✔ {repr(ch)} → {out_path}")
        else:
            print(f"⚠ Missing glyph for {repr(ch)}")

if __name__ == "__main__":
    main()