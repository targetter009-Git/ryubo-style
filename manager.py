"""
role: "総監督：リポジトリのツリー構造設計図に基づき、起動時に欠落しているディレクトリや各部屋のREADME（仕様書・スキーマ）、専門スタッフクラスを自律的に自動修復してから、全工程を指揮する"
"""

import sys
import os
import yaml

# procedures/ フォルダをインポートパスに追加できるようにする
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 🎬 監督が保持する「理想のリポジトリ・ツリー構造とスキーマ定義」のYAMLブループリント
REPOSITORY_BLUEPRINT = """
project_name: "ryubo-style"
required_tree:
  - path: "manager.py"
    type: "file"
    role: "総監督"
  - path: "index.html"
    type: "file"
    role: "スクリーン（シアターポータル）"
  - path: "documents/"
    type: "directory"
    role: "フィルム（台本）の控室"
    files:
      - "README.md"
  - path: "assets/"
    type: "directory"
    role: "アセット実体の保管場所"
    files:
      - "README.md"
    sub_dirs:
      - path: "assets/images/"
        readme: true
      - path: "assets/audios/"
        readme: true
      - path: "assets/videos/"
        readme: true
      - path: "assets/prompts/"
        readme: true
  - path: ".trash/"
    type: "directory"
    role: "古いフィルム・不要ファイルの退避場所"
  - path: "procedures/"
    type: "directory"
    role: "専門工程モジュール群"
    files:
      - "README.md"
      - "__init__.py"
      - "base.py"
      - "procedure1.py"
      - "procedure2.py"
      - "procedure3.py"
      - "procedure4.py"
"""

def self_repair(blueprint_data):
    """監督自らがツリー設計図に基づき、不足している部屋、ファイル、各所のREADME（スキーマ）を構築する"""
    print("🛠️ [Manager 自律修復] ツリー設計図と現行の舞台セットを照合し、不足箇所を構築します...")
    
    for item in blueprint_data.get("required_tree", []):
        path = item["path"]
        item_type = item["type"]
        
        if item_type == "directory":
            os.makedirs(path, exist_ok=True)
            
            # ディレクトリ直下のファイル生成
            for file_name in item.get("files", []):
                file_path = os.path.join(path, file_name)
                if not os.path.exists(file_path):
                    create_default_file(file_path)
                    print(f"✨ 規約ドキュメント/スタッフを配備しました: {file_path}")
                    
            # サブディレクトリの生成
            for sub in item.get("sub_dirs", []):
                sub_path = sub["path"]
                os.makedirs(sub_path, exist_ok=True)
                if sub.get("readme", False):
                    sub_readme = os.path.join(sub_path, "README.md")
                    if not os.path.exists(sub_readme):
                        create_default_file(sub_readme)
                        print(f"✨ アセット管理用READMEを配備しました: {sub_readme}")
                        
        elif item_type == "file" and path == "index.html":
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    f.write("<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Ryubo Theater</title></head><body><h1>Initializing Theater...</h1></body></html>")
                print(f"✨ 初期スクリーンを自動配置しました: {path}")

def create_default_file(file_path):
    """各種プロシージャ、ベースクラス、および各部屋のREADME（スキーマ定義）のテンプレート"""
    base_name = os.path.basename(file_path)
    parent_dir = os.path.dirname(file_path)
    content = ""
    
    if base_name == "README.md":
        if "documents" in parent_dir:
            content = """# 📜 documents/ フィルム（台本）控室の仕様書

このディレクトリには、上映するフィルム（Markdown台本）を保管します。

## フィルム命名規則
- 形式: `Film.YYYY.MM.DD.[AM/PM].md`
- 例: `Film.2026.10.15.AM.md`

## 台本スキーマ構造
```yaml
scenario:
  title: "フィルムのタイトル"
  protagonist: "主人公・視点"
acts:
  - act: 1
    title: "第一幕のタイトル"
    dialogue:
      - speaker: "話者名"
        line: "セリフやト書き"
