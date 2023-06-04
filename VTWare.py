import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineDownloadItem


class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self.setFixedHeight(25)
        self.setStyleSheet("background-color: gray;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(0)

        self.title_label = QLabel(self)
        self.title_label.setStyleSheet("font-weight: bold; color: white;")
        layout.addWidget(self.title_label)

        minimize_button = QPushButton("_", self)
        minimize_button.setFixedSize(20, 20)
        minimize_button.clicked.connect(parent.showMinimized)
        layout.addWidget(minimize_button)

        maximize_button = QPushButton("□", self)
        maximize_button.setFixedSize(20, 20)
        maximize_button.clicked.connect(self.toggle_maximized)
        layout.addWidget(maximize_button)

        close_button = QPushButton("✕", self)
        close_button.setFixedSize(20, 20)
        close_button.clicked.connect(parent.close)
        layout.addWidget(close_button)

        self.draggable = False
        self.offset = QPoint()

    def toggle_maximized(self):
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def mousePressEvent(self, event):
        self.draggable = True
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable:
            self.window().move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.draggable = False


class WebBrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VTWare")
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Create the custom title bar
        self.title_bar = CustomTitleBar(self)
        self.setMenuWidget(self.title_bar)

        # Create the web view
        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)

        # Configure the web engine profile to enable downloads
        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.downloadRequested.connect(self.handle_download_request)

        # Load the initial URL
        self.load_url("https://emupedia.net/beta/emuos/")

    def load_url(self, url):
        self.web_view.load(QUrl(url))

    def handle_download_request(self, download):
        download_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)")
        if download_path:
            download.setPath(download_path)
            download.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebBrowserWindow()
    window.show()
    sys.exit(app.exec_())
