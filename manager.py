"""
role: "総監督：リポジトリの全体指揮を執り、各専門スタッフ（Procedures）を順次起動して、最終成果物をリポジトリへ自動コミット＆プッシュして定着させる"
"""

import sys
import os
import yaml
import subprocess

# procedures/ フォルダをインポートパスに追加できるようにする
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def git_commit_and_push():
    """監督自らが成果物や修復されたツリー構造をリポジトリへ自動保存（コミット＆プッシュ）する"""
    print("📦 [Manager Git保全] 生成・修復された成果物をリポジトリへ永続化します...")
    
    try:
        # Gitのユーザー設定（Actions環境用）
        subprocess.run(["git", "config", "--global", "user.name", "github-actions[bot]"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], check=True)
        
        # 変更があるかチェック
        status_result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        if not status_result.stdout.strip():
            print("✨ 変更事項はありませんでした（すでに最新の状態です）。")
            return

        # 追加・コミット・プッシュ
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "🎬 Autonomous Theater: Auto-repair and portal build by Manager"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("🚀 リモートリポジトリへのプッシュが成功し、舞台装置が完全に定着しました！")
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git操作中にエラーが発生しました: {e}")
        raise

def direct():
    print("🎬🎬🎬 [Manager] 映画監督による全体ディレクションを開始します。")
    
    try:
        # 1. クラス化された各専門スタッフをインポート
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
        
        # 2. 成果物のGit永続化（コミット＆プッシュ）
        git_commit_and_push()
        
        print("\n" + "="*50)
        print("✨✨✨ [Manager] すべての撮影が無事にクランクアップし、リポジトリに定着しました！ ✨✨✨")
        print("="*50)
        
    except Exception as e:
        print("\n" + "="*50)
        print("🚨 [Manager 裁定] 現場から不整合・エラーの報告を受け取りました。")
        print(f"⚠️ 現場からの報告内容: {e}")
        print("🛡️ 監督権限を発動：ツリー設計図との整合性を守るため、これ以上の進行を中止し保護します。")
        print("="*50 + "\n")
        sys.exit(1)

if __name__ == "__main__":
    direct()
