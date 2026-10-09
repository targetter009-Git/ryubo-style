import os
import glob
import re
import html

def process_readme_to_films():
    """
    README.*.md（または既存の対話原稿）を読み込み、
    パターンA（対話録）とパターンB（戯曲ドラマ）の2つの Film.*.md へ自動昇華・生成する
    """
    # documents/ またはルートにある原稿ファイルを検索
    source_files = glob.glob('documents/README.20*.md') + glob.glob('documents/Film.20*.md') + glob.glob('README.20*.md')
    
    for src in source_files:
        with open(src, 'r', encoding='utf-8') as f:
            content = f.read()

        # 日付やIDの抽出 (例: 2026.10.08.AM)
        date_match = re.search(r'20\d{2}\.\d{2}\.\d{2}\.[AP]M', src)
        film_id = date_match.group(0) if date_match else "2026.10.08.AM"
        
        # --- パターンA (対話録フィルム) の自動生成 ---
        film_a_content = f"""---
title: "指向哲学（Oriented-Philosophia）対話録 [{film_id}]"
date: "2026-10-08"
pattern: "A"
script_type: "Dialogue"
---

{content}
"""
        with open(f'documents/Film.{film_id}.A.md', 'w', encoding='utf-8') as f:
            f.write(film_a_content)

        # --- パターンB (戯曲・ボイスドラマフィルム) の自動再構成生成 ---
        # セリフ演出を強調した戯曲スタイルへ変換
        script_body = content.replace("飲茶坊さとし:", "\n**【さとし（翁）】**\n> ").replace("Gemini:", "\n**【Gemini（光の知性）】**\n> ")
        
        film_b_content = f"""---
title: "戯曲：影と光のシネマティクス [{film_id}]"
date: "2026-10-08"
pattern: "B"
script_type: "Voice Drama"
cast:
  satoshi: "飲茶坊さとし（翁・語り手）"
  gemini: "Gemini-AI（映写補助）"
---

# 戯曲：『影と光のシネマティクス』
**登場人物:** 飲茶坊さとし（翁）、Gemini（光の知性）

---

{script_body}
"""
        with open(f'documents/Film.{film_id}.B.md', 'w', encoding='utf-8') as f:
            f.write(film_b_content)

