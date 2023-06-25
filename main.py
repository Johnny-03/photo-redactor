from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog,QLabel,QPushButton,QVBoxLayout,QHBoxLayout,QListWidget
import os 
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import ImageFilter
from PIL import Image
app = QApplication([])
main_win = QWidget()
main_win.resize(700,500)
main_win.setWindowTitle('Easy Editor')
image_main = QLabel('Картинка')
btn_dir = QPushButton('Папка')
file_list = QListWidget()
button_left = QPushButton('Лево')
button_right = QPushButton('Право')
button_mirror = QPushButton('Зеркало')
button_sharp = QPushButton('Резкость')
button_bw = QPushButton('Ч/Б')
row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(file_list)
col2.addWidget(image_main)
row_tools = QHBoxLayout()
row_tools.addWidget(button_left)
row_tools.addWidget(button_right)
row_tools.addWidget(button_mirror)
row_tools.addWidget(button_sharp)
row_tools.addWidget(button_bw)
col2.addLayout(row_tools)
row.addLayout(col1,20)
row.addLayout(col2,80)
main_win.setLayout(row)
main_win.show()
work_dir = ''
def chooseWork_dir():
    global work_dir
    work_dir = QFileDialog.getExistingDirectory()
def filter (files,extensions):
    result = []
    for file in files:
        for ext in extensions:
            if file.endswith(ext):
                result.append(file)
    return result
def finds_files():
    extensions = ['.png','.jpg','.jpeg','.gif','.bmp']
    chooseWork_dir()
    filesname = filter(os.listdir(work_dir),extensions)
    file_list.clear()
    for file in filesname:
        file_list.addItem(file)
btn_dir.clicked.connect(finds_files)
class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modified/'
    def loadImage(self,dir,filename):
        self.dir = dir 
        self.filename = filename
        image_path = os.path.join(dir,filename)
        self.image = Image.open(image_path)
    def do_bw(self):
        self.image =  self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.showImage (image_path)
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.showImage (image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.showImage (image_path)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.showImage (image_path)
    def do_sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.showImage (image_path)
    def saveImage(self):
        path = os.path.join(self.dir,self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path,self.filename)
        self.image.save(image_path)
    def showImage(self,path):
        image_main.hide()
        pixmapimage = QPixmap(path)
        w, h = image_main.width(), image_main.height()
        pixmapimage = pixmapimage.scaled(w, h , Qt.KeepAspectRatio)
        image_main.setPixmap(pixmapimage)
        image_main.show()
def showChosenImage():
    if file_list.currentRow()>=0:
        filename = file_list.currentItem().text()
        workimage.loadImage(work_dir,filename)
        image_path = os.path.join(workimage.dir,workimage.filename)
        workimage.showImage(image_path)
workimage = ImageProcessor()
file_list.currentRowChanged.connect(showChosenImage)
button_bw.clicked.connect(workimage.do_bw)
button_left.clicked.connect(workimage.do_left)
button_right.clicked.connect(workimage.do_right)
button_mirror.clicked.connect(workimage.do_flip)
button_sharp.clicked.connect(workimage.do_sharpen)
app.exec()
        
        

