from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QComboBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
# from PIL import Image, ImageEnhance, ImageFilter  

App = QApplication([])
main_window = QWidget()
main_window.setWindowTitle("Photo Editor")
main_window.resize(800, 600)

# Add widgets
btn_folder = QPushButton("folder")
file_list = QListWidget()

btn_left = QPushButton("Left")
btn_right = QPushButton("Right")
mirror = QPushButton("Mirror")
sharpness = QPushButton("Sharpness")
brightness = QPushButton("Brightness")
contrast = QPushButton("Contrast")
saturation = QPushButton("Saturation")
blur = QPushButton("Blur")
rotate = QPushButton("Rotate")
crop = QPushButton("Crop")
gray = QPushButton("Black and White")

# Dropdown menu
filter_box = QComboBox()
filter_box.addItem("Original")
filter_box.addItem("Left")
filter_box.addItem("Right")
filter_box.addItem("Mirror")
filter_box.addItem("Sharpness")
filter_box.addItem("Brightness")
filter_box.addItem("Contrast")
filter_box.addItem("Saturation")
filter_box.addItem("Blur")
filter_box.addItem("Rotate")
filter_box.addItem("Crop")
filter_box.addItem("Gray")

picture_box = QLabel("Picture")

# Layout
master_layout = QVBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()

col1.addWidget(btn_folder)
col2.addWidget(file_list)
col1.addWidget(filter_box)
col1.addWidget(btn_left)
col1.addWidget(btn_right)
col1.addWidget(mirror)
col1.addWidget(sharpness)
col1.addWidget(brightness)
col1.addWidget(contrast)
col1.addWidget(saturation)
col1.addWidget(blur)
col1.addWidget(rotate)
col1.addWidget(crop)
col1.addWidget(gray)

col2.addWidget(picture_box)

master_layout.addLayout(col1, 20)
master_layout.addLayout(col2, 80)

main_window.setLayout(master_layout)










main_window.show()
App.exec_()
