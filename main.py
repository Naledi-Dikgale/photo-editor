from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QComboBox, QVBoxLayout, QHBoxLayout, QFileDialog, QGridLayout, QSlider, QInputDialog, QSplitter
from PyQt5.QtCore import Qt, QSize, QEvent
import os
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QColor
from PIL import Image, ImageEnhance, ImageFilter

def colorize_icon(icon_path, color):
    pixmap = QPixmap(icon_path)
    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), QColor(color))
    painter.end()
    return QIcon(pixmap)

App = QApplication([])
main_window = QWidget()
main_window.setWindowTitle("Photo Editor")
main_window.resize(800, 600)

# Load QSS file
with open("styles.qss", "r") as file:
    App.setStyleSheet(file.read())

# Add widgets
btn_folder = QPushButton()
btn_folder.setIcon(colorize_icon("icons/folder.svg", "pink"))
btn_folder.setIconSize(QSize(24, 24))
btn_folder.setFixedSize(32, 32)

file_list = QListWidget()

buttons = [
    {"name": "mirror", "icon": "icons/mirror.svg"},
    {"name": "sharpness", "icon": "icons/sharpness.svg"},
    {"name": "brightness", "icon": "icons/brightness.svg"},
    {"name": "contrast", "icon": "icons/contrast.svg"},
    {"name": "saturation", "icon": "icons/saturation.svg"},
    {"name": "blur", "icon": "icons/image.svg"},
    {"name": "rotate", "icon": "icons/rotate.svg"},
    {"name": "gray", "icon": "icons/paint.svg"},
    {"name": "blue", "icon": "icons/paint.svg"},
    {"name": "undo", "icon": "icons/undo.svg"},
    {"name": "save", "icon": "icons/save.svg"}
]

button_widgets = []

for button in buttons:
    btn_layout = QVBoxLayout()
    btn_layout.setContentsMargins(0, 0, 0, 0)
    btn_layout.setSpacing(0)
    btn_widget = QWidget()
    btn = QPushButton()
    btn.setIcon(colorize_icon(button["icon"], "pink"))
    btn.setIconSize(QSize(24, 24))
    btn.setFixedSize(32, 32)
    label = QLabel(button["name"])
    label.setAlignment(Qt.AlignCenter)
    btn_layout.addWidget(btn)
    btn_layout.addWidget(label)
    btn_widget.setLayout(btn_layout)
    button_widgets.append(btn_widget)

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

bottom_right_layout = QVBoxLayout()
image_layout = QHBoxLayout()
image_layout.addWidget(original_picture_box)
image_layout.addWidget(edited_picture_box)
bottom_right_layout.addLayout(image_layout)

bottom_buttons_layout = QHBoxLayout()
bottom_buttons_layout.addWidget(button_widgets[-2])
bottom_buttons_layout.addWidget(button_widgets[-1])  
bottom_right_layout.addLayout(bottom_buttons_layout)

right_layout.addLayout(top_right_layout)
right_layout.addLayout(bottom_right_layout)

# Add button widgets
for btn_widget in button_widgets[:-2]:  
    top_right_layout.addWidget(btn_widget)

# Divide the left and right sides
splitter = QSplitter(Qt.Horizontal)
left_widget = QWidget()
left_widget.setLayout(left_layout)
right_widget = QWidget()
right_widget.setLayout(right_layout)
splitter.addWidget(left_widget)
splitter.addWidget(right_widget)
splitter.setSizes([160, 640])

main_layout.addWidget(splitter)

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
button_widgets[0].findChild(QPushButton).clicked.connect(lambda: main.transformImage("MirrorImage"))
button_widgets[1].findChild(QPushButton).clicked.connect(lambda: main.transformImage("AdjustSharpness"))
button_widgets[2].findChild(QPushButton).clicked.connect(lambda: main.transformImage("AdjustBrightness"))
button_widgets[3].findChild(QPushButton).clicked.connect(lambda: main.transformImage("AdjustContrast"))
button_widgets[4].findChild(QPushButton).clicked.connect(lambda: main.transformImage("AdjustSaturation"))
button_widgets[5].findChild(QPushButton).clicked.connect(lambda: main.transformImage("ApplyBlur"))
button_widgets[6].findChild(QPushButton).clicked.connect(lambda: main.transformImage("RotateImage"))
button_widgets[7].findChild(QPushButton).clicked.connect(lambda: main.transformImage("ConvertToGray"))
button_widgets[8].findChild(QPushButton).clicked.connect(lambda: main.transformImage("ConvertToBlue"))
button_widgets[9].findChild(QPushButton).clicked.connect(lambda: main.transformImage("Undo"))
button_widgets[10].findChild(QPushButton).clicked.connect(lambda: main.transformImage("SaveImage"))

def resizeEvent(event):
    available_width = main_window.width()
    button_width = button_widgets[0].width()
    columns = available_width // button_width
    for i, btn in enumerate(button_widgets[:-2]): 
        row = i // columns
        col = i % columns
        top_right_layout.addWidget(btn, row + 1, col)

main_window.resizeEvent = resizeEvent

main_window.show()
App.exec_()