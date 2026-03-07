import sys
from PyQt5.QtWidgets import QApplication


from QuickViewer import QuickViewer

def main():
    app = QApplication(sys.argv)
    
    if len(sys.argv) < 2:
        print("Usage: python image_viewer.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    
    viewer = QuickViewer()
    viewer.openImage(image_path)
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()