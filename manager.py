"""
role: "総監督：リポジトリのツリー構造定義を保持し、起動時に欠落しているディレクトリやファイルを自律的に自動修復してから、各専門スタッフ（クラス）をインスタンス化して全工程を指揮する"
"""

import sys
import os
import yaml

# procedures/ フォルダをインポートパスに追加できるようにする
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 🎬 監督が保持する「理想のリポジトリ・ツリー構造」のYAML定義
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
  - path: "assets/"
    type: "directory"
    role: "アセット実体の保管場所"
    sub_dirs:
      - "assets/images/"
      - "assets/audios/"
  - path: ".trash/"
    type: "directory"
    role: "古いフィルム・不要ファイルの退避場所"
  - path: "procedures/"
    type: "directory"
    role: "専門工程モジュール群"
    files:
      - "__init__.py"
      - "base.py"
      - "procedure1.py"
      - "procedure2.py"
      - "procedure3.py"
      - "procedure4.py"
"""

def self_repair(blueprint_data):
    """監督自らがツリー設計図に基づき、不足している部屋やファイル、ベースクラスを構築する"""
    print("🛠️ [Manager 自律修復] ツリー設計図と現行の舞台セットを照合し、不足箇所を構築します...")
    
    for item in blueprint_data.get("required_tree", []):
        path = item["path"]
        item_type = item["type"]
        
        if item_type == "directory":
            os.makedirs(path, exist_ok=True)
            for sub in item.get("sub_dirs", []):
                os.makedirs(sub, exist_ok=True)
            for file_name in item.get("files", []):
                file_path = os.path.join(path, file_name)
                if not os.path.exists(file_path):
                    create_default_procedure_file(file_path)
                    print(f"✨ スタッフ（ファイル）を自動配備しました: {file_path}")
                    
        elif item_type == "file" and path == "index.html":
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    f.write("<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Ryubo Theater</title></head><body><h1>Initializing Theater...</h1></body></html>")
                print(f"✨ 初期スクリーンを自動配置しました: {path}")

def create_default_procedure_file(file_path):
    """各プロシージャおよびベースクラスの初期クラス雛形テンプレート"""
    base_name = os.path.basename(file_path)
    content = ""
    
    if base_name == "__init__.py":
        content = "# procedures package\n"
    elif base_name == "base.py":
        content = '''class BaseProcedure:
    """すべての専門工程（プロシージャ）の共通ベースクラス"""
    def __init__(self, name):
        self.name = name

    def run(self, *args, **kwargs):
        raise NotImplementedError("各プロシージャクラスで run メソッドを実装してください。")
'''
    elif base_name == "procedure1.py":
        content = '''import os, glob
from procedures.base import BaseProcedure

class Procedure1(BaseProcedure):
    def __init__(self):
        super().__init__("Procedure1: フィルム点検")

    def run(self):
        print(f"🎬 [{self.name}] フィルムの点検を開始します。")
        os.makedirs("documents", exist_ok=True)
        films = glob.glob("documents/Film.*.md")
        if not films:
            sample = "documents/Film.2026.10.15.AM.md"
            with open(sample, "w", encoding="utf-8") as f:
                f.write("scenario:\\n  title: \\"初期自動生成フィルム\\"\\nacts: []\\n")
            films = [sample]
        films.sort()
        return films[-1]
'''
    elif base_name == "procedure2.py":
        content = '''import re
from procedures.base import BaseProcedure

class Procedure2(BaseProcedure):
    def __init__(self):
        super().__init__("Procedure2: フィルム解析")

    def run(self, film_path):
        print(f" projector [{self.name}] フィルム解析: {film_path}")
        with open(film_path, "r", encoding="utf-8") as f:
            content = f.read()
        cuts = re.findall(r"## CUT \d+|## SCENE \d+|act:", content)
        return {"film_path": film_path, "total_cuts": max(len(cuts), 1)}
'''
    elif base_name == "procedure3.py":
        content = '''import os
from procedures.base import BaseProcedure

class Procedure3(BaseProcedure):
    def __init__(self):
        super().__init__("Procedure3: ポータル構築")

    def run(self, build_data):
        print(f"🖥️ [{self.name}] シアターポータルをビルド中...")
        html = f"<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Ryubo Style</title></head><body><h1>Ryubo Cinema</h1><p>Latest Film: {os.path.basename(build_data['film_path'])}</p></body></html>"
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
        return "index.html"
'''
    elif base_name == "procedure4.py":
        content = '''import os
from procedures.base import BaseProcedure

class Procedure4(BaseProcedure):
    def __init__(self):
        super().__init__("Procedure4: クランクアップ検証")

    def run(self):
        print(f"🔍 [{self.name}] 最終確認クランクアップ検証中...")
        if not os.path.exists("index.html"): 
            raise FileNotFoundError("index.html がありません")
        print("🎉 クランクアップ！すべての検証が完了しました。")
        return True
'''
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def direct():
    print("🎬🎬🎬 [Manager] 映画監督による全体ディレクションを開始します。")
    blueprint = yaml.safe_load(REPOSITORY_BLUEPRINT)
    print(f"🎯 対象プロジェクト: {blueprint['project_name']}")
    
    try:
        # 1. 監督による自律修復（ベースクラスやプロシージャクラスの配備）
        self_repair(blueprint)
        
        # 2. クラス化された各専門スタッフをインポート
        from procedures.procedure1 import Procedure1
        from procedures.procedure2 import Procedure2
        from procedures.procedure3 import Procedure3
        from procedures.procedure4 import Procedure4

        print("\n--- [第一幕: スタッフインスタンス化 & 実行] ---")
        proc1 = Procedure1()
        latest_film = proc1.run()
        
        print("\n--- [第二幕: スタッフインスタンス化 & 実行] ---")
        proc2 = Procedure2()
        build_data = proc2.run(latest_film)
        
        print("\n--- [第三幕: スタッフインスタンス化 & 実行] ---")
        proc3 = Procedure3()
        index_file = proc3.run(build_data)
        
        print("\n--- [第四幕: スタッフインスタンス化 & 実行] ---")
        proc4 = Procedure4()
        proc4.run()
        
        print("\n" + "="*50)
        print("✨✨✨ [Manager] すべての撮影が無事にクランクアップしました！お疲れ様でした。 ✨✨✨")
        print("="*50)
        
    except Exception as e:
        print("\n" + "="*50)
        print("🚨 [Manager 裁定] 撮影現場から不整合・エラーの報告を受け取りました。")
        print(f"⚠️ 現場からの報告内容: {e}")
        print("🛡️ 監督権限を発動：ツリー設計図との整合性を守るため、これ以上の進行を中止し保護します。")
        print("="*50 + "\n")
        sys.exit(1)

if __name__ == "__main__":
    direct()
