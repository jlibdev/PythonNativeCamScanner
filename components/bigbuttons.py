from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize


def create_big_button(label, icon , action):
    button = QPushButton()
    button.setIcon(QIcon(icon))
    button.setText(label)
    button.setIconSize(QSize(30,30))
    button.clicked.connect(action)

    # Use margin instead of padding
    button.setStyleSheet("""
        QPushButton {
            padding: 50px;
        }
    """)

    return button