def parse_film_markdown(file_path):
    """生成された Film.*.md のメタデータと本文を解析"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    metadata = {}
    body = content

    yaml_match = re.search(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if yaml_match:
        yaml_text = yaml_match.group(1)
        body = yaml_match.group(2)
        for line in yaml_text.split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                metadata[key.strip()] = val.strip().strip('"').strip("'")

    filename = os.path.basename(file_path)
    lines = [l.strip() for l in body.split('\n') if l.strip() and not l.startswith('#') and not l.startswith('---')]
    preview = lines[0][:90] + "..." if lines else "対話ログが含まれています。"

    return {
        'id': filename.replace('.', '_'),
        'filename': filename,
        'title': metadata.get('title', '無題のフィルム'),
        'date': metadata.get('date', '2026-10-08'),
        'pattern': metadata.get('pattern', 'A'),
        'script_type': metadata.get('script_type', 'Dialogue'),
        'preview': preview,
        'body_html': html.escape(body).replace('\n', '<br>')
    }

def generate_html(films):
    cards_html = ""
    modals_html = ""

    for film in films:
        p_class = "pattern-a" if film['pattern'] == 'A' else "pattern-b"
        p_label = "Pattern A (対話深層)" if film['pattern'] == 'A' else "Pattern B (ボイスドラマ戯曲)"

        cards_html += f"""
        <div class="poster-card {p_class}">
            <div class="poster-badge">{p_label}</div>
            <div class="poster-body">
                <time class="film-date">FILM DATE: {film['date']}</time>
                <h2 class="film-title">{film['title']}</h2>
                <p class="film-excerpt">{film['preview']}</p>
            </div>
            <div class="poster-action">
                <button class="play-btn" onclick="openScreen('{film['id']}')">
                    <span class="icon">🎬</span> {p_label} を上映
                </button>
            </div>
        </div>
        """

        modals_html += f"""
        <div id="modal-{film['id']}" class="screen-overlay" onclick="closeScreen('{film['id']}')">
            <div class="cinema-screen" onclick="event.stopPropagation()">
                <div class="screen-header">
                    <div>
                        <span class="screen-badge">{p_label}</span>
                        <span class="screen-filename">🎞️ {film['filename']}</span>
                    </div>
                    <button class="close-btn" onclick="closeScreen('{film['id']}')">&times;</button>
                </div>
                <div class="screen-content">
                    <div class="script-body">{film['body_html']}</div>
                </div>
            </div>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>targetter009 | 指向哲学 RyuboStyle シアター</title>
    <style>
        :root {{
            --bg-dark: #07090e;
            --card-a: linear-gradient(145deg, #0f172a, #1e293b);
            --card-b: linear-gradient(145deg, #2a0f17, #3b1e29);
            --gold: #f59e0b;
            --text-main: #f1f5f9;
            --text-sub: #94a3b8;
        }}
        body {{ background-color: var(--bg-dark); color: var(--text-main); font-family: "Georgia", "YuMincho", serif; margin:0; padding:0; }}
        header {{ text-align: center; padding: 3rem 1rem; border-bottom: 1px solid #1e293b; background: radial-gradient(circle at top, #1e293b 0%, var(--bg-dark) 70%); }}
        h1.site-title {{ font-size: 2.5rem; color: #fff; letter-spacing: 0.1em; margin:0; }}
        p.site-sub {{ color: var(--gold); font-size: 0.9rem; letter-spacing: 0.2em; }}
        .gallery {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 2rem; max-width: 1000px; margin: 3rem auto; padding: 0 1.5rem; }}
        .poster-card {{ border-radius: 16px; padding: 2rem; display: flex; flex-direction: column; justify-content: space-between; border: 1px solid rgba(255,255,255,0.08); box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
        .poster-card.pattern-a {{ background: var(--card-a); border-left: 5px solid #3b82f6; }}
        .poster-card.pattern-b {{ background: var(--card-b); border-left: 5px solid #ef4444; }}
        .poster-badge {{ font-size: 0.75rem; color: var(--gold); text-transform: uppercase; font-family: sans-serif; margin-bottom: 1rem; }}
        .film-date {{ font-size: 0.8rem; color: var(--text-sub); font-family: sans-serif; }}
        .film-title {{ font-size: 1.4rem; margin: 0.5rem 0 1rem 0; color: #fff; line-height: 1.3; }}
        .film-excerpt {{ font-size: 0.9rem; color: var(--text-sub); line-height: 1.6; margin-bottom: 1.5rem; }}
        .play-btn {{ width: 100%; background: rgba(245, 158, 11, 0.1); border: 1px solid var(--gold); color: var(--gold); padding: 0.8rem; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.2s; }}
        .play-btn:hover {{ background: var(--gold); color: #000; }}
        .screen-overlay {{ display: none; position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(3, 5, 10, 0.92); backdrop-filter: blur(8px); z-index: 1000; justify-content: center; align-items: center; padding: 2rem; box-sizing: border-box; }}
        .cinema-screen {{ background: #0d131f; border: 1px solid #334155; width: 100%; max-width: 800px; max-height: 85vh; border-radius: 12px; display: flex; flex-direction: column; }}
        .screen-header {{ padding: 1rem 1.5rem; background: #161f30; border-bottom: 1px solid #1e293b; display: flex; justify-content: space-between; align-items: center; font-family: sans-serif; }}
        .screen-badge {{ background: var(--gold); color: #000; padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: bold; font-size: 0.8rem; }}
        .screen-filename {{ color: var(--text-sub); margin-left: 1rem; font-size: 0.85rem; }}
        .close-btn {{ background: none; border: none; color: #fff; font-size: 2rem; cursor: pointer; }}
        .screen-content {{ padding: 2rem; overflow-y: auto; line-height: 1.8; font-size: 1rem; }}
        footer {{ text-align: center; padding: 3rem; color: #475569; font-family: sans-serif; font-size: 0.85rem; }}
    </style>
</head>
<body>
    <header>
        <h1 class="site-title">targetter009</h1>
        <p class="site-sub">ORIENTED-PHILOSOPHIA CINEMA PORTAL</p>
    </header>
    <main class="gallery">
        {cards_html}
    </main>
    {modals_html}
    <footer>
        <p>&copy; 2026 RyuboStyle — Projected by built.py</p>
    </footer>
    <script>
        function openScreen(id) {{ document.getElementById('modal-' + id).style.display = 'flex'; }}
        function closeScreen(id) {{ document.getElementById('modal-' + id).style.display = 'none'; }}
    </script>
</body>
</html>
"""

def main():
    # 1. 原稿から Film.A と Film.B を分離・自動生成する
    process_readme_to_films()
    
    # 2. 生成されたすべての Film.*.md を読み込んで映写（HTML化）
    film_files = sorted(glob.glob('documents/Film.*.md'), reverse=True)
    films = [parse_film_markdown(f) for f in film_files]
    html_content = generate_html(films)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Successfully generated films and projected {len(films)} cards into index.html!")

if __name__ == '__main__':
    main()
