import os
import glob
import re
from gtts import gTTS

def extract_texts_from_md(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # YAMLヘッダーやマークダウン記号を除去し、テキスト抽出
    lines = content.split('\n')
    speech_lines = []
    for line in lines:
        if line.startswith('---') or line.startswith('#') or ':' in line and not '「' in line:
            continue
        clean_text = re.sub(r'[\*\_`#]', '', line).strip()
        if clean_text:
            speech_lines.append(clean_text)
    return " ".join(speech_lines) if speech_lines else "指向哲学の映像表現へようこそ。"

def generate_speech():
    os.makedirs('assets/audios', exist_ok=True)
    film_files = glob.glob('documents/Film.*.md')
    
    for film_path in film_files:
        filename = os.path.basename(film_path)
        film_id = filename.replace('Film.', '').replace('.md', '')
        output_audio = f"assets/audios/Film.{film_id}.mp3"
        
        text = extract_texts_from_md(film_path)
        print(f"Generating audio for {film_id}...")
        
        # gTTSによる音声生成
        tts = gTTS(text=text, lang='ja')
        tts.save(output_audio)
        print(f"Audio saved: {output_audio}")

if __name__ == '__main__':
    generate_speech()
