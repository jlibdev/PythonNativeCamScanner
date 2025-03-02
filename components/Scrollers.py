from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

class imageSrollerV(QWidget):
    def __init__(self):
        super().__init__()
        self.sizeIncrement = 80
        self.height = 80
        self.setFixedWidth(70)
        self.setFixedHeight(self.height)
        self.mainlayout = QVBoxLayout(self)
        self.mainlayout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def clear_layout(self):
        while self.mainlayout.count():
            item = self.mainlayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def add_item(self, item):
        self.mainlayout.addWidget(item)
        self.height = self.height + self.sizeIncrement
        self.setFixedHeight(self.height)
    def removed_item(self):
         self.height = self.height - self.sizeIncrement
         self.setFixedHeight(self.height)
    



        