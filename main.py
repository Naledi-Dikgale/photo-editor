from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QComboBox, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5.QtCore import Qt
import os
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageEnhance, ImageFilter 

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

# Functionality
working_directory = ""

# filter filex
def filter(files, extensions):
    results = []
    for file in files:
        for extension in extensions:
            if file.endswith(extension):
                results.append(file)
    return results

# get current directory
def get_current_directory():
    global working_directory
    working_directory = QFileDialog.getExistingDirectory()
    extensions = [".jpg", ".jpeg", ".png", ".gif", "svg"]
    filenames = filter(os.listdir(working_directory), extensions)
    file_list.clear()
    for file in filenames:
        file_list.addItem(filenames)


class Editor[]:
  def __init__(self):
    self.image = None
    self.original = None
    self.filename = None
    self.save_folder = "edits"

def LoadImage(self, filename):
    self.filename = filename
    fullname = os.path.join(working_directory, filename)
    self.image = Image.open(fullname)
    self.original = self.image.copy()

def SaveImage(self):
  path = os.path.join(working_directory, self.save_folder)
  if not(os.path.exists(path) or os.path.isdir(path)):
    os.mkdir(path)

  fullname = os.path.join(path, self.filename)
  self.image.save(fullname)

def Show_image(self, path):
  picture_box.hide()
  image = QPixmap(path)
  w, h = picture_box.width(), picture_box.height()
  image = image.scaled(w, h, Qt.KeepAspectRatio)
  picture_box.setPixmap(image)
  picture_box.show()


def displayImage():
  if file_list.currentItem() >= 0:
    filename = file_list.currentItem().text()
    main.LoadImage(filename)
    main.Show_image(os.path.join(working_directory, main.filename))
    

main = Editor()

btn_folder.clicked.connect(get_current_directory)
file_list.currentRowChanged.connect(displayImage)

main_window.show()
App.exec_()
