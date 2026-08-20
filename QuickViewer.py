from pathlib import Path

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                             QVBoxLayout, QPushButton)
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent

import os

from TransparentImageWidget import TransparentImageWidget


class QuickViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_image_index = 0
        self.image_files = []
        self.current_directory = None
        self.initUI()
        
    def initUI(self):
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.image_widget = TransparentImageWidget()
        self.main_layout.addWidget(self.image_widget)
        
        self.close_button_container = QPushButton(self)
        
        self.close_button_container.setFixedSize(50, 50)
        self.close_button_container.setStyleSheet("""
            QPushButton {
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
                background-color: rgba(100, 0, 0, 0);
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0);
            }
        """)
        self.close_button = QPushButton("✕", self.close_button_container)
        self.close_button.setFixedSize(30, 30)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 0, 0, 180);
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 100, 100, 200);
            }
        """)
        self.close_button.clicked.connect(self.close)
        self.close_button_container.clicked.connect(self.close)
        self.close_button.move(10, 10) 
        
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        width = int(screen_geometry.width() * 0.75)
        height = int(screen_geometry.height() * 0.75)
        self.resize(width, height)
        
        self.showFullScreen()

    def resizeEvent(self, event):
        self.close_button_container.move(self.width() - 50, 0)
        super().resizeEvent(event)
        
    def openImage(self, image_path):
        if not os.path.isfile(image_path):
            print(f"Error: File not found - {image_path}")
            return
            
        self.current_directory = Path(image_path).parent
        self.image_files = self.get_image_files()
        
        filename = os.path.basename(image_path)
        self.current_image_index = self.image_files.index(filename)   
        self.image_widget.setImage(image_path)
        self.update()
        
    def get_image_files(self):
        if not self.current_directory: return []
            
        IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tif', 'tiff', 'webp']
        files = []
        for file in os.scandir(self.current_directory):
            if file.name.split(".")[-1] in IMAGE_EXTENSIONS :
                files.append(file.name)
        return sorted(files)
        
    def show_next_image(self):
        print("showing next image")
        if not self.image_files:
            return
        if self.current_image_index+1 == len(self.image_files) : return
        self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
        image_path = self.current_directory / self.image_files[self.current_image_index]
        self.image_widget.setImage(image_path)
        
    def show_prev_image(self):
        if not self.image_files:
            return
        if self.current_image_index == 0 : return
        self.current_image_index = (self.current_image_index - 1) % len(self.image_files)
        image_path = self.current_directory / self.image_files[self.current_image_index]
        self.image_widget.setImage(image_path)
        
    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.close_button_container.setHidden(True)
            self.showNormal()
        else:
            self.close_button_container.setHidden(False)
            self.showFullScreen()
        
    def keyPressEvent(self, event: QKeyEvent):
        print(f"{event.key()} pressed")
        match event.key():
            case Qt.Key.Key_F : self.toggle_fullscreen()
            case Qt.Key.Key_E : self.show_next_image()
            case Qt.Key.Key_Q : self.show_prev_image()
            case Qt.Key.Key_Escape : self.close()
            case _ : super().keyPressEvent(event)

