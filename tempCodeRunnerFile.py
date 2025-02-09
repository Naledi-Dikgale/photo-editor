from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QComboBox, QVBoxLayout, QHBoxLayout, QFileDialog, QGridLayout, QSlider, QInputDialog
from PyQt5.QtCore import Qt, QSize
import os
from PyQt5.QtGui import QPixmap, QIcon
from PIL import Image, ImageEnhance, ImageFilter

App = QApplication([])
main_window = QWidget()
main_window.setWindowTitle("Photo Editor")
main_window.resize(800, 600)

# Load QSS file
with open("styles.qss", "r") as file:
    App.setStyleSheet(file.read())

# Add widgets
btn_folder = QPushButton()
btn_folder.setIcon(QIcon("icons/folder.svg"))
btn_folder.setIconSize(QSize(24, 24))
btn_folder.setFixedSize(32, 32)

file_list = QListWidget()

mirror = QPushButton()
mirror.setIcon(QIcon("icons/mirror.svg"))
mirror.setIconSize(QSize(24, 24))
mirror.setFixedSize(32, 32)

sharpness = QPushButton()
sharpness.setIcon(QIcon("icons/sharpness.svg"))
sharpness.setIconSize(QSize(24, 24))
sharpness.setFixedSize(32, 32)

brightness = QPushButton()
brightness.setIcon(QIcon("icons/brightness.svg"))
brightness.setIconSize(QSize(24, 24))
brightness.setFixedSize(32, 32)

contrast = QPushButton()
contrast.setIcon(QIcon("icons/contrast.svg"))
contrast.setIconSize(QSize(24, 24))
contrast.setFixedSize(32, 32)

saturation = QPushButton()
saturation.setIcon(QIcon("icons/saturation.svg"))
saturation.setIconSize(QSize(24, 24))
saturation.setFixedSize(32, 32)

blur = QPushButton()
blur.setIcon(QIcon("icons/image.svg"))
blur.setIconSize(QSize(24, 24))
blur.setFixedSize(32, 32)

rotate = QPushButton()
rotate.setIcon(QIcon("icons/rotate.svg"))
rotate.setIconSize(QSize(24, 24))
rotate.setFixedSize(32, 32)

gray = QPushButton()
gray.setIcon(QIcon("icons/paint.svg"))
gray.setIconSize(QSize(24, 24))
gray.setFixedSize(32, 32)

blue = QPushButton()
blue.setIcon(QIcon("icons/paint.svg"))
blue.setIconSize(QSize(24, 24))
blue.setFixedSize(32, 32)

undo = QPushButton()
undo.setIcon(QIcon("icons/undo.svg"))
undo.setIconSize(QSize(24, 24))
undo.setFixedSize(32, 32)

save = QPushButton()
save.setIcon(QIcon("icons/save.svg"))
save.setIconSize(QSize(24, 24))
save.setFixedSize(32, 32)

# Dropdown menu
filter_box = QComboBox()
filter_box.addItem("Original")
filter_box.addItem("Mirror")
filter_box.addItem("Sharpness")
filter_box.addItem("Brightness")
filter_box.addItem("Contrast")
filter_box.addItem("Saturation")
filter_box.addItem("Blur")
filter_box.addItem("Rotate")
filter_box.addItem("Gray")
filter_box.addItem("Blue")

original_picture_box = QLabel("Original Picture")
edited_picture_box = QLabel("Edited Picture")

# Layout
main_layout = QHBoxLayout()

left_layout = QVBoxLayout()
left_layout.addWidget(btn_folder)
left_layout.addWidget(file_list)

right_layout = QVBoxLayout()

top_right_layout = QGridLayout()
top_right_layout.addWidget(filter_box, 0, 0, 1, 4)
top_right_layout.addWidget(mirror, 1, 0)
top_right_layout.addWidget(sharpness, 1, 1)
top_right_layout.addWidget(brightness, 1, 2)
top_right_layout.addWidget(contrast, 1, 3)
top_right_layout.addWidget(saturation, 2, 0)
top_right_layout.addWidget(blur, 2, 1)
top_right_layout.addWidget(rotate, 2, 2)
top_right_layout.addWidget(gray, 2, 3)
top_right_layout.addWidget(blue, 3, 0)

bottom_right_layout = QVBoxLayout()
image_layout = QHBoxLayout()
image_layout.addWidget(original_picture_box)
image_layout.addWidget(edited_picture_box)
bottom_right_layout.addLayout(image_layout)

bottom_buttons_layout = QHBoxLayout()
bottom_buttons_layout.addWidget(undo)
bottom_buttons_layout.addWidget(save)
bottom_right_layout.addLayout(bottom_buttons_layout)

right_layout.addLayout(top_right_layout)
right_layout.addLayout(bottom_right_layout)

main_layout.addLayout(left_layout, 1)
main_layout.addLayout(right_layout, 4)

main_window.setLayout(main_layout)

# Functionality
working_directory = ""
history = []

# filter files
def filter(files, extensions):
    results = []
    for file in files:
        for extension in extensions:
            if file.endswith(extension):
                results.append(file)
    return results

