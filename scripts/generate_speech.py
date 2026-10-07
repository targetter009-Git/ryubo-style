import os
import glob
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
        
        # 見出しや空行、ト書き注記（*（SE: ...）* など）をスキップ
        if not line or line.startswith("#") or line.startswith("*（") or line.startswith("【"):
            continue
            
        # 話者の抽出 (例: **語り手（さとし）**： や *語り手* ：)
        speaker_match = re.match(r"^[\*\_]*(.*?)[\*\_]*\s*[:：](.*)", line)
        if speaker_match:
            current_speaker = speaker_match.group(1).strip()
            text = speaker_match.group(2).strip()
        else:
            text = line
            
        # マークダウン装飾や括弧（演出指示）を削除
        clean_text = re.sub(r"[\*\_\（\）\(\)]", "", text).strip()
        
        if clean_text:
            dialogues.append({
                "speaker": current_speaker,
                "text": clean_text
            })
            
    return dialogues


def process_all_scripts(input_dir="documents", output_dir="assets/audio"):
    """
    documents フォルダ内のすべての .md ファイルを一括処理する関数
    """
    # .md ファイルをすべて検索
    script_files = glob.glob(os.path.join(input_dir, "*.md"))
    
    if not script_files:
        print(f"警告: {input_dir} フォルダ内に .md ファイルが見つかりませんでした。")
        return

    os.makedirs(output_dir, exist_ok=True)
    print(f"=== 合計 {len(script_files)} 件の台本ファイルを処理します ===")

    for script_path in script_files:
        filename = os.path.basename(script_path)
        base_name = os.path.splitext(filename)[0]
        
        # PROMPT などの台本以外のマークダウンはスキップ
        if base_name.startswith("PROMPT") or base_name.startswith("PROJECT"):
            continue

        print(f"\n▶ 処理中: {filename}")

        with open(script_path, "r", encoding="utf-8") as f:
            markdown_text = f.read()

        dialogues = parse_script(markdown_text)

        if not dialogues:
            print("  ↳ 読上げ可能なセリフが見つかりませんでした。")
            continue

        # セリフをひとつのテキストに結合
        full_text = "。\n".join([item['text'] for item in dialogues])

        # gTTS で音声化
        tts = gTTS(text=full_text, lang='ja', slow=False)
        output_filepath = os.path.join(output_dir, f"{base_name}.mp3")
        tts.save(output_filepath)

        print(f"  └ 成功: 保存完了 ➔ {output_filepath}")

    print("\n=== すべての音声生成が完了しました！ ===")


if __name__ == "__main__":
    # documents/ 内の全台本を一括変換
    process_all_scripts()
