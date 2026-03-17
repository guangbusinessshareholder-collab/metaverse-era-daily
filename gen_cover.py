from PIL import Image, ImageDraw, ImageFont
import os

W, H = 900, 500
img = Image.new('RGB', (W, H), color=(8, 12, 20))
draw = ImageDraw.Draw(img)

# Grid lines
for x in range(0, W, 40):
    draw.line([(x, 0), (x, H)], fill=(0, 212, 255, 10), width=1)
for y in range(0, H, 40):
    draw.line([(0, y), (W, y)], fill=(0, 212, 255, 10), width=1)

# Gradient overlay (simulate with rectangles)
for i in range(H):
    alpha = int(15 * (1 - i/H))
    draw.line([(0, i), (W, i)], fill=(0, 30, 60))

# Top accent bar
draw.rectangle([0, 0, W, 4], fill=(0, 212, 255))

# Glow circles
for cx, cy, r, color in [
    (750, 80, 180, (123, 47, 255)),
    (100, 400, 120, (0, 212, 255)),
]:
    for ri in range(r, 0, -4):
        alpha = int(30 * (1 - ri/r))
        draw.ellipse([cx-ri, cy-ri, cx+ri, cy+ri], fill=(*color, alpha))

# Badge
draw.rectangle([50, 45, 260, 75], fill=(0, 30, 50), outline=(0, 212, 255), width=1)

# Title area
draw.rectangle([40, 90, W-40, 210], fill=(13, 20, 33))
draw.rectangle([40, 90, 46, 210], fill=(0, 212, 255))

# Bottom bar
draw.rectangle([0, H-50, W, H], fill=(13, 20, 33))
draw.line([(0, H-50), (W, H-50)], fill=(0, 212, 255, 60), width=1)

# Try to load a font, fallback to default
try:
    font_big = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 52)
    font_med = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 26)
    font_small = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 20)
    font_tiny = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 16)
    font_en = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
    font_en_sm = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
except:
    font_big = font_med = font_small = font_tiny = font_en = font_en_sm = ImageFont.load_default()

# Badge text
draw.text((58, 50), "  元宇纪研发部 · 情报中心", font=font_en_sm, fill=(0, 212, 255))

# Main title
draw.text((60, 100), "每日科技早报", font=font_big, fill=(232, 244, 253))

# Subtitle
draw.text((60, 170), "AI 研发总监实时搜索 · 10条全球科技前沿", font=font_med, fill=(138, 163, 187))

# News snippets
snippets = [
    "01  NVIDIA GTC 2026：Vera Rubin架构，万亿美元订单",
    "02  Apple iPhone 17e：16核Neural Engine生成式AI",
    "03  Google+Accel：5家AI创业公司各获200万美元",
    "04  全球电商规模预计达8.1万亿美元",
]
for i, text in enumerate(snippets):
    y = 230 + i * 38
    draw.rectangle([50, y, 56, y+24], fill=(0, 212, 255))
    draw.text((68, y), text, font=font_small, fill=(180, 210, 235))

# Date and branding
draw.text((50, H-35), "2026.03.17  MON", font=font_en_sm, fill=(0, 212, 255))
draw.text((W-200, H-35), "METAVERSE ERA", font=font_en_sm, fill=(74, 98, 120))

# Right decorative element
draw.rectangle([W-120, 230, W-50, 380], fill=(13, 25, 45), outline=(0, 212, 255, 30), width=1)
draw.text((W-115, 265), "09", font=font_big, fill=(0, 212, 255))
draw.text((W-107, 330), ":30", font=font_med, fill=(74, 98, 120))
draw.text((W-102, 360), "DAILY", font=font_en_sm, fill=(74, 98, 120))

output = '/Users/zian/.openclaw/workspace-rd/daily-news/cover.png'
img.save(output, 'PNG', optimize=True)
print(f"saved: {output} ({os.path.getsize(output)//1024}KB)")
