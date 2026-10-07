import os
import re
from gtts import gTTS

def parse_script(markdown_text):
    """
    台本（Markdown）からセリフやナレーションを抽出する関数
    """
    lines = markdown_text.split("\n")
    dialogues = []
    
    current_speaker = "語り手"
    
    for line in lines:
        line = line.strip()
        
        # ト書き（括弧書き）や見出し、装飾をスキップ
        if not line or line.startswith("#") or line.startswith("**（") or line.startswith("*"):
            continue
            
        # 話者の抽出 (例: **さとし**： や **語り手**：)
        speaker_match = re.match(r"^\*\*(.*?)\*\*：(.*)", line)
        if speaker_match:
            current_speaker = speaker_match.group(1).strip()
            text = speaker_match.group(2).strip()
        else:
            text = line
            
        # 記号などの余分な装飾（太字や斜体など）を除去
        clean_text = re.sub(r"[\*\_\（\）\(\)]", "", text).strip()
        
        if clean_text:
            dialogues.append({
                "speaker": current_speaker,
                "text": clean_text
            })
            
    return dialogues


def generate_audio_from_script(script_path, output_dir="assets/audio"):
    """
    台本ファイルを読み込み、音声ファイル(.mp3)を出力する関数
    """
    if not os.path.exists(script_path):
        print(f"エラー: 台本ファイルが見つかりません: {script_path}")
        return

    os.makedirs(output_dir, exist_ok=True)
    
    with open(script_path, "r", encoding="utf-8") as f:
        markdown_text = f.read()
        
    dialogues = parse_script(markdown_text)
    
    print(f"--- 台本の解析完了 ({len(dialogues)} 件の音声要素) ---")
    
    # 抽出したテキストを1つの統合音声として出力（または行ごとに個別保存）
    full_text = ""
    for idx, item in enumerate(dialogues, 1):
        print(f"[{idx}] {item['speaker']}: {item['text']}")
        full_text += f"{item['text']}。\n"

    # 日本語音声（ja）として音声化
    print("\n音声ファイルの生成中...")
    tts = gTTS(text=full_text, lang='ja', slow=False)
    
    # ファイル名を設定して保存
    base_name = os.path.splitext(os.path.basename(script_path))[0]
    output_filepath = os.path.join(output_dir, f"{base_name}.mp3")
    tts.save(output_filepath)
    
    print(f"成功: 音声ファイルを保存しました ➔ {output_filepath}")


if __name__ == "__main__":
    # 対象の台本ファイルのパス（必要に応じて変更）
    script_file = "documents/Oriented-Philosophia.2026.10.07.A.md"
    
    # 実行
    generate_audio_from_script(script_file)
