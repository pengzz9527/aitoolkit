#!/usr/bin/env python3
"""Batch generate 1200x630 OG images for all aitoolkit tools."""
import os, re, sys
from PIL import Image, ImageDraw, ImageFont

TOOLS_DIR = "/root/aitoolkit/content/tools"
OUT_DIR = "/root/aitoolkit/static/images/og/tools"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

os.makedirs(OUT_DIR, exist_ok=True)

# Color palettes by category
CAT_COLORS = {
    "开发工具": {"from": "#1a1a2e", "to": "#16213e", "accent": "#4361ee"},
    "文本处理": {"from": "#16213e", "to": "#0f3460", "accent": "#4cc9f0"},
    "编码解码": {"from": "#1a1a2e", "to": "#2d1b69", "accent": "#7209b7"},
    "网络工具": {"from": "#0f3460", "to": "#1a3a5c", "accent": "#00b4d8"},
    "安全工具": {"from": "#1a1a2e", "to": "#3d0000", "accent": "#e63946"},
    "格式转换": {"from": "#16213e", "to": "#1a3a2e", "accent": "#06d6a0"},
    "设计工具": {"from": "#2d1b69", "to": "#1a1a2e", "accent": "#f72585"},
    "时间工具": {"from": "#1a3a5c", "to": "#16213e", "accent": "#ffd166"},
    "数学工具": {"from": "#16213e", "to": "#0f3460", "accent": "#118ab2"},
    "趣味工具": {"from": "#2d1b69", "to": "#3d0000", "accent": "#ef476f"},
}

def parse_frontmatter(filepath):
    """Extract title, icon, description, categories from Hugo frontmatter."""
    with open(filepath, "r") as f:
        content = f.read()
    
    # Match YAML frontmatter between --- delimiters
    m = re.match(r'^---\s+(.*?)\s+---', content, re.DOTALL)
    if not m:
        return None
    
    fm = m.group(1)
    
    def get_val(key):
        # Match: key: "value" or key: value
        p = re.compile(r'^' + re.escape(key) + r':\s*"(.+?)"\s*$', re.MULTILINE)
        m = p.search(fm)
        if m:
            return m.group(1)
        p2 = re.compile(r'^' + re.escape(key) + r':\s*(.+?)\s*$', re.MULTILINE)
        m = p2.search(fm)
        if m:
            return m.group(1).strip()
        return ""
    
    title = get_val("title")
    icon = get_val("icon")
    desc = get_val("description")
    categories_raw = get_val("categories")
    
    # Parse list: ["cat1", "cat2"]
    cats = []
    if categories_raw:
        cats = re.findall(r'"([^"]+)"', categories_raw)
        if not cats:
            cats = [categories_raw.strip("[]\" ")]
    
    return {
        "title": title,
        "icon": icon or "🔧",
        "description": desc,
        "categories": cats,
    }

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def gradient(draw, size, color_from, color_to):
    """Draw a vertical gradient background."""
    rf, gf, bf = hex_to_rgb(color_from)
    rt, gt, bt = hex_to_rgb(color_to)
    for y in range(size[1]):
        r = int(rf + (rt - rf) * y / size[1])
        g = int(gf + (gt - gf) * y / size[1])
        b = int(bf + (bt - bf) * y / size[1])
        draw.line([(0, y), (size[0], y)], fill=(r, g, b))

def generate_og(name, tool_name, icon, categories):
    """Generate a single 1200x630 OG image."""
    cat = categories[0] if categories else "开发工具"
    palette = CAT_COLORS.get(cat, CAT_COLORS["开发工具"])
    
    img = Image.new("RGB", (1200, 630), "#1a1a2e")
    draw = ImageDraw.Draw(img)
    
    # Background gradient
    gradient(draw, (1200, 630), palette["from"], palette["to"])
    
    # Subtle grid pattern
    for x in range(0, 1200, 40):
        draw.line([(x, 0), (x, 630)], fill=(255, 255, 255, 5), width=1)
    for y in range(0, 630, 40):
        draw.line([(0, y), (1200, y)], fill=(255, 255, 255, 5), width=1)
    
    # Accent bar
    draw.rectangle([(0, 0), (8, 630)], fill=hex_to_rgb(palette["accent"]))
    
    # Try to load fonts
    title_font = None
    icon_font = None
    domain_font = None
    cat_font = None
    
    try:
        title_font = ImageFont.truetype(FONT_BOLD, 52)
    except:
        title_font = ImageFont.load_default()
    try:
        icon_font = ImageFont.truetype(FONT_BOLD, 90)
    except:
        icon_font = ImageFont.load_default()
    try:
        domain_font = ImageFont.truetype(FONT_SANS, 28)
    except:
        domain_font = ImageFont.load_default()
    try:
        cat_font = ImageFont.truetype(FONT_SANS, 22)
    except:
        cat_font = ImageFont.load_default()
    
    # Emoji icon
    draw.text((80, 100), icon, font=icon_font, fill="#ffffff")
    
    # Tool name
    display_title = tool_name if tool_name else name.replace("-", " ").title()
    # Handle CJK text that might be too long
    if len(display_title) > 16:
        display_title = display_title[:15] + "…"
    draw.text((80, 210), display_title, font=title_font, fill="#ffffff")
    
    # Category badge
    draw.rounded_rectangle([(80, 300), (80 + len(cat) * 22, 340)], radius=6, fill=hex_to_rgb(palette["accent"]))
    draw.text((88, 306), cat, font=cat_font, fill="#ffffff")
    
    # Domain + tagline
    draw.text((80, 500), "198007.xyz | 免费在线工具", font=domain_font, fill="#8888aa")
    
    # Bottom accent line
    draw.rectangle([(80, 560), (500, 564)], fill=hex_to_rgb(palette["accent"]))
    
    outpath = os.path.join(OUT_DIR, f"{name}.png")
    img.save(outpath, "PNG")
    return outpath

def main():
    tools = sorted(os.listdir(TOOLS_DIR))
    count = 0
    for tool_dir in tools:
        index_path = os.path.join(TOOLS_DIR, tool_dir, "index.md")
        if not os.path.isfile(index_path):
            continue
        fm = parse_frontmatter(index_path)
        if fm:
            out = generate_og(tool_dir, fm["title"], fm["icon"] or "🔧", fm["categories"])
        else:
            out = generate_og(tool_dir, "", "🔧", [])
        print(f"  [{count+1}] {tool_dir} -> {out}")
        count += 1
    
    print(f"\n✅ {count} OG images generated in {OUT_DIR}")

if __name__ == "__main__":
    main()
