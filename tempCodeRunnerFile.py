from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QComboBox, QVBoxLayout, QHBoxLayout, QFileDialog, QGridLayout
from PyQt5.QtCore import Qt
import os
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageEnhance, ImageFilter

App = QApplication([])
main_window = QWidget()
main_window.setWindowTitle("Photo Editor")
main_window.resize(800, 600)

# Add widgets
btn_folder = QPushButton("Folder")
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
layout = QGridLayout()

layout.addWidget(btn_folder, 0, 0, 1, 2)
layout.addWidget(file_list, 1, 0, 5, 2)
layout.addWidget(filter_box, 0, 2, 1, 4)
layout.addWidget(btn_left, 1, 2)
layout.addWidget(btn_right, 1, 3)
layout.addWidget(mirror, 1, 4)
layout.addWidget(sharpness, 1, 5)
layout.addWidget(brightness, 2, 2)
layout.addWidget(contrast, 2, 3)
layout.addWidget(saturation, 2, 4)
layout.addWidget(blur, 2, 5)
layout.addWidget(rotate, 3, 2)
layout.addWidget(crop, 3, 3)
layout.addWidget(gray, 3, 4)
layout.addWidget(picture_box, 1, 6, 5, 6)

main_window.setLayout(layout)

# Apply theme
App.setStyleSheet("""
    QWidget {
        background-color: white;
        color: blue;
    }
    QPushButton {
        background-color: blue;
        color: black;
        border: 1px solid blue;
    }
    QListWidget {
        background-color: white;
        color: blue;
        border: 1px solid blue;
    }
    QComboBox {
        background-color: white;
        color: blue;
        border: 1px solid blue;
    }
    QLabel {
        background-color: white;
        color: blue;
    }
""")

# Functionality
working_directory = ""

# filter files
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
    print(f"Selected directory: {working_directory}") 
    extensions = [".jpg", ".jpeg", ".png", ".gif", ".svg"]
    filenames = filter(os.listdir(working_directory), extensions)
    print(f"Filtered filenames: {filenames}") #debug
    file_list.clear()
    for file in filenames:
        file_list.addItem(file)

class Editor:
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
        print(f"Loaded image: {fullname}")

    def SaveImage(self):
        path = os.path.join(working_directory, self.save_folder)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)
        print(f"Saved image: {fullname}")
        return fullname

    def Show_image(self, path):
        picture_box.hide()
        image = QPixmap(path)
        w, h = picture_box.width(), picture_box.height()
        image = image.scaled(w, h, Qt.KeepAspectRatio)
        picture_box.setPixmap(image)
        picture_box.show()
        print(f"Displayed image: {path}")

    def RotateLeft(self):
        if self.image:
            self.image = self.image.rotate(90, expand=True)
            path = self.SaveImage()
            self.Show_image(path)

    def RotateRight(self):
        if self.image:
            self.image = self.image.rotate(-90, expand=True)
            path = self.SaveImage()
            self.Show_image(path)

    def MirrorImage(self):
        if self.image:
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            path = self.SaveImage()
            self.Show_image(path)

    def AdjustSharpness(self):
        if self.image:
            enhancer = ImageEnhance.Sharpness(self.image)
            self.image = enhancer.enhance(2.0)  # Increase sharpness
            path = self.SaveImage()
            self.Show_image(path)

    def AdjustBrightness(self):
        if self.image:
            enhancer = ImageEnhance.Brightness(self.image)
            self.image = enhancer.enhance(1.5)  # Increase brightness
            path = self.SaveImage()
            self.Show_image(path)

    def AdjustContrast(self):
        if self.image:
            enhancer = ImageEnhance.Contrast(self.image)
            self.image = enhancer.enhance(1.5)  # Increase contrast
            path = self.SaveImage()
            self.Show_image(path)

    def AdjustSaturation(self):
        if self.image:
            enhancer = ImageEnhance.Color(self.image)
            self.image = enhancer.enhance(1.5)  # Increase saturation
            path = self.SaveImage()
            self.Show_image(path)

    def ApplyBlur(self):
        if self.image:
            self.image = self.image.filter(ImageFilter.BLUR)
            path = self.SaveImage()
            self.Show_image(path)

    def RotateImage(self):
        if self.image:
            self.image = self.image.rotate(45, expand=True)
            path = self.SaveImage()
            self.Show_image(path)

    def CropImage(self):
        if self.image:
            width, height = self.image.size
            left = width / 4
            top = height / 4
            right = 3 * width / 4
            bottom = 3 * height / 4
            self.image = self.image.crop((left, top, right, bottom))
            path = self.SaveImage()
            self.Show_image(path)

    def ConvertToGray(self):
        if self.image:
            self.image = self.image.convert("L")
            path = self.SaveImage()
            self.Show_image(path)

def displayImage():
    if file_list.currentRow() >= 0:
        filename = file_list.currentItem().text()
        main.LoadImage(filename)
        main.Show_image(os.path.join(working_directory, main.filename))

main = Editor()

btn_folder.clicked.connect(get_current_directory)
file_list.currentRowChanged.connect(displayImage)
btn_left.clicked.connect(main.RotateLeft)
btn_right.clicked.connect(main.RotateRight)
mirror.clicked.connect(main.MirrorImage)
sharpness.clicked.connect(main.AdjustSharpness)
brightness.clicked.connect(main.AdjustBrightness)
contrast.clicked.connect(main.AdjustContrast)
saturation.clicked.connect(main.AdjustSaturation)
blur.clicked.connect(main.ApplyBlur)
rotate.clicked.connect(main.RotateImage)
crop.clicked.connect(main.CropImage)
gray.clicked.connect(main.ConvertToGray)

main_window.show()
App.exec_()