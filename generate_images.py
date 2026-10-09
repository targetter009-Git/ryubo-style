import os
import glob

def generate_images():
    """
    12コマの16:9画像プレースホルダー生成スクリプト
    assets/images/ 内へ指定の12コマ画像を準備する
    """
    os.makedirs('assets/images', exist_ok=True)
    
    scenes = ['scene1', 'scene2', 'scene3', 'scene4']
    cuts = ['01', '02', '03']
    
    for s in scenes:
        for c in cuts:
            img_name = f"{s}_{c}_16_9.png"
            img_path = os.path.join('assets/images', img_name)
            if not os.path.exists(img_path):
                with open(img_path, 'wb') as f:
                    f.write(b'') # 16:9プレースホルダー作成
                print(f"Created placeholder: {img_name}")

if __name__ == '__main__':
    generate_images()
