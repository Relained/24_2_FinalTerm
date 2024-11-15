import os
import shutil
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image

# 폴더 경로 설정
folder_1 = r"C:\Users\admin\Desktop\ss"
folder_2 = r"C:\Users\admin\Desktop\real"
folder_3 = r"C:\Users\admin\Desktop\emo"
folder_4 = r"C:\Users\admin\Desktop\zzal"

# 폴더가 없으면 생성
for folder in [folder_1, folder_2, folder_3, folder_4]:
    os.makedirs(folder, exist_ok=True)

class ImageSorterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Sorter")
        self.setGeometry(100, 100, 600, 600)

        # 이미지 파일 경로 리스트
        self.image_paths = []
        self.current_index = 0  # 현재 이미지 인덱스

        # 레이아웃 설정
        layout = QVBoxLayout()

        # 이미지 레이블
        self.image_label = QLabel("Select images to display here.")
        self.image_label.setFixedSize(500, 500)
        layout.addWidget(self.image_label)

        # 버튼 레이아웃 설정
        button_layout = QHBoxLayout()

        # 이미지 선택 버튼
        self.select_button = QPushButton("Select Images")
        self.select_button.clicked.connect(self.select_images)
        button_layout.addWidget(self.select_button)

        # 폴더 이동 버튼들
        self.folder1_button = QPushButton("씹덕")
        self.folder1_button.clicked.connect(lambda: self.move_image(folder_1))
        button_layout.addWidget(self.folder1_button)

        self.folder2_button = QPushButton("사진")
        self.folder2_button.clicked.connect(lambda: self.move_image(folder_2))
        button_layout.addWidget(self.folder2_button)

        self.folder3_button = QPushButton("디시콘")
        self.folder3_button.clicked.connect(lambda: self.move_image(folder_3))
        button_layout.addWidget(self.folder3_button)

        self.folder4_button = QPushButton("짤")  # 새로운 폴더 버튼 추가
        self.folder4_button.clicked.connect(lambda: self.move_image(folder_4))
        button_layout.addWidget(self.folder4_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def select_images(self):
        # 파일 다이얼로그를 열어 여러 이미지 파일 선택
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", "Image Files (*.jpg *.jpeg *.png)", options=options)
        
        if files:
            self.image_paths = files
            self.current_index = 0
            self.display_image(self.image_paths[self.current_index])

    def display_image(self, file_path):
        # QPixmap으로 직접 로드하여 알파 채널 문제 해결
        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            # 만약 QPixmap이 이미지를 로드하지 못하면 알파 채널 제거 후 로드
            img = Image.open(file_path).convert("RGB")
            img.thumbnail((500, 500))
            img.save("temp_display.jpg")  # 임시 저장 후 다시 로드
            pixmap = QPixmap("temp_display.jpg")
        
        # QLabel 크기에 맞게 QPixmap을 스케일링하여 전체 이미지 표시
        scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)



    def move_image(self, folder_path):
        # 현재 이미지가 있는 경우 해당 폴더로 이동
        if self.image_paths:
            current_image_path = self.image_paths[self.current_index]
            shutil.move(current_image_path, folder_path)
            print(f"Image moved to: {folder_path}")

            # 다음 이미지 표시
            self.current_index += 1
            if self.current_index < len(self.image_paths):
                self.display_image(self.image_paths[self.current_index])
            else:
                # 모든 이미지를 이동한 경우
                self.image_label.clear()
                self.image_label.setText("All images moved.")
                self.image_paths = []
                self.current_index = 0

    def keyPressEvent(self, event):
        # 숫자 키로 폴더 이동 제어
        if event.key() == Qt.Key_1:
            self.move_image(folder_1)
        elif event.key() == Qt.Key_2:
            self.move_image(folder_2)
        elif event.key() == Qt.Key_3:
            self.move_image(folder_3)
        elif event.key() == Qt.Key_4:
            self.move_image(folder_4)

# 애플리케이션 실행
app = QApplication([])
window = ImageSorterApp()
window.show()
app.exec_()
