import os
import glob
from moviepy.editor import ImageClip, AudioFileClip, concat_videoclips

def generate_movies():
    os.makedirs('assets/videos', exist_ok=True)
    film_files = glob.glob('documents/Film.*.md')
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
        for img_p in images:
            clip = ImageClip(img_p).set_duration(15)
            clips.append(clip)
            
        video = concat_videoclips(clips, method="compose")
        audio = AudioFileClip(audio_path)
        video = video.set_audio(audio)
        
        video.write_videofile(
            output_video,
            fps=24,
            codec='libx264',
            audio_codec='aac'
        )
        print(f"Movie saved: {output_video}")

if __name__ == '__main__':
    generate_movies()