# current directory
def get_current_directory():
    global working_directory
    working_directory = QFileDialog.getExistingDirectory()
    print(f"Selected directory: {working_directory}") 
    extensions = [".jpg", ".jpeg", ".png", ".gif", ".svg"]
    filenames = filter(os.listdir(working_directory), extensions)
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
        history.clear()
        history.append(self.image.copy())
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
        original_picture_box.hide()
        edited_picture_box.hide()
        original_image = QPixmap(os.path.join(working_directory, self.filename))
        edited_image = QPixmap(path)
        w, h = original_picture_box.width(), original_picture_box.height()
        original_image = original_image.scaled(w, h, Qt.KeepAspectRatio)
        edited_image = edited_image.scaled(w, h, Qt.KeepAspectRatio)
        original_picture_box.setPixmap(original_image)
        edited_picture_box.setPixmap(edited_image)
        original_picture_box.show()
        edited_picture_box.show()
        print(f"Displayed images: original - {os.path.join(working_directory, self.filename)}, edited - {path}")

    def RotateLeft(self):
        if self.image:
            self.image = self.image.rotate(90, expand=True)
            history.append(self.image.copy())
            path = self.SaveImage()
            self.Show_image(path)

    def RotateRight(self):
        if self.image:
            self.image = self.image.rotate(-90, expand=True)
            history.append(self.image.copy())
            path = self.SaveImage()
            self.Show_image(path)

    def MirrorImage(self):
        if self.image:
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            history.append(self.image.copy())
            path = self.SaveImage()
            self.Show_image(path)

    def AdjustSharpness(self, value):
        if self.image:
            enhancer = ImageEnhance.Sharpness(self.image)
            self.image = enhancer.enhance(value)
            history.append(self.image.copy())
            path = self.SaveImage()
            self.Show_image(path)

    def AdjustBrightness(self, value):
        if self.image:
            enhancer = ImageEnhance.Brightness(self.image)
            self.image = enhancer.enhance(value)
            history.append(self.image.copy())
            path = self.SaveImage()
            self.Show_image(path)

    def AdjustContrast(self, value):
        if self.image:
            enhancer = ImageEnhance.Contrast(self.image)
            self.image = enhancer.enhance(value)
            history.append(self.image.copy())
            path = self.SaveImage()
            self.Show_image(path)

    def AdjustSaturation(self, value):
        if self.image:
            enhancer = ImageEnhance.Color(self.image)
            self.image = enhancer.enhance(value)
            history.append(self.image.copy())
            path = self.SaveImage()
            self.Show_image(path)

    def ApplyBlur(self, value):
        if self.image:
            self.image = self.image.filter(ImageFilter.GaussianBlur(value))
            history.append(self.image.copy())
            path = self.SaveImage()
            self.Show_image(path)

    def RotateImage(self, value):
        if self.image:
            self.image = self.image.rotate(value, expand=True)
            history.append(self.image.copy())
            path = self.SaveImage()
            self.Show_image(path)

    def ConvertToGray(self):
        if self.image:
            self.image = self.image.convert("L")
            history.append(self.image.copy())
            path = self.SaveImage()
            self.Show_image(path)

    def ConvertToBlue(self):
        if self.image:
            self.image = self.image.convert("RGB")
            r, g, b = self.image.split()
            self.image = Image.merge("RGB", (b, g, r))
            history.append(self.image.copy())
            path = self.SaveImage()
            self.Show_image(path)

    def Undo(self):
        if len(history) > 1:
            history.pop()
            self.image = history[-1].copy()
            path = self.SaveImage()
            self.Show_image(path)

    def transformImage(self, action):
        actions = {
            "MirrorImage": self.MirrorImage,
            "AdjustSharpness": lambda: self.AdjustSharpness(5),
            "AdjustBrightness": lambda: self.AdjustBrightness(3),
            "AdjustContrast": lambda: self.AdjustContrast(5),
            "AdjustSaturation": lambda: self.AdjustSaturation(5),
            "ApplyBlur": lambda: self.ApplyBlur(4),
            "RotateImage": lambda: self.RotateImage(90),
            "ConvertToGray": self.ConvertToGray,
            "ConvertToBlue": self.ConvertToBlue,
            "Undo": self.Undo,
            "SaveImage": self.SaveImage
        }
        if action in actions:
            actions[action]()

def displayImage():
    if file_list.currentRow() >= 0:
        filename = file_list.currentItem().text()
        main.LoadImage(filename)
        main.Show_image(os.path.join(working_directory, main.filename))

main = Editor()

btn_folder.clicked.connect(get_current_directory)
file_list.currentRowChanged.connect(displayImage)
mirror.clicked.connect(lambda: main.transformImage("MirrorImage"))
sharpness.clicked.connect(lambda: main.transformImage("AdjustSharpness"))
brightness.clicked.connect(lambda: main.transformImage("AdjustBrightness"))
contrast.clicked.connect(lambda: main.transformImage("AdjustContrast"))
saturation.clicked.connect(lambda: main.transformImage("AdjustSaturation"))
blur.clicked.connect(lambda: main.transformImage("ApplyBlur"))
rotate.clicked.connect(lambda: main.transformImage("RotateImage"))
gray.clicked.connect(lambda: main.transformImage("ConvertToGray"))
blue.clicked.connect(lambda: main.transformImage("ConvertToBlue"))
undo.clicked.connect(lambda: main.transformImage("Undo"))
save.clicked.connect(lambda: main.transformImage("SaveImage"))

main_window.show()
App.exec_()