# generator.py
import os
import yaml
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

class FilmGenerator:
    """YAML設計図を読み込み、映像と音声を自動で錬成・合体させる零点モジュール"""
    def __init__(self, film_yaml_path="docs/Film.2026.10.20.01.yaml"):
        self.film_yaml_path = film_yaml_path
        self.output_dir = "videos"

    def _load_film(self):
        """映像設計図（YAML）を読み込む"""
        if not os.path.exists(self.film_yaml_path):
            alt_path = f"../{self.film_yaml_path}"
            if os.path.exists(alt_path):
                self.film_yaml_path = alt_path
        
        with open(self.film_yaml_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def generate_video(self, output_filename="scene.2026.10.21.mp4"):
        """各シーンの画像と音声を結びつけ、1本の動画として書き出す"""
        film_data = self._load_film()
        os.makedirs(self.output_dir, exist_ok=True)
        
        scenes = film_data.get('scenes', [])
        clip_list = []

        print("--- [FilmGenerator] 映像の自動錬成を開始します ---")

        for scene in scenes:
            scene_num = scene.get('scene_number')
            # 設計図内の画像パス、または生成された音声パスを設定
            # ※お持ちの画像ファイルの配置に合わせてパスを調整してください
            audio_path = os.path.join("audios", f"scene_{scene_num:02d}.mp3")
            
            # 例として、各シーンの画像が images/ などのフォルダにある前提、
            # または一時的に静止画クリップを構築する場合の処理
            # （画像ファイルが手元にあるパスを指定します）
            image_path = scene.get('image_path', f"images/scene_{scene_num:02d}.png") # 必要に応じて変更

            if not os.path.exists(audio_path):
                print(вольf"  > 警告: 音声ファイルが見つかりません: {audio_path}")
                continue

            print(f"  > シーン {scene_num} の素材を結合中...")

            # 音声ファイルを読み込み、その長さに合わせて画像クリップの表示時間を決定
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration

            # 画像クリップを作成し、音声をセット（もし画像がまだない場合はダミー背景等も検討できます）
            # ※ここでは仮に画像が存在する想定で進めます
            if os.path.exists(image_path):
                image_clip = ImageClip(image_path).set_duration(duration)
                video_clip = image_clip.set_audio(audio_clip)
                clip_list.append(video_clip)
            else:
                print(f"  > 注意: 画像ファイルが見つからないため音声の長さ分のプレースホルダー等が必要かもしれません: {image_path}")
                # 画像がない場合の処理（必要に応じて黒背景などを生成することも可能です）

        if clip_list:
            # すべてのシーンのクリップを一本に結合
            final_video = concatenate_videoclips(clip_list, method="compose")
            
            output_path = os.path.join(self.output_dir, output_filename)
            print(f"  > 動画ファイルをレンダリング中... ➔ {output_path}")
            
            # MP4として書き出し（fps=24 など）
            final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
            print("--- [FilmGenerator] 動画の自動錬成が完了しました！ ---")
        else:
            print("  > エラー: 結合できるクリップがありませんでした。")

if __name__ == "__main__":
    generator = FilmGenerator()
    generator.generate_video()
