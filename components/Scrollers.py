from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

class imageSrollerV(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(70,500)
        self.mainlayout = QVBoxLayout(self)
        self.mainlayout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def clear_layout(self):
        while self.mainlayout.count():
            item = self.mainlayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def add_item(self, item):
        self.mainlayout.addWidget(item)



        