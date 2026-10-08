import os
import glob
import re
import urllib.parse
import urllib.request

def extract_prompts(markdown_text):
    """
    台本から <!-- IMAGE_PROMPT: ... --> の注記を抽出する関数
    見つからない場合はデフォルトのプロンプトを返す
    """
    prompts = re.findall(r"<!--\s*IMAGE_PROMPT:\s*(.*?)\s*-->", markdown_text, re.IGNORECASE)
    
    if not prompts:
        # プロンプト注記がない場合のデフォルトプロンプト（沖縄のガジュマルと光）
        prompts = [
            "Okinawa banyan tree with deep massive roots, light and shadow, dramatic cinematic lighting, masterpiece, 8k"
        ]
    return prompts

def generate_images_from_scripts(input_dir="documents", output_dir="assets/images"):
    """
    documents フォルダ内の台本を読み込み、対応する挿絵画像を自動出力する関数
    """
    script_files = glob.glob(os.path.join(input_dir, "*.md"))
    
    if not script_files:
        print("処理対象の .md ファイルが見つかりませんでした。")
        return

    os.makedirs(output_dir, exist_ok=True)
    print(f"=== 合計 {len(script_files)} 件の台本から画像を生成します ===")

    for script_path in script_files:
        filename = os.path.basename(script_path)
        base_name = os.path.splitext(filename)[0]

        if base_name.startswith("PROMPT") or base_name.startswith("PROJECT"):
            continue

        print(f"\n▶ 画像生成中: {filename}")

        with open(script_path, "r", encoding="utf-8") as f:
            markdown_text = f.read()

        prompts = extract_prompts(markdown_text)

        for idx, prompt_text in enumerate(prompts, 1):
            # URLエンコード処理
            encoded_prompt = urllib.parse.quote(prompt_text)
            
            # Pollinations.ai の高画質画像生成URL (16:9のアスペクト比: 1280x720)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true&seed=42"
            
            suffix = f"_{idx}" if len(prompts) > 1 else ""
            output_filepath = os.path.join(output_dir, f"{base_name}{suffix}.png")

            try:
                # 画像のダウンロードと保存
                req = urllib.request.Request(
                    image_url, 
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                with urllib.request.urlopen(req) as response, open(output_filepath, 'wb') as out_file:
                    out_file.write(response.read())
                print(f"  └ 成功: 画像保存 ➔ {output_filepath}")
            except Exception as e:
                print(f"  └ エラー発生: {e}")

    print("\n=== すべての画像生成が完了しました！ ===")

if __name__ == "__main__":
    generate_images_from_scripts()
