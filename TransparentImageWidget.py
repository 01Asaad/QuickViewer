from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt, QPoint, QRect
from PySide6.QtGui import QPixmap, QPainter, QColor, QWheelEvent

class TransparentImageWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = None
        self.scale_factor = 1.0
        self.offset = QPoint(0, 0)
        self.drag_start_point = None
        self.max_scale = 1.0
        self.setMouseTracking(True)
        
    def setImage(self, image_path):
        self.image = QPixmap(image_path)
        self.calculateInitialScale()
        self.offset = QPoint(0, 0)
        self.update()
        
    def calculateInitialScale(self):
        if not self.image:
            return
            
        screen_geometry = QApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        
        
        max_width = screen_width * 0.75
        max_height = screen_height * 0.75
        
       
        width_scale = max_width / self.image.width()
        height_scale = max_height / self.image.height()
        
        self.scale_factor = min(width_scale, height_scale)
        
        self.max_scale = max(2.0, self.scale_factor * 2)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        
        painter.fillRect(self.rect(), QColor(0, 0, 0, 180))
        
        if self.image:
            scaled_width = self.image.width() * self.scale_factor
            scaled_height = self.image.height() * self.scale_factor
            
            x = (self.width() - scaled_width) / 2 + self.offset.x()
            y = (self.height() - scaled_height) / 2 + self.offset.y()
            
            painter.drawPixmap(QRect(int(x), int(y), int(scaled_width), int(scaled_height)), self.image)
    def zoomin(self, zoom_factor) :
        new_scale = self.scale_factor * zoom_factor
        if new_scale <= self.max_scale:
            self.scale_factor = new_scale
    def zoomout(self, zoom_factor) :
        new_scale = self.scale_factor / zoom_factor
        if new_scale >= 0.1:
            self.scale_factor = new_scale
    def wheelEvent(self, event: QWheelEvent):
        zoom_factor = 1.1
        if event.angleDelta().y() > 0:
            self.zoomin(zoom_factor)
        else:
            self.zoomout(zoom_factor)
                
        self.update()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_point = event.pos()
            
    def mouseMoveEvent(self, event):
        if self.drag_start_point is None: return
        
        delta = event.pos() - self.drag_start_point
        self.offset += delta
        self.drag_start_point = event.pos()
        self.update()
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_point = None
