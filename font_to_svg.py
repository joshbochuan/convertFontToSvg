import os
import math
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
SCALE = 0.02

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
    svg_width = math.ceil(width * SCALE)
    svg_height = int(units_per_em * SCALE)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{int(1.2*svg_height)}" viewbox="0 0 {svg_width} {int(1.2*svg_height)}">
<g transform="translate(0,{int(0.9*svg_height)}) scale({SCALE},-{SCALE})">
<g fill="{color}">
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
    fullwidth_symbol_dir = os.path.join(root_dir, "fullwidth_symbol")
    
    ascii_chars = [chr(i) for i in range(32, 127)]
    chinese_chars = ""
    with open("chineseChar.txt", 'r', encoding='utf-8') as file:
        chinese_chars = file.read()
    tc = list()
    for i in chinese_chars:
        if ord(i) <= 127:
            continue
        tc.append(i)
    fullwidth_symbol = [0x3000, 0x3002, 0x300C, 0x300D, 0x3001, 0x30FB] + list(range(0xFF01, 0xFFEF+1))
    fullwidth_symbol = list(map(chr, fullwidth_symbol))

    if not os.path.exists(ttf_filename):
        print(f"❌ {ttf_filename} not found.")
        return

    font = TTFont(ttf_filename)
    os.makedirs(root_dir, exist_ok=True)
    os.makedirs(upper_dir, exist_ok=True)
    os.makedirs(lower_dir, exist_ok=True)
    os.makedirs(symbol_dir, exist_ok=True)
    os.makedirs(chinese_dir, exist_ok=True)
    os.makedirs(fullwidth_symbol_dir, exist_ok=True)
    
    asciiOK, tcOK, fullwidthOK = 0, 0, 0
    for ch in ascii_chars:
        filename = safe_filename(ch) + ".svg"

        if "A" <= ch <= "Z":
            out_path = os.path.join(upper_dir, filename)
        elif "a" <= ch <= "z":
            out_path = os.path.join(lower_dir, filename)
        else:
            out_path = os.path.join(symbol_dir, filename)

        ok = glyph_to_svg(font, ch, out_path, color)
        if ok:
            asciiOK += 1
            print(f"✔ {repr(ch)} → {out_path}")
        else:
            print(f"⚠ Missing glyph for {repr(ch)}")
    for ch in fullwidth_symbol:
        filename = ch + ".svg"
        out_path = os.path.join(fullwidth_symbol_dir, filename)
        ok = glyph_to_svg(font, ch, out_path, color)
        if ok:
            fullwidthOK += 1
            print(f"✔ {repr(ch)} → {out_path}")
        else:
            print(f"⚠ Missing glyph for {repr(ch)}")
    for ch in tc:
        filename = ch + ".svg"
        out_path = os.path.join(chinese_dir, filename)
        ok = glyph_to_svg(font, ch, out_path, color)
        if ok:
            tcOK += 1
            print(f"✔ {repr(ch)} → {out_path}")
        else:
            print(f"⚠ Missing glyph for {repr(ch)}")
    print(f"ascii: {asciiOK}/{len(ascii_chars)}")
    print(f"fw   : {fullwidthOK}/{len(fullwidth_symbol)}")
    print(f"tc   : {tcOK}/{len(tc)}")

if __name__ == "__main__":
    main()