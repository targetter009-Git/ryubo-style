"""
role: "総監督：リポジトリのツリー構造定義を保持し、各プロシージャからの報告を元に全体指揮および例外時の裁定を行う"
acts:
  - step_1: "YAML形式で定義されたリポジトリの理想ツリー構造を把握する"
  - step_2: "各プロシージャ（1〜4）を順次キックする"
  - step_3: "プロシージャから返されたエラーや不整合を受け取り、監督判断で修復指示または安全停止（ロールバック）を行う"
"""

import sys
import os
import yaml

# procedures/ フォルダをインポートパスに追加
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
    expected_pattern: "Film.YYYY.MM.DD.?M.md"
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
      - "procedure1.py"
      - "procedure2.py"
      - "procedure3.py"
      - "procedure4.py"
"""

def direct():
    print("🎬🎬🎬 [Manager] 映画監督による全体ディレクションを開始します。")
    print("📋 [Manager] 監督の脳内ツリー設計図（Blueprint）を確認中...")
    blueprint = yaml.safe_load(REPOSITORY_BLUEPRINT)
    print(f"🎯 対象プロジェクト: {blueprint['project_name']}")
    
    try:
        # この後 procedures/ フォルダや子モジュールを呼び出していくため、
        # まっさらな状態の現段階では、まずはモジュール群のインポートテストが行われます。
        from procedures import procedure1, procedure2, procedure3, procedure4

        print("\n--- [第一幕: Procedure 1 実行] ---")
        latest_film = procedure1.run()
        
        print("\n--- [第二幕: Procedure 2 実行] ---")
        build_data = procedure2.run(latest_film)
        
        print("\n--- [第三幕: Procedure 3 実行] ---")
        index_file = procedure3.run(build_data)
        
        print("\n--- [第四幕: Procedure 4 実行] ---")
        procedure4.run()
        
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
