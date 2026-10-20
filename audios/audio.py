# audios/audio.py
import os
import yaml
import asyncio
import edge_tts

class AudioFactory:
    """edge-tts を用いて女性音声のアセットを錬成する零点モジュール"""
    def __init__(self, film_yaml_path="docs/Film.2026.10.20.01.yaml"):
        self.film_yaml_path = film_yaml_path
        self.output_dir = "audios"
        # 高品質な日本語女性Neuralボイス（例: NanamiNeural）
        self.voice = "ja-JP-NanamiNeural"

    def _load_film(self):
        """映像設計図（YAML）を読み込む"""
        if not os.path.exists(self.film_yaml_path):
            alt_path = f"../{self.film_yaml_path}"
            if os.path.exists(alt_path):
                self.film_yaml_path = alt_path
        
        with open(self.film_yaml_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    async def _generate_single_audio(self, text, output_path):
        """edge-tts を使って非同期で音声を生成する"""
        # 必要に応じてピッチ(+0Hzなど)やレート(+0%など)を微調整できます
        communicate = edge_tts.Communicate(text, self.voice, rate="+0%", pitch="+0Hz")
        await communicate.save(output_path)

    def generate_audios(self, callback=None):
        """YAMLからナレーションを抽出し、シーンごとのMP3音声を錬成する"""
        film_data = self._load_film()
        os.makedirs(self.output_dir, exist_ok=True)
        
        scenes = film_data.get('scenes', [])
        for scene in scenes:
            scene_num = scene.get('scene_number')
            narration = scene.get('narration')
            
            if not narration:
                continue

            output_filename = f"scene_{scene_num:02d}.mp3"
            output_path = os.path.join(self.output_dir, output_filename)
            
            print(f"[AudioFactory/edge-tts] 錬成中: Scene {scene_num} -> 「{narration}」")
            
            # 非同期の音声生成を実行
            asyncio.run(self._generate_single_audio(narration, output_path))
            
            if callback:
                callback(scene_num, output_path)

        if callback:
            callback("COMPLETE", self.output_dir)

if __name__ == "__main__":
    print("--- 音声ファクトリー（edge-tts版・零点）起動 ---")
    factory = AudioFactory()
    factory.generate_audios(callback=lambda s, m: print(f"  > [通知] status: {s}, path: {m}"))
    print("--- 音声の錬成が完了しました ---")