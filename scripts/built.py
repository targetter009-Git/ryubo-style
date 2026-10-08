import os
import glob
import re

def parse_film_markdown(file_path):
    """Film.*.md のYAMLフロントメタデータと本文を解析する"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    metadata = {}
    body = content

    # --- で囲まれたYAMLフロントメタデータを抽出
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
    date = metadata.get('date', 'Unknown Date')
    pattern = metadata.get('pattern', 'A')
    script_type = metadata.get('script_type', 'Dialogue')

    # タイトルや主要部分をカード用プレビューとして整形
    lines = [l.strip() for l in body.split('\n') if l.strip() and not l.startswith('#') and not l.startswith('---')]
    preview = lines[0][:120] + "..." if lines else "対話ログが含まれています。"

    return {
        'filename': filename,
        'title': title,
        'date': date,
        'pattern': pattern,
        'script_type': script_type,
        'preview': preview,
        'body': body
    }

def generate_html(films):
    """Film情報からシネマティックな index.html を生成する"""
    
    cards_html = ""
    for film in films:
        # パターンA（濃紺）/ パターンB（深朱）のデザイン分岐演出
        pattern_class = "pattern-a" if film['pattern'] == 'A' else "pattern-b"
        badge_label = f"Pattern {film['pattern']} / {film['script_type']}"

        cards_html += f"""
        <article class="film-card {pattern_class}">
            <div class="card-header">
                <span class="badge">{badge_label}</span>
                <time class="date">{film['date']}</time>
            </div>
            <h2 class="film-title">{film['title']}</h2>
            <p class="film-preview">{film['preview']}</p>
            <div class="card-footer">
                <span class="file-tag">🎞️ {film['filename']}</span>
            </div>
        </article>
        """

    html_template = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>targetter009 | 指向哲学 (Oriented-Philosophia)</title>
    <style>
        :root {{
            --bg-color: #0b0f19;
            --text-color: #e2e8f0;
            --accent-gold: #d97706;
            --card-bg: #1e293b;
            --border-color: #334155;
        }}
        
        body {{
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            margin: 0;
            padding: 2rem 1rem;
            line-height: 1.6;
        }}

        header {{
            text-align: center;
            max-width: 800px;
            margin: 0 auto 3rem auto;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 2rem;
        }}

        h1 {{
            font-size: 2.2rem;
            letter-spacing: 0.05em;
            color: #f8fafc;
            margin-bottom: 0.5rem;
        }}

        p.subtitle {{
            color: #94a3b8;
            font-style: italic;
            font-size: 1rem;
        }}

        .film-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 1.5rem;
            max-width: 1100px;
            margin: 0 auto;
        }}

        .film-card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            transition: transform 0.2s ease, border-color 0.2s ease;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        }}

        .film-card:hover {{
            transform: translateY(-4px);
            border-color: var(--accent-gold);
        }}

        .film-card.pattern-a {{
            border-left: 4px solid #3b82f6; /* 青のアクセント */
        }}

        .film-card.pattern-b {{
            border-left: 4px solid #ef4444; /* 赤のアクセント */
        }}

        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            font-size: 0.85rem;
        }}

        .badge {{
            background-color: #0f172a;
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            color: #cbd5e1;
            font-weight: 600;
        }}

        .date {{
            color: #64748b;
        }}

        .film-title {{
            font-size: 1.25rem;
            margin: 0 0 0.8rem 0;
            color: #f1f5f9;
        }}

        .film-preview {{
            color: #94a3b8;
            font-size: 0.95rem;
            margin-bottom: 1.2rem;
        }}

        .card-footer {{
            font-size: 0.8rem;
            color: #64748b;
            border-top: 1px dashed var(--border-color);
            padding-top: 0.8rem;
        }}

        footer {{
            text-align: center;
            margin-top: 4rem;
            color: #475569;
            font-size: 0.85rem;
        }}
    </style>
</head>
<body>
    <header>
        <h1>targetter009</h1>
        <p class="subtitle">指向哲学（Oriented-Philosophia）/ RyuboStyle 映写ポータル</p>
    </header>

    <main class="film-grid">
        {cards_html}
    </main>

    <footer>
        <p>&copy; 2026 RyuboStyle — Projected by built.py</p>
    </footer>
</body>
</html>
"""
    return html_template

def main():
    # documents/ 内の Film.*.md を検索して処理
    film_files = sorted(glob.glob('documents/Film.*.md'), reverse=True)
    
    films = []
    for f_path in film_files:
        films.append(parse_film_markdown(f_path))

    # html出力生成
    html_content = generate_html(films)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"Successfully projected {len(films)} film(s) into index.html!")

if __name__ == '__main__':
    main()
