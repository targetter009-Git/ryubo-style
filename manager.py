import os
import sys
import traceback

def run_step(step_name, func):
    """個別の処理ステップを安全に実行し、エラートラップするラッパー"""
    print(f"\n=== [START] {step_name} ===")
    try:
        func()
        print(f"=== [SUCCESS] {step_name} ===")
        return True
    except Exception as e:
        print(f"=== [ERROR] Failed in {step_name} ===")
        traceback.print_exc()
        return False

def step_images():
    # 画像生成処理のインポートと実行
    import generate_images
    generate_images.generate_images()

def step_speech():
    # 音声合成処理のインポートと実行
    import generate_speech
    generate_speech.generate_speech()

def step_movies():
    # 動画結合処理のインポートと実行
    import generate_movies
    generate_movies.generate_movies()

def main():
    print("🎬 全自動シネマティック生成マネージャー (manager.py) を起動します...")
    
    # 1. 画像生成ステップ
    if not run_step("Image Generation", step_images):
        sys.exit(1)
        
    # 2. 音声合成ステップ
    if not run_step("Speech Generation", step_speech):
        sys.exit(1)
        
    # 3. 動画結合ステップ
    if not run_step("Movie Generation", step_movies):
        sys.exit(1)
        
    print("\n🎉 すべてのマルチメディア生成プロセスが正常に完了しました！")

if __name__ == '__main__':
    main()
