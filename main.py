import os
import unicodedata
import shutil
from natsort import natsorted
from tqdm import tqdm
from pprint import pprint
from PIL import Image
try:
    import pillow_avif
except ImportError:
    print("AVIFファイルを扱う場合は 'pillow-avif-plugin' をインストールしてください")
    print("pip install pillow-avif-plugin")

supported_formats = [".jpeg", ".jpg", ".png", ".avif", ".webp", ".jpe", ".jfif", ".jif"]

input_dir = input("パスを入力してください: ")

def collect_images(dir):
    images = []
    for root, _, files in os.walk(dir):
        for file in natsorted(files):
            if isinstance(file, str) and file.lower().endswith(tuple(supported_formats)):
                images.append(os.path.join(root, file))
    return images

def get_spaces(dir_name):
    length = 0
    size = shutil.get_terminal_size(fallback=(80, 20)).columns * 0.5
    for ch in os.path.basename(dir_name):
        if unicodedata.east_asian_width(ch) in ('F', 'W'):
            length += 2
        else:
            length += 1
    return int(size) - length

def to_pdf(dir):
    image_files = collect_images(dir)
    if not image_files:
        print(f"{dir}に画像が見つかりません。スキップします。")
        return
    
    images = []
    spaces = get_spaces(os.path.basename(dir))

    for _, file in enumerate(tqdm(image_files, ascii="-#", desc=f"Processing: {os.path.basename(dir)}{' ' * spaces}", unit="img", bar_format="{l_bar}{bar} {n_fmt}/{total_fmt}")):
        img = Image.open(file)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        images.append(img)

    title = os.path.join(os.path.dirname(dir), os.path.basename(dir) + ".pdf")
    images[0].save(title, save_all=True, append_images=images[1:])

for dir in os.listdir(input_dir):
    path = os.path.join(input_dir, dir)
    if os.path.isdir(path):
        to_pdf(path)