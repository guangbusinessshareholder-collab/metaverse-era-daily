from PIL import Image, ImageDraw, ImageFont
import os, textwrap

W, H = 750, 1334  # iPhone-style portrait
img = Image.new('RGB', (W, H), color=(8, 12, 20))
draw = ImageDraw.Draw(img)

# Background grid
for x in range(0, W, 30):
    draw.line([(x, 0), (x, H)], fill=(0, 40, 70), width=1)
for y in range(0, H, 30):
    draw.line([(0, y), (W, y)], fill=(0, 40, 70), width=1)

# Glow orb top right
for r in range(250, 0, -5):
    alpha = max(0, int(20 * (1 - r/250)))
    draw.ellipse([W-r, -r, W+r, r], fill=(123, 47, 255))

# Glow orb bottom left
for r in range(200, 0, -5):
    draw.ellipse([-r, H-r, r, H+r], fill=(0, 100, 150))

# Load fonts
try:
    f_xl   = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 56)
    f_lg   = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 36)
    f_md   = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 26)
    f_sm   = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 22)
    f_xs   = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 18)
    f_en   = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
    f_en_sm= ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 17)
    f_en_xs= ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
except:
    f_xl = f_lg = f_md = f_sm = f_xs = f_en = f_en_sm = f_en_xs = ImageFont.load_default()

NEON_BLUE   = (0, 212, 255)
NEON_PURPLE = (123, 47, 255)
NEON_GREEN  = (0, 255, 136)
NEON_ORANGE = (255, 107, 53)
WHITE       = (232, 244, 253)
GRAY        = (138, 163, 187)
MUTED       = (74, 98, 120)
CARD_BG     = (13, 20, 33)

# ── TOP ACCENT BAR ──
draw.rectangle([0, 0, W, 5], fill=NEON_BLUE)

# ── HEADER ──
y = 30
draw.rectangle([30, y, 220, y+34], fill=(0, 25, 45), outline=NEON_BLUE, width=1)
draw.text((42, y+6), "METAVERSE ERA · 元宇纪", font=f_en_xs, fill=NEON_BLUE)

y = 80
draw.text((30, y), "每日科技早报", font=f_xl, fill=WHITE)
y = 148
draw.text((30, y), "DAILY TECH INTELLIGENCE", font=f_en_sm, fill=MUTED)

# Date pill
draw.rounded_rectangle([30, 185, 220, 218], radius=14, fill=(0, 212, 255, 30), outline=NEON_BLUE, width=1)
draw.text((50, 192), "2026.03.17  MON", font=f_en_sm, fill=NEON_BLUE)

# Divider
draw.rectangle([30, 232, W-30, 234], fill=(0, 212, 255))

# ── NEWS ITEMS ──
news = [
    ("01", "🖥️", "NVIDIA", "GTC 2026：Vera Rubin架构发布，披露万亿美元AI订单", NEON_BLUE),
    ("02", "📱", "Apple", "iPhone 17e发布：16核Neural Engine专为生成式AI设计", (160,160,160)),
    ("03", "💰", "Google", "AI基金选出5家创业公司，每家获200万美元+算力资源", (66,133,244)),
    ("04", "🧠", "Anthropic", "Claude Opus 4.6发布，成AI开发者首选推理模型", NEON_ORANGE),
    ("05", "🛒", "电商趋势", "全球电商规模将达8.1万亿美元，AI成卖家生存标配", NEON_BLUE),
    ("06", "⚙️", "外贸AI", "AI+ERP成标配，RCEP推动东南亚出口新机遇", NEON_GREEN),
    ("07", "🚀", "一人公司", "5个AI工具运营一人公司，ChatGPT用户大量转向Claude", NEON_PURPLE),
    ("08", "🎯", "社交创业", "Solo创始人发布Jusssmile：AI驱动技能变现平台上线", NEON_PURPLE),
    ("09", "🤖", "物理AI", "NVIDIA×Disney：Olaf机器人正式在主题公园大规模落地", (255,45,120)),
    ("10", "📉", "AI成本", "AI价格战加剧：苹果仅投146亿，模型商品化趋势明确", NEON_GREEN),
]

item_h = 90
y_start = 250

for i, (num, icon, tag, title, color) in enumerate(news):
    y = y_start + i * item_h
    # Card bg
    draw.rounded_rectangle([25, y+4, W-25, y+item_h-4], radius=10, fill=CARD_BG)
    # Left accent
    draw.rounded_rectangle([25, y+4, 30, y+item_h-4], radius=2, fill=color)

    # Number
    draw.text((40, y+12), num, font=f_en_xs, fill=color)
    # Icon
    draw.text((70, y+8), icon, font=f_sm, fill=WHITE)
    # Tag
    draw.rounded_rectangle([108, y+12, 108+len(tag)*13+8, y+30], radius=4, fill=(*color[:3], 40))
    draw.text((112, y+13), tag, font=f_en_xs, fill=color)
    # Title - wrap at ~24 chars
    words = title
    if len(words) > 22:
        mid = title.rfind('，', 0, 24) or title.rfind('：', 0, 24) or 22
        line1 = title[:mid+1] if mid > 0 else title[:22]
        line2 = title[mid+1:] if mid > 0 else title[22:]
        draw.text((40, y+33), line1, font=f_xs, fill=WHITE)
        draw.text((40, y+55), line2, font=f_xs, fill=GRAY)
    else:
        draw.text((40, y+40), title, font=f_sm, fill=WHITE)

# ── FOOTER ──
fy = H - 80
draw.rectangle([0, fy, W, fy+1], fill=(0, 212, 255, 60))
draw.text((30, fy+15), "由元宇纪AI研发总监自动生成 · 每日09:30更新", font=f_xs, fill=MUTED)

qr_text = "guangbusinessshareholder-collab.github.io/metaverse-era-daily"
draw.text((30, fy+40), "🔗 " + qr_text[:45], font=f_en_xs, fill=(0, 150, 180))

out = '/Users/zian/.openclaw/workspace-rd/daily-news/poster.png'
img.save(out, 'PNG', optimize=True)
print(f"✅ poster saved: {out} ({os.path.getsize(out)//1024}KB)")
