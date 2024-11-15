import os
import shutil
import numpy as np
import cv2
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# 원본 데이터 폴더와 변환된 이미지 폴더 경로 설정
original_data_dir = r"C:\Users\admin\Desktop\datasets"       # 기존 데이터셋 경로
processed_data_dir = r"C:\Users\admin\Desktop\processed_data"  # 변환된 이미지 저장 경로

# GIF 및 WEBP 이미지를 PNG로 변환 (OpenCV 사용)
def convert_images(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            file_path = os.path.join(root, file)
            output_folder = root.replace(input_dir, output_dir)
            os.makedirs(output_folder, exist_ok=True)

            output_path = os.path.join(output_folder, os.path.splitext(file)[0] + '.png')

            # GIF 파일 처리
            if file.lower().endswith('.gif'):
                try:
                    cap = cv2.VideoCapture(file_path)
                    ret, frame = cap.read()  # 첫 번째 프레임 읽기
                    cap.release()
                    if ret:
                        cv2.imwrite(output_path, frame)  # 첫 번째 프레임 저장
                        print(f"Converted GIF {file} to PNG format.")
                except Exception as e:
                    print(f"Failed to process GIF {file}: {e}")

            # WEBP 파일 처리
            elif file.lower().endswith('.webp'):
                try:
                    img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
                    if img is not None:
                        if img.shape[-1] == 4:  # 투명 채널 처리
                            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                        cv2.imwrite(output_path, img)
                        print(f"Converted WEBP {file} to PNG format.")
                except Exception as e:
                    print(f"Failed to process WEBP {file}: {e}")

            # 기타 형식 처리
            else:
                try:
                    img = cv2.imread(file_path)
                    if img is not None:
                        cv2.imwrite(output_path, img)
                        print(f"Copied {file} to processed folder.")
                except Exception as e:
                    print(f"Failed to process {file}: {e}")

# 변환 함수 실행
convert_images(original_data_dir, processed_data_dir)

# 모델 구성
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# 기존 모델에 새로운 분류 레이어 추가
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
predictions = Dense(3, activation='softmax')(x)  # 클래스 수에 맞게 수정
model = Model(inputs=base_model.input, outputs=predictions)

# 사전 학습된 레이어를 동결
base_model.trainable = False

# 모델 컴파일
model.compile(optimizer=Adam(learning_rate=0.0001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# 데이터 로드 및 전처리 (변환된 이미지 폴더 사용)
train_datagen = ImageDataGenerator(rescale=1.0/255, validation_split=0.2)

train_data = train_datagen.flow_from_directory(
    processed_data_dir,           # 변환된 데이터 경로
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

val_data = train_datagen.flow_from_directory(
    processed_data_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

# 모델 학습
print("Starting model training...")
model.fit(
    train_data,
    validation_data=val_data,
    epochs=10
)

# 학습이 완료된 모델을 저장
model.save("my_trained_model.h5")
print("Model saved as 'my_trained_model.h5'")

# 변환된 이미지 폴더 삭제
print("Deleting processed data directory...")
shutil.rmtree(processed_data_dir)
print("Processed data directory deleted.")
