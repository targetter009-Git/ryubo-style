import os
import sys
import glob
import re
import urllib.parse
import requests
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, concat_videoclips

def run_step(step_name, func):
    print(f"\n=== [START] {step_name} ===")
    try:
        func()
        print(f"=== [SUCCESS] {step_name} ===")
        return True
    except Exception as e:
        print(f"=== [ERROR] Failed in {step_name}: {e} ===")
        import traceback
        traceback.print_exc()
        return False

# 1. 画像生成プロセス
def step_images():
    os.makedirs('assets/images', exist_ok=True)
    scenes = ['scene1', 'scene2', 'scene3', 'scene4']
    cuts = ['01', '02', '03']
    base_prompt = "cinematic film still, 16:9 aspect ratio, dark philosophical atmosphere, glowing lights, Japanese aesthetics, high quality, 8k"
    
    for s in scenes:
        for c in cuts:
            img_name = f"{s}_{c}_16_9.png"
            img_path = os.path.join('assets/images', img_name)
            prompt = f"{base_prompt}, scene {s} cut {c}, mysterious shadow and light"
            encoded_prompt = urllib.parse.quote(prompt)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true"
            
            print(f"Downloading image: {img_name}...")
            res = requests.get(image_url, timeout=30)
            if res.status_code == 200:
                with open(img_path, 'wb') as f:
                    f.write(res.content)

# 2. 音声合成プロセス
def step_speech():
    os.makedirs('assets/audios', exist_ok=True)
    film_files = glob.glob('documents/Film.*.md')
    
    for film_path in film_files:
        filename = os.path.basename(film_path)
        film_id = filename.replace('Film.', '').replace('.md', '')
        output_audio = f"assets/audios/Film.{film_id}.mp3"
        
        with open(film_path, 'r', encoding='utf-8') as f:
            content = f.read()
        lines = content.split('\n')
        speech_lines = []
        for line in lines:
            if line.startswith('---') or line.startswith('#') or ('complex' in line and not '「' in line):
                continue
            clean_text = re.sub(r'[\*\_`#]', '', line).strip()
            if clean_text:
                speech_lines.append(clean_text)
        text = " ".join(speech_lines) if speech_lines else "指向哲学の映像表現へようこそ。"
        
        print(f"Generating audio for {film_id}...")
        tts = gTTS(text=text, lang='ja')
        tts.save(output_audio)

# 3. 動画結合プロセス
def step_movies():
    os.makedirs('assets/videos', exist_ok=True)
    film_files = glob.glob('documents/Film.*.md')
    images = sorted(glob.glob('assets/images/*_16_9.png'))
    
    for film_path in film_files:
        filename = os.path.basename(film_path)
        film_id = filename.replace('Film.', '').replace('.md', '')
        output_video = f"assets/videos/Film.{film_id}.mp4"
        audio_path = f"assets/audios/Film.{film_id}.mp3"
        
        if not os.path.exists(audio_path) or not images:
            raise FileNotFoundError(f"Required assets missing for {film_id}")
            
        print(f"Building movie for {film_id} (15 sec per scene)...")
        clips = [ImageClip(img_p).set_duration(15) for img_p in images]
        video = concat_videoclips(clips, method="compose")
        audio = AudioFileClip(audio_path)
        video = video.set_audio(audio)
        
        video.write_videofile(output_video, fps=24, codec='libx264', audio_codec='aac')

def main():
    print("🎬 完全統合型マネージャー (manager.py) を起動します...")
    
    if not run_step("Image Generation", step_images):
        sys.exit(1)
    if not run_step("Speech Generation", step_speech):
        sys.exit(1)
    if not run_step("Movie Generation", step_movies):
        sys.exit(1)
        
    print("\n🎉 すべてのマルチメディア生成プロセスが正常に完了しました！")

if __name__ == '__main__':
    main()
