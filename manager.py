import os
import sys
import yaml

# ==========================================
# 🎥 Ryubo Theater 舞台監督システム (Manager)
# ==========================================

def load_blueprint():
    """舞台の設計図（theater_blueprint.yaml）を読み込む"""
    blueprint_path = "theater_blueprint.yaml"
    if os.path.exists(blueprint_path):
        with open(blueprint_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}

def create_default_file(file_path):
    """各部屋のREADMEや初期ファイルを生成する"""
    base_name = os.path.basename(file_path)
    parent_dir = os.path.dirname(file_path)
    content = ""
    
    if base_name == "README.md":
        if "documents" in parent_dir:
            content = "# 📜 documents/ フィルム控室\n\n上映するフィルム（Markdown台本）を保管する空間です。\n"
        elif "assets/images" in parent_dir:
            content = "# 🖼️ assets/images/ スクリーンショット・映像素材の控室\n\nフィルムに映し出すビジュアルや画像を保管する空間です。\n"
        elif "assets/audios" in parent_dir:
            content = "# 🎵 assets/audios/ サウンド・言霊の控室\n\n音声ファイルやMP3など、空間を彩る響きを保管する空間です。\n"
        elif "assets/videos" in parent_dir:
            content = "# 🎬 assets/videos/ フィルム映像の控室\n\nレンダリングされた動画アセットを保管する空間です。\n"
        elif "assets/prompts" in parent_dir:
            content = "# 📝 assets/prompts/ プロンプトの控室\n\nAIや生成パイプラインで使用するプロンプト設計を保管する空間です。\n"
        elif "procedures" in parent_dir:
            content = "# ⚙️ procedures/ 専門工程モジュール群\n\n舞台を形作るための自動化スクリプトやプロシージャを収めています。\n"
        else:
            content = f"# {base_name}\n\nこの空間は Ryubo Theater のシステムによって管理されています。\n"
    elif base_name == "__init__.py":
        content = "# Procedure Package Init\n"
    elif base_name == "base.py":
        content = 'class BaseProcedure:\n    """各専門プロシージャのベースクラス"""\n    def run(self):\n        raise NotImplementedError\n'
    else:
        content = f"# {base_name}\n"

    if content and not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

def self_repair(blueprint_data):
    """設計図に基づき、ディレクトリ構造とアセット用控室を自動構築する"""
    print("🛠️ [Manager 自律修復] 舞台セットとアセット用控室を点検・構築します...")
    
    for item in blueprint_data.get("required_tree", []):
        path = item["path"]
        
        if item["type"] == "directory":
            os.makedirs(path, exist_ok=True)
            
            # ディレクトリ直下のファイル生成
            for file_name in item.get("files", []):
                file_path = os.path.join(path, file_name)
                create_default_file(file_path)
                    
            # サブディレクトリ（assets内の各部屋など）の生成
            for sub in item.get("sub_dirs", []):
                sub_path = sub["path"]
                os.makedirs(sub_path, exist_ok=True)
                if sub.get("readme", False):
                    create_default_file(os.path.join(sub_path, "README.md"))
                    
        elif item["type"] == "file" and path == "index.html":
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    f.write("<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Ryubo Theater</title></head><body><h1>Ryubo Theater</h1></body></html>")

def main():
    print("🎭 Ryubo Theater Manager 起動...")
    blueprint = load_blueprint()
    if blueprint:
        self_repair(blueprint)
        print("🎬 舞台と控室の点検・修復が完了しました。")
    else:
        print("⚠️ 警告: theater_blueprint.yaml が見つかりません。")

if __name__ == "__main__":
    main()
