import os
import glob

def generate_speech():
    """
    音声トラック（.mp3）のプレースホルダー生成スクリプト
    assets/audios/ 内へ音声アセット枠を準備する
    """
    os.makedirs('assets/audios', exist_ok=True)
    
    # フィルムごとの音声枠作成
    for p in ['A', 'B']:
        audio_path = f"assets/audios/Film.2026.10.09.AM.{p}.mp3"
        if not os.path.exists(audio_path):
            with open(audio_path, 'wb') as f:
                f.write(b'') # 音声ファイルのプレースホルダー
            print(f"Created audio placeholder: {audio_path}")

if __name__ == '__main__':
    generate_speech()
