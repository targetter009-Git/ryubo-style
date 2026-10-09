import os
import glob
from moviepy.editor import ImageClip, AudioFileClip, concat_videoclips

def generate_movies():
    os.makedirs('assets/videos', exist_ok=True)
    film_files = glob.glob('documents/Film.*.md')
    
    # 12コマ画像アセットの収集
    images = sorted(glob.glob('assets/images/*_16_9.png'))
    
    for film_path in film_files:
        filename = os.path.basename(film_path)
        film_id = filename.replace('Film.', '').replace('.md', '')
        output_video = f"assets/videos/Film.{film_id}.mp4"
        audio_path = f"assets/audios/Film.{film_id}.mp3"
        
        if not os.path.exists(audio_path) or not images:
            print(f"Skip {film_id}: Required assets missing.")
            continue
            
        print(f"Building movie for {film_id} (15 sec per scene)...")
        
        clips = []
        # 1カットあたり15秒の静止画クリップを作成
        for img_p in images:
            clip = ImageClip(img_p).set_duration(15) # 1カット15秒
            clips.append(clip)
            
        # 全カットを連結（全12カット × 15秒 = 180秒）
        video = concat_videoclips(clips, method="compose")
        
        # 音声トラックのBGM/ボイス合成
        audio = AudioFileClip(audio_path)
        # 動画長さを調整し、音声をセット
        video = video.set_audio(audio)
        
        # mp4動画のレンダリング書き出し
        video.write_videofile(
            output_video,
            fps=24,
            codec='libx264',
            audio_codec='aac'
        )
        print(f"Movie saved: {output_video}")

if __name__ == '__main__':
    generate_movies()
