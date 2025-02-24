import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QColorDialog, QMessageBox
)
#from PyQt6.QtGui import QColor,QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QColorDialog, QMessageBox


# Funkcje konwersji
def RGB_to_OLE(red, green, blue):
    return red + (green * 256) + (blue * 256 * 256)


def OLE_to_RGB(ole_color):
    red = ole_color & 0xFF
    green = (ole_color >> 8) & 0xFF
    blue = (ole_color >> 16) & 0xFF
    return red, green, blue


class ColorConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Color Converter (RGB ↔ OLE)")
        self.setGeometry(100, 100, 400, 200)

        # Główne układy
        main_layout = QVBoxLayout()

        # Input RGB
        rgb_layout = QHBoxLayout()
        rgb_layout.addWidget(QLabel("RGB (R,G,B):"))
        self.rgb_input = QLineEdit()
        rgb_layout.addWidget(self.rgb_input)
        self.rgb_to_ole_btn = QPushButton("Convert to OLE")
        self.rgb_to_ole_btn.clicked.connect(self.convert_rgb_to_ole)
        rgb_layout.addWidget(self.rgb_to_ole_btn)

        # Input OLE
        ole_layout = QHBoxLayout()
        ole_layout.addWidget(QLabel("OLE Color:"))
        self.ole_input = QLineEdit()
        ole_layout.addWidget(self.ole_input)
        self.ole_to_rgb_btn = QPushButton("Convert to RGB")
        self.ole_to_rgb_btn.clicked.connect(self.convert_ole_to_rgb)
        ole_layout.addWidget(self.ole_to_rgb_btn)

        # Przyciski wyboru kolorów
        color_picker_btn = QPushButton("Select Color (RGB)")
        color_picker_btn.clicked.connect(self.open_color_picker)
        main_layout.addWidget(color_picker_btn)

        # Dodanie układów
        main_layout.addLayout(rgb_layout)
        main_layout.addLayout(ole_layout)

        # Wyniki
        self.result_label = QLineEdit("")
        main_layout.addWidget(self.result_label)

        # Ustawienie układu
        self.setLayout(main_layout)

    def convert_rgb_to_ole(self):
        try:
            # Pobieranie wartości RGB
            rgb_text = self.rgb_input.text()
            red, green, blue = map(int, rgb_text.split(","))
            if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
                raise ValueError("Values must be in the range 0-255.")

            # Konwersja do OLE
            ole_color = RGB_to_OLE(red, green, blue)
            self.result_label.setText(f"OLE Color: {ole_color}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid RGB input: {e}")

    def convert_ole_to_rgb(self):
        try:
            # Pobieranie wartości OLE
            ole_color = int(self.ole_input.text())
            if ole_color < 0:
                raise ValueError("OLE color must be a positive integer.")

            # Konwersja do RGB
            red, green, blue = OLE_to_RGB(ole_color)
            self.result_label.setText(f"{red}, {green}, {blue}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid OLE input: {e}")

    def open_color_picker(self):
        color = QColorDialog.getColor()
        if color.isValid():
            red, green, blue = color.red(), color.green(), color.blue()
            self.rgb_input.setText(f"{red},{green},{blue}")


# Uruchamianie aplikacji
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ColorConverterApp()
    window.show()
    sys.exit(app.exec())