import os
import re
import glob

class FilmCut:
    def __init__(self, scene_id, cut_id, prompt, motion, dialogue):
        self.scene_id = scene_id
        self.cut_id = cut_id
        self.prompt = prompt
        self.motion = motion
        self.dialogue = dialogue

class FilmParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.cuts = []
        self.parse()

    def parse(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # シーンおよびカット単位で分割してプロンプトとセリフを抽出するパーサーロジック
        # Markdownの見出し構造（SCENE / CUT）に合わせた正規表現による解析
        scenes = re.split(r'#\s+SCENE\s+', content)
        for scene_block in scenes[1:]:
            scene_match = re.search(r'0?(\d+)', scene_block)
            if not scene_match:
                continue
            scene_id = f"scene{scene_match.group(1)}"
            
            cut_blocks = re.split(r'##\s+CUT\s+', scene_block)
            for cut_block in cut_blocks[1:]:
                cut_match = re.search(r'0?(\d+)', cut_block)
                if not cut_match:
                    continue
                cut_id = cut_match.group(1).zfill(2)
                
                # 画像生成プロンプトの抽出
                prompt_match = re.search(r'Image generation prompt \(English\).*?\n_{3,}\n(.*?)\n_{3,}', cut_block, re.DOTALL)
                prompt = prompt_match.group(1).strip() if prompt_match else ""
                
                # 動画モーション指示の抽出
                motion_match = re.search(r'Video motion direction \(English\).*?\n_{3,}\n(.*?)\n_{3,}', cut_block, re.DOTALL)
                motion = motion_match.group(1).strip() if motion_match else ""
                
                # セリフ／ナレーションの抽出
                dialogue_match = re.search(r'セリフ／ナレーション\s*\n\s*(["“「](.*?)["”」])', cut_block)
                dialogue = dialogue_match.group(2).strip() if dialogue_match else ""
                
                if prompt:
                    self.cuts.append(FilmCut(scene_id, cut_id, prompt, motion, dialogue))

class AssetPipeline:
    def __init__(self, film_parser):
        self.film_parser = film_parser

    def generate_assets(self):
        os.makedirs('assets/images', exist_ok=True)
        os.makedirs('assets/audios', exist_ok=True)
        
        for cut in self.film_parser.cuts:
            print(f"Processing -> Scene: {cut.scene_id}, Cut: {cut.cut_id}")
            # ここで Pollinations API による画像生成や gTTS による音声合成をカットごとに実行
            # 例: img_name = f"{cut.scene_id}_{cut.cut_id}_16_9.png"
