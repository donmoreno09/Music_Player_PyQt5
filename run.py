from main import ModernMusicPlayer
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
window = ModernMusicPlayer()
window.show()

sys.exit(app.exec())