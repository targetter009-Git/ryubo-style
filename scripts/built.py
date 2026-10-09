import os
import glob
import re
import html

def parse_film_markdown(file_path):
    """Film.*.md のYAMLフロントメタデータと本文を解析する"""
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
    title = metadata.get('title', '無題のフィルム')
    date = metadata.get('date', '2026-10-08')
    pattern = metadata.get('pattern', 'A')
    script_type = metadata.get('script_type', 'Dialogue')

    lines = [l.strip() for l in body.split('\n') if l.strip() and not l.startswith('#') and not l.startswith('---')]
    preview = lines[0][:100] + "..." if lines else "対話ログが含まれています。"

    return {
        'id': filename.replace('.', '_'),
        'filename': filename,
        'title': title,
        'date': date,
        'pattern': pattern,
        'script_type': script_type,
        'preview': preview,
        'body_html': html.escape(body).replace('\n', '<br>')
    }

def generate_html(films):
    cards_html = ""
    modals_html = ""

    for film in films:
        p_class = "pattern-a" if film['pattern'] == 'A' else "pattern-b"
        p_label = "Pattern A (対話録)" if film['pattern'] == 'A' else "Pattern B (戯曲/ドラマ)"

        # 映写ポスターカード
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
                    <span class="icon">🎬</span> フィルムを再生（全編上映）
                </button>
            </div>
        </div>
        """

        # シネマスクリーン（全編閲覧用モーダル）
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
                    <h1>{film['title']}</h1>
                    <hr class="cinema-hr">
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

        body {{
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: "Georgia", "YuMincho", "Hiragino Mincho ProN", serif;
            margin: 0;
            padding: 0;
            min-height: 100vh;
        }}

        header {{
            text-align: center;
            padding: 4rem 1rem 2rem 1rem;
            background: radial-gradient(circle at top, #1e293b 0%, var(--bg-dark) 70%);
            border-bottom: 1px solid #1e293b;
        }}

        .projector-light {{
            display: inline-block;
            font-size: 2.5rem;
            filter: drop-shadow(0 0 15px var(--gold));
            margin-bottom: 0.5rem;
        }}

        h1.site-title {{
            font-size: 2.8rem;
            margin: 0;
            letter-spacing: 0.1em;
            color: #ffffff;
            text-shadow: 0 0 20px rgba(245, 158, 11, 0.3);
        }}

        p.site-sub {{
            color: var(--gold);
            font-size: 1rem;
            letter-spacing: 0.2em;
            margin-top: 0.5rem;
        }}

        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
            gap: 2rem;
            max-width: 1100px;
            margin: 3rem auto;
            padding: 0 1.5rem;
        }}

        .poster-card {{
            border-radius: 16px;
            padding: 2rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            border: 1px solid rgba(255,255,255,0.08);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}

        .poster-card.pattern-a {{ background: var(--card-a); border-left: 5px solid #3b82f6; }}
        .poster-card.pattern-b {{ background: var(--card-b); border-left: 5px solid #ef4444; }}

        .poster-card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(245, 158, 11, 0.15);
            border-color: var(--gold);
        }}

        .poster-badge {{
            font-size: 0.75rem;
            letter-spacing: 0.1em;
            color: var(--gold);
            text-transform: uppercase;
            font-family: sans-serif;
            margin-bottom: 1rem;
        }}

        .film-date {{ font-size: 0.8rem; color: var(--text-sub); font-family: sans-serif; }}
        .film-title {{ font-size: 1.5rem; margin: 0.5rem 0 1rem 0; color: #fff; line-height: 1.3; }}
        .film-excerpt {{ font-size: 0.95rem; color: var(--text-sub); line-height: 1.6; margin-bottom: 1.5rem; }}

        .play-btn {{
            width: 100%;
            background-color: rgba(245, 158, 11, 0.1);
            border: 1px solid var(--gold);
            color: var(--gold);
            padding: 0.8rem;
            border-radius: 8px;
            font-size: 0.95rem;
            cursor: pointer;
            transition: all 0.2s ease;
            font-family: sans-serif;
            font-weight: bold;
        }}

        .play-btn:hover {{
            background-color: var(--gold);
            color: #000;
            box-shadow: 0 0 15px rgba(245, 158, 11, 0.4);
        }}

        .screen-overlay {{
            display: none;
            position: fixed;
            top:0; left:0; width:100%; height:100%;
            background: rgba(3, 5, 10, 0.92);
            backdrop-filter: blur(8px);
            z-index: 1000;
            justify-content: center;
            align-items: center;
            padding: 2rem;
            box-sizing: border-box;
        }}

        .cinema-screen {{
            background: #0d131f;
            border: 1px solid #334155;
            width: 100%;
            max-width: 850px;
            max-height: 85vh;
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            box-shadow: 0 0 50px rgba(0,0,0,0.8);
        }}

        .screen-header {{
            padding: 1.2rem 1.8rem;
            background: #161f30;
            border-bottom: 1px solid #1e293b;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: sans-serif;
        }}

        .screen-badge {{ background: var(--gold); color: #000; padding: 0.2rem 0.6rem; border-radius: 4px; font-weight: bold; font-size: 0.8rem; }}
        .screen-filename {{ color: var(--text-sub); margin-left: 1rem; font-size: 0.85rem; }}
        .close-btn {{ background: none; border: none; color: #fff; font-size: 2rem; cursor: pointer; }}

        .screen-content {{
            padding: 2.5rem;
            overflow-y: auto;
            line-height: 1.8;
            font-size: 1.05rem;
        }}

        .cinema-hr {{ border: 0; height: 1px; background: #334155; margin: 1.5rem 0 2rem 0; }}

        footer {{ text-align: center; padding: 3rem; color: #475569; font-family: sans-serif; font-size: 0.85rem; }}
    </style>
</head>
<body>
    <header>
        <div class="projector-light">🎞️</div>
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
        function openScreen(id) {{
            document.getElementById('modal-' + id).style.display = 'flex';
        }}
        function closeScreen(id) {{
            document.getElementById('modal-' + id).style.display = 'none';
        }}
    </script>
</body>
</html>
"""

def main():
    film_files = sorted(glob.glob('documents/Film.*.md'), reverse=True)
    films = [parse_film_markdown(f) for f in film_files]
    html_content = generate_html(films)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Successfully projected {len(films)} film(s) into cinema portal!")

if __name__ == '__main__':
    main()
