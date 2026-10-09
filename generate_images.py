import os
import glob
import requests
import urllib.parse

def generate_images():
    os.makedirs('assets/images', exist_ok=True)
    scenes = ['scene1', 'scene2', 'scene3', 'scene4']
    cuts = ['01', '02', '03']
    
    base_prompt = "cinematic film still, 16:9 aspect ratio, dark philosophical atmosphere, glowing lights, Japanese aesthetics, high quality, 8k"
    
    for s in scenes:
        for c in cuts:
            img_name = f"{s}_{c}_16_9.png"
            img_path = os.path.join('assets/images', img_name)
            
            # 各カットの雰囲気を変える個別プロンプトの構成
            prompt = f"{base_prompt}, scene {s} cut {c}, mysterious shadow and light"
            encoded_prompt = urllib.parse.quote(prompt)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true"
            
            print(f"Downloading image: {img_name}...")
            try:
                res = requests.get(image_url, timeout=30)
                if res.status_code == 200:
                    with open(img_path, 'wb') as f:
                        f.write(res.content)
                    print(f"Image saved: {img_path}")
            except Exception as e:
                print(f"Failed to generate {img_name}: {e}")

if __name__ == '__main__':
    generate_images()
