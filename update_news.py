#!/usr/bin/env python3
"""
元宇纪每日早报 HTML 生成脚本
用法：python3 update_news.py '{"date":"2026.03.17","news":[...]}'
或直接 import 调用 generate_html(date_str, news_list)
"""
import sys, json, os, subprocess
from datetime import datetime

TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<meta name="description" content="元宇纪研发部 · 每日全球科技前沿情报">
<title>元宇纪每日早报 · {DATE}</title>
<meta property="og:title" content="元宇纪每日早报 · {DATE}">
<meta property="og:description" content="{OG_DESC}">
<meta property="og:type" content="article">
<meta property="og:image" content="https://guangbusinessshareholder-collab.github.io/metaverse-era-daily/cover.png">
<meta property="og:image:width" content="900">
<meta property="og:image:height" content="500">
<meta property="og:url" content="https://guangbusinessshareholder-collab.github.io/metaverse-era-daily/">
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap');
:root{{--neon-blue:#00d4ff;--neon-purple:#7b2fff;--neon-green:#00ff88;--neon-orange:#ff6b35;--dark-bg:#080c14;--card-bg:#0d1421;--card-border:rgba(0,212,255,0.15);--text-primary:#e8f4fd;--text-secondary:#8aa3bb;--text-muted:#4a6278}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:var(--dark-bg);color:var(--text-primary);font-family:'Inter',-apple-system,sans-serif;min-height:100vh;overflow-x:hidden}}
body::before{{content:'';position:fixed;top:0;left:0;right:0;bottom:0;background-image:linear-gradient(rgba(0,212,255,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(0,212,255,0.03) 1px,transparent 1px);background-size:40px 40px;z-index:0;pointer-events:none}}
body::after{{content:'';position:fixed;width:600px;height:600px;background:radial-gradient(circle,rgba(123,47,255,0.08) 0%,transparent 70%);top:-200px;right:-200px;z-index:0;pointer-events:none}}
.container{{max-width:780px;margin:0 auto;padding:0 16px 40px;position:relative;z-index:1}}
.header{{padding:28px 0 20px;text-align:center}}
.header-badge{{display:inline-flex;align-items:center;gap:6px;background:rgba(0,212,255,0.08);border:1px solid rgba(0,212,255,0.25);border-radius:20px;padding:4px 14px;font-size:11px;font-weight:600;color:var(--neon-blue);letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px}}
.header-badge::before{{content:'';width:6px;height:6px;border-radius:50%;background:var(--neon-blue);animation:pulse 2s infinite}}
@keyframes pulse{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:0.4;transform:scale(0.8)}}}}
.header h1{{font-family:'Orbitron',sans-serif;font-size:clamp(22px,5vw,36px);font-weight:900;background:linear-gradient(135deg,#fff 0%,var(--neon-blue) 50%,var(--neon-purple) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.2;margin-bottom:8px}}
.header-sub{{font-size:13px;color:var(--text-secondary)}}
.header-sub span{{color:var(--neon-blue);font-weight:600}}
.date-line{{display:flex;align-items:center;gap:12px;margin:20px 0}}
.date-line::before,.date-line::after{{content:'';flex:1;height:1px;background:linear-gradient(90deg,transparent,rgba(0,212,255,0.3),transparent)}}
.date-text{{font-family:'Orbitron',sans-serif;font-size:12px;color:var(--neon-blue);letter-spacing:2px;white-space:nowrap}}
.stats-bar{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:24px}}
.stat-item{{background:rgba(0,212,255,0.04);border:1px solid rgba(0,212,255,0.12);border-radius:12px;padding:12px;text-align:center}}
.stat-value{{font-family:'Orbitron',sans-serif;font-size:18px;font-weight:700;color:var(--neon-blue);display:block}}
.stat-label{{font-size:10px;color:var(--text-muted);letter-spacing:0.5px;margin-top:2px}}
.news-grid{{display:flex;flex-direction:column;gap:14px}}
.news-card{{background:var(--card-bg);border:1px solid var(--card-border);border-radius:16px;overflow:hidden;transition:all 0.3s ease;position:relative}}
.news-card::before{{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:var(--accent-color,var(--neon-blue));opacity:0.6}}
.news-card:hover{{border-color:rgba(0,212,255,0.35);transform:translateY(-2px);box-shadow:0 8px 30px rgba(0,0,0,0.4),0 0 20px rgba(0,212,255,0.06)}}
.card-inner{{display:flex}}
.card-visual{{width:90px;min-height:100px;display:flex;flex-direction:column;align-items:center;justify-content:center;background:var(--accent-bg,rgba(0,212,255,0.06));flex-shrink:0;position:relative;overflow:hidden}}
.card-visual::after{{content:'';position:absolute;width:80px;height:80px;border-radius:50%;background:var(--accent-glow,rgba(0,212,255,0.1));filter:blur(20px)}}
.card-number{{font-family:'Orbitron',sans-serif;font-size:10px;font-weight:700;color:var(--accent-color,var(--neon-blue));opacity:0.6;letter-spacing:1px;position:relative;z-index:1;margin-bottom:4px}}
.card-icon{{font-size:28px;position:relative;z-index:1;filter:drop-shadow(0 0 8px var(--accent-color,var(--neon-blue)))}}
.card-content{{padding:14px 16px;flex:1;min-width:0}}
.card-tag{{display:inline-block;font-size:9px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:var(--accent-color,var(--neon-blue));background:var(--accent-bg,rgba(0,212,255,0.08));border-radius:4px;padding:2px 7px;margin-bottom:6px}}
.card-title{{font-size:14px;font-weight:700;color:var(--text-primary);line-height:1.4;margin-bottom:6px}}
.card-summary{{font-size:12px;color:var(--text-secondary);line-height:1.6;margin-bottom:8px}}
.card-insight{{font-size:11.5px;color:var(--neon-green);background:rgba(0,255,136,0.05);border-left:2px solid var(--neon-green);padding:6px 10px;border-radius:0 6px 6px 0;line-height:1.5;margin-bottom:8px}}
.card-insight::before{{content:'📌 '}}
.card-meta{{display:flex;align-items:center;gap:10px;flex-wrap:wrap}}
.card-source{{display:flex;align-items:center;gap:4px;font-size:10px;color:var(--text-muted)}}
.card-source a{{color:var(--neon-blue);text-decoration:none;opacity:0.8}}
.card-source a:hover{{opacity:1}}
.card-time{{font-size:10px;color:var(--text-muted)}}
.share-section{{margin-top:28px;background:linear-gradient(135deg,rgba(123,47,255,0.1),rgba(0,212,255,0.08));border:1px solid rgba(123,47,255,0.25);border-radius:16px;padding:20px;text-align:center}}
.share-title{{font-family:'Orbitron',sans-serif;font-size:13px;color:var(--text-secondary);letter-spacing:1px;margin-bottom:14px}}
.share-buttons{{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}}
.share-btn{{display:flex;align-items:center;gap:6px;padding:10px 18px;border-radius:25px;font-size:13px;font-weight:600;cursor:pointer;border:none;transition:all 0.3s ease}}
.share-btn-wechat{{background:#07C160;color:white}}
.share-btn-wechat:hover{{background:#06ad56;transform:scale(1.05);box-shadow:0 4px 20px rgba(7,193,96,0.4)}}
.share-btn-copy{{background:rgba(0,212,255,0.1);color:var(--neon-blue);border:1px solid rgba(0,212,255,0.3)}}
.share-btn-copy:hover{{background:rgba(0,212,255,0.2);transform:scale(1.05)}}
.footer{{margin-top:30px;text-align:center;padding:20px 0;border-top:1px solid rgba(0,212,255,0.08)}}
.footer-logo{{font-family:'Orbitron',sans-serif;font-size:14px;color:var(--text-muted);letter-spacing:2px;margin-bottom:4px}}
.footer-sub{{font-size:11px;color:var(--text-muted);opacity:0.6}}
.toast{{position:fixed;bottom:30px;left:50%;transform:translateX(-50%) translateY(80px);background:var(--neon-green);color:#000;font-weight:600;font-size:13px;padding:10px 20px;border-radius:25px;z-index:2000;transition:transform 0.3s ease;white-space:nowrap}}
.toast.show{{transform:translateX(-50%) translateY(0)}}
.scan-line{{position:fixed;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--neon-blue),transparent);animation:scan 4s linear infinite;opacity:0.3;z-index:999;pointer-events:none}}
@keyframes scan{{0%{{top:0}}100%{{top:100vh}}}}
.cat-1{{--accent-color:#76b900;--accent-bg:rgba(118,185,0,0.08);--accent-glow:rgba(118,185,0,0.15)}}
.cat-2{{--accent-color:#a0a0a0;--accent-bg:rgba(160,160,160,0.08);--accent-glow:rgba(160,160,160,0.1)}}
.cat-3{{--accent-color:#4285f4;--accent-bg:rgba(66,133,244,0.08);--accent-glow:rgba(66,133,244,0.1)}}
.cat-4{{--accent-color:#ff6b35;--accent-bg:rgba(255,107,53,0.08);--accent-glow:rgba(255,107,53,0.1)}}
.cat-5{{--accent-color:#00d4ff;--accent-bg:rgba(0,212,255,0.08);--accent-glow:rgba(0,212,255,0.1)}}
.cat-6{{--accent-color:#00ff88;--accent-bg:rgba(0,255,136,0.06);--accent-glow:rgba(0,255,136,0.1)}}
.cat-7{{--accent-color:#7b2fff;--accent-bg:rgba(123,47,255,0.08);--accent-glow:rgba(123,47,255,0.1)}}
.cat-8{{--accent-color:#ff2d78;--accent-bg:rgba(255,45,120,0.08);--accent-glow:rgba(255,45,120,0.1)}}
@media(max-width:480px){{.card-visual{{width:70px}}.card-icon{{font-size:22px}}.card-title{{font-size:13px}}}}
</style>
</head>
<body>
<div class="scan-line"></div>
<div class="toast" id="toast">✅ 链接已复制！</div>
<div class="container">
<div class="header">
  <div class="header-badge">元宇纪研发部 · 情报中心</div>
  <h1>每日科技早报</h1>
  <p class="header-sub">由 <span>AI 研发总监</span> 实时搜索 · 自动生成</p>
  <div class="date-line"><span class="date-text">{DATE} · {WEEKDAY}</span></div>
</div>
<div class="stats-bar">
  <div class="stat-item"><span class="stat-value">10</span><span class="stat-label">今日条目</span></div>
  <div class="stat-item"><span class="stat-value">{SOURCE_COUNT}</span><span class="stat-label">信息来源</span></div>
  <div class="stat-item"><span class="stat-value">实时</span><span class="stat-label">数据更新</span></div>
</div>
<div class="news-grid">
{NEWS_CARDS}
</div>
<div class="share-section">
  <div class="share-title">— 分享给团队 —</div>
  <div class="share-buttons">
    <button class="share-btn share-btn-wechat" onclick="shareWechat()">💬 微信分享</button>
    <button class="share-btn share-btn-copy" onclick="copyLink()">🔗 复制链接</button>
  </div>
</div>
<div class="footer">
  <div class="footer-logo">METAVERSE ERA · 元宇纪</div>
  <div class="footer-sub">研发部 AI 自动生成 · 每日 09:30 更新 · 数据来自 Brave Search 实时检索</div>
</div>
</div>
<script>
function shareWechat(){{alert('在微信内打开此页面，点击右上角「···」即可分享到朋友圈或好友')}}
function copyLink(){{
  const url='https://guangbusinessshareholder-collab.github.io/metaverse-era-daily/';
  if(navigator.clipboard){{navigator.clipboard.writeText(url).then(showToast)}}
  else{{const el=document.createElement('textarea');el.value=url;document.body.appendChild(el);el.select();document.execCommand('copy');document.body.removeChild(el);showToast()}}
}}
function showToast(){{const t=document.getElementById('toast');t.classList.add('show');setTimeout(()=>t.classList.remove('show'),3000)}}
</script>
</body>
</html>'''

CAT_ICONS = ['🖥️','📱','💰','🧠','🛒','⚙️','🚀','🎯','🤖','📊']
CATS = ['cat-1','cat-2','cat-3','cat-4','cat-5','cat-6','cat-7','cat-8','cat-1','cat-5']
WEEKDAYS = ['周一','周二','周三','周四','周五','周六','周日']

def generate_html(date_str, news_list):
    import zoneinfo
    today = datetime.now(zoneinfo.ZoneInfo('Asia/Shanghai'))
    weekday = WEEKDAYS[today.weekday()]
    cards_html = ''
    sources = set()
    for i, item in enumerate(news_list[:10]):
        cat = CATS[i % len(CATS)]
        icon = CAT_ICONS[i % len(CAT_ICONS)]
        num = f"{i+1:02d}"
        tag = item.get('tag','科技')
        title = item.get('title','')
        summary = item.get('summary','')
        insight = item.get('insight','')
        source_name = item.get('source_name','')
        source_url = item.get('source_url','#')
        pub_time = item.get('time','')
        if source_name:
            sources.add(source_name)
        cards_html += f'''
    <div class="news-card {cat}">
      <div class="card-inner">
        <div class="card-visual">
          <span class="card-number">NO.{num}</span>
          <span class="card-icon">{icon}</span>
        </div>
        <div class="card-content">
          <span class="card-tag">{tag}</span>
          <div class="card-title">{title}</div>
          <div class="card-summary">{summary}</div>
          <div class="card-insight">{insight}</div>
          <div class="card-meta">
            <span class="card-source">📰 <a href="{source_url}" target="_blank">{source_name}</a></span>
            <span class="card-time">🕐 {pub_time}</span>
          </div>
        </div>
      </div>
    </div>'''
    og_desc = '、'.join([n.get('title','')[:15] for n in news_list[:3]]) + '...今日10条科技前沿'
    html = TEMPLATE.format(
        DATE=date_str,
        WEEKDAY=weekday,
        SOURCE_COUNT=len(sources),
        NEWS_CARDS=cards_html,
        OG_DESC=og_desc
    )
    return html

def push_to_github(html, date_str):
    path = '/Users/zian/.openclaw/workspace-rd/daily-news/index.html'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    repo = '/Users/zian/.openclaw/workspace-rd/daily-news'
    subprocess.run(['git', 'add', 'index.html'], cwd=repo, check=True)
    subprocess.run(['git', 'commit', '-m', f'每日早报更新 {date_str}'], cwd=repo, check=True)
    result = subprocess.run(['git', 'push'], cwd=repo, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Push error: {result.stderr}")
        return False
    print(f"✅ 已推送: {date_str}")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 update_news.py '<json>'")
        sys.exit(1)
    data = json.loads(sys.argv[1])
    date_str = data.get('date', datetime.now().strftime('%Y.%m.%d'))
    news_list = data.get('news', [])
    html = generate_html(date_str, news_list)
    push_to_github(html, date_str)
