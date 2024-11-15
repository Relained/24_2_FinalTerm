from pathlib import Path
from vision_api import label_detection
from collections import Counter

allowed_extensions = \
        {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.raw', '.ico', '.pdf', '.tiff'}

def open_image_binary(image_path):
    with open(image_path, 'rb') as image_file:
        binary_data = image_file.read()
    return binary_data

def frequent_labels_in_folder(folder_path):
    folder = Path(folder_path)
    if not folder.is_dir():
        raise ValueError(f"{folder_path}는 존재하지 않거나 디렉토리가 아닙니다.")

    print(f"{folder_path} 폴더에서 라벨 분석을 시작합니다.")
    all_labels = []

    for file in folder.rglob('*'):
        if file.is_file() and file.suffix.lower() in allowed_extensions:
            desc, _ = label_detection(str(file))
            all_labels.append(desc)

    label_counts = Counter(all_labels)
    label_counts = label_counts.most_common()
    return label_counts