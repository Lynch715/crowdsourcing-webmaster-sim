#!/usr/bin/env python3
"""压缩 assets 并内联为 base64,输出 dist/index.html 单文件发布版。"""
import base64, io, os, re, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "index.html")
OUT_DIR = os.path.join(ROOT, "dist")
OUT = os.path.join(OUT_DIR, "index.html")

# 各类资源的最大宽度与webp质量
RULES = [
    ("assets/char/",  (512, 768),  74),
    ("assets/bg/",    (1280, 720), 70),
    ("assets/event/", (960, 540),  72),
    ("assets/ui/icon_",(96, 96),   80),
    ("assets/ui/logo_",(900, 340), 76),
    ("assets/ui/",    (512, 160),  80),
]

def rule_for(path):
    for prefix, size, q in RULES:
        if path.startswith(prefix):
            return size, q
    return (1024, 1024), 72

def to_data_uri(rel):
    fp = os.path.join(ROOT, rel)
    if not os.path.exists(fp):
        print(f"  ⚠️ 缺失: {rel}(保留原路径)")
        return None
    (mw, mh), q = rule_for(rel)
    im = Image.open(fp)
    im.thumbnail((mw, mh), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=q, method=6)
    data = buf.getvalue()
    print(f"  {rel}: {os.path.getsize(fp)//1024}KB → {len(data)//1024}KB webp")
    return "data:image/webp;base64," + base64.b64encode(data).decode()

def main():
    html = open(SRC, encoding="utf-8").read()
    paths = sorted(set(re.findall(r'assets/[A-Za-z0-9_/.-]+?\.(?:png|jpg)', html)))
    print(f"发现 {len(paths)} 个静态引用")
    total = 0
    for p in paths:
        uri = to_data_uri(p)
        if uri:
            html = html.replace(p, uri)
            total += len(uri)
    # JS里动态拼接的路径: boss立绘 assets/char/char_boss_{state}.png、事件ART map "assets/"+key+".png"
    dyn = {}
    for st in ["smug", "anxious", "ruined"]:
        u = to_data_uri(f"assets/char/char_boss_{st}.png")
        if u: dyn[f"char_boss_{st}"] = u; total += len(u)
    # ART/EART 值(如 "event/ev_money")→ 运行时拼 "assets/"+v+".png"
    for v in sorted(set(re.findall(r'"((?:event|bg|char)/[a-z0-9_]+)"', html))):
        u = to_data_uri(f"assets/{v}.png")
        if u: dyn[v] = u; total += len(u)
    inject = "const ASSETS=" + repr(dyn).replace("'", '"') + ";\n" \
             "function asset(p){const k=p.replace(/^assets\\//,'').replace(/\\.png$/,'');" \
             "return ASSETS[k]||ASSETS[k.replace('char/','')]||p;}\n"
    # 替换动态引用点
    html = html.replace('"use strict";', '"use strict";\n' + inject)
    html = html.replace('img.src="assets/char/char_boss_"+st+".png";',
                        'img.src=asset("char_boss_"+st);')
    html = html.replace('const artFile=ART[key]?("assets/"+ART[key]+".png"):null;',
                        'const artFile=ART[key]?asset(ART[key]):null;')
    html = html.replace('im.src="assets/"+EART[key]+".png";',
                        'im.src=asset(EART[key]);')
    html = html.replace('fig.src="assets/"+CHART[key]+".png";',
                        'fig.src=asset(CHART[key]);')
    html = html.replace('if(artFile.includes("/char/"))im.className="por";',
                        'if(ART[key]&&ART[key].includes("char/"))im.className="por";')
    os.makedirs(OUT_DIR, exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(html)
    print(f"\n✅ dist/index.html 生成: {os.path.getsize(OUT)/1048576:.1f} MB")
    leftover = re.findall(r'src="assets/', html) + re.findall(r'url\("assets/', html)
    if leftover: print(f"  ⚠️ 仍有 {len(leftover)} 处外部引用未内联")

if __name__ == "__main__":
    main()
