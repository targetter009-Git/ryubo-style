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
