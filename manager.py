import os
import sys
import yaml

# ==========================================
# 🎥 Ryubo Theater 舞台監督システム (Manager - Simple)
# ==========================================

def load_blueprint():
    """舞台の設計図（theater_blueprint.yaml）を読み込む"""
    blueprint_path = "theater_blueprint.yaml"
    if os.path.exists(blueprint_path):
        with open(blueprint_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}

def create_default_file(file_path):
    """ファイルの初期コンテンツを生成する"""
    base_name = os.path.basename(file_path)
    
    if base_name == "README.md":
        content = f"# {os.path.dirname(file_path)}\n\nこの空間は Ryubo Theater のシステムによって管理されています。\n"
    elif base_name == "__init__.py":
        content = "# Procedure Package Init\n"
    elif base_name == "base.py":
        content = 'class BaseProcedure:\n    """各専門プロシージャのベースクラス"""\n    def run(self):\n        raise NotImplementedError\n'
    else:
        content = f"# {base_name}\n"

    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

def self_repair(blueprint_data):
    """設計図に基づきディレクトリとファイルを構築する"""
    print("🛠️ [Manager 自律修復] 舞台セットを点検します...")
    
    for item in blueprint_data.get("required_tree", []):
        path = item["path"]
        
        if item["type"] == "directory":
            os.makedirs(path, exist_ok=True)
            
            # ファイル生成
            for file_name in item.get("files", []):
                file_path = os.path.join(path, file_name)
                create_default_file(file_path)
                    
            # サブディレクトリ生成
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
        print("🎬 舞台の点検・修復が完了しました。")
    else:
        print("⚠️ 警告: theater_blueprint.yaml が見つかりません。")

if __name__ == "__main__":
    main()
