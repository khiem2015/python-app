from PyQt6.QtWidgets import*
from PyQt6.QtCore import *
from PyQt6 import uic
import sys
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/list.ui", self)
        self.init_ui()

    def init_ui(self):
        self.list_widegt = self.findChild(QListWidget, "list_widget")

        data = self.load_json()
        for item in data:
            self.list_widegt.addItem(item["name"])

    def load_json(self):
        with open("data/anime.json", "r") as f:
            data = json.load(f)
        return data
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())