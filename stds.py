import datetime
import os.path
import re
import subprocess
import threading
import time
from threading import Thread

import PIL.Image
import keyboard
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from send2trash import send2trash

accentColor=[200,200,200]
accentColor1=[(255+i)//2 for i in accentColor]
alpha=1
fileMenus=[[
    "用记事本打开",
    "notepad <s>",
    "assets/ico/txt.png"
]]
def setfileMenu(fm:list[list]):
    global fileMenus
    fileMensu=fm
def setAlpha(boolean):
    global alpha
    alpha=2-int(bool(boolean))
def setAC(l: list[int:3]):
    global accentColor,accentColor1
    accentColor=l
    accentColor1=[(255+i)//2 for i in accentColor]


class Logger(Thread):
    def __init__(self):
        super().__init__()
        self.event = threading.Event()
        self.activate=True
        lfp="logs"
        lf=f".\\{lfp}\\{self.nowTime().replace(':','').replace('-','')}.log"
        #lf="logs/1.log"
        self.text=""
        if(os.path.exists(lfp)):
            if(os.path.isdir(lfp)):
                self.file=open(lf,"a")
            else:
                showError("无法创建日志文件，已关闭日志")
        else:
            os.makedirs(lfp)
            self.file=open(lf,"a")
    def nowTime(self):return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')
    def info(self,txt):
        if(self.activate):
            log=f"[{self.nowTime()} Info] >> {txt}"
            print(log)
            self.text+=log+"\n"
    def error(self,txt):
        if(self.activate):
            log=f"[{self.nowTime()} Error] >> {txt}"
            print(log)
            self.text+=log+"\n"
    def enable(self,boolean:bool):
        self.activate=boolean
    def save(self):
        if(self.activate):
            self.file.write(self.text)
            self.file.flush()
        self.text=""
    def close(self):
        if(self.activate):
            self.info("Disabling logger")
            self.save()
            self.activate=False
        self.file.close()
    def run(self):
        while self.activate:
            for i in range(100):
                time.sleep(0.1*self.activate)
            self.save()
logger=Logger()
logger.start()

def EXIT():
    global logger
    logger.close()
    exit()
class Slider(QSlider):
    def __init__(self, *args):
        super().__init__(*args)
        # 设置滑动条的样式，使轨道和滑块半透明
        self.setStyleSheet(f"""
            QSlider::groove:vertical {{
                background: none; /* 轨道半透明 */
                width: 20px; /* 轨道宽度 */
                border: 1px solid rgb(204, 204, 204);
            }}
            QSlider::handle:vertical {{
                background: rgba(204,204,204, 1); /* 滑块半透明 */
                border: none; /* 滑块边框设置为无 */
                width: 20px; /* 滑块宽度 */
                height: 40px; /* 滑块高度 */
            }}
        """)
        self.setRange(0, 100)  # 设置滑动条的范围
        self.setInvertedAppearance(True)
        self.setValue(0)  # 设置滑动条的初始值
qf=QFont("SimHei",10)
def setFont(name:str,italic=False,bold=False):
    global qf
    qf=QFont(name,10)
    qf.setItalic(italic)
    qf.setBold(bold)

def showError(s:str,parent=None):
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setText(s)
    msg_box.setWindowTitle("报错")
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()

def showInfo(s:str,parent=None):
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setText(s)
    msg_box.setWindowTitle("信息")
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()

def AskIf(title:str,ask:str,parent=None):
    confirm = QMessageBox.question(
        parent,
        title,
        ask,
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )
    if confirm == QMessageBox.Yes:
        return True
    else:
        return False
class Bar(QPushButton):
    def __init__(self,*args):
        super().__init__(*args)
        self.setFixedSize(150,30)
        self.set(self.text())
        self.setFont(qf)
        self.tqdm=0
        self.setStyleSheet(f"""
        QPushButton {{
        border: none; /* 白色边框 */
        background-color: rgba(255,255,255,{alpha*0.5});  /* 原始背景颜色 */
        color: #000000;            /* 文字颜色 */
    }}
    QPushButton:hover {{
        background-color:rgba({accentColor1[0]},{accentColor1[1]},{accentColor1[2]},{alpha*0.5})
    }}
    QPushButton:pressed {{
        background-color: rgba({accentColor[0]},{accentColor[1]},{accentColor[2]},{alpha*0.5}); /* 按钮被按下时的背景颜色 */
    }}
        """)
        self.isclicked=False
        self.clicked.connect(self.c)

        self.quitButton=QPushButton(self)
        self.quitButton.setIcon(QIcon("assets/ico/ui/x.png"))
        self.quitButton.setFont(qf)
        self.quitButton.setStyleSheet(f"""
        QPushButton {{
        border: none;
        background-color: none;  /* 原始背景颜色 */
    }}
    QPushButton:hover {{
        background-color:rgba(255,0,0,{alpha*0.5}); /* 鼠标悬停时的背景颜色 */
    }}
    QPushButton:pressed {{
        background-color: rgba(200,0,0,{alpha*0.5}); /* 按钮被按下时的背景颜色 */
    }}""")
        self.quitButton.setGeometry(125,5,20,20)
        self.quitButton.clicked.connect(self.q)
        self.isquited=False

        self.setToolTip(self.rawText)

    def c(self):
        self.isclicked=True
        self.setStyleSheet(f"""
        QPushButton {{
        border: 1px solid rgb({accentColor[0]-50},{accentColor[1]-50},{accentColor[2]-50}); /* 白色边框 */
        background-color: rgba({accentColor[0]},{accentColor[1]},{accentColor[2]},{alpha*0.5});  /* 原始背景颜色 */
        color: #000000;            /* 文字颜色 */
    }}""")
    def q(self):
        self.isquited=True
        self.hide()
    def unc(self):
        self.isclicked=False
        self.setStyleSheet(f"""
        QPushButton {{
        border:none; /* 白色边框 */
        background-color: rgba(255,255,255,{alpha*0.5});  /* 原始背景颜色 */
        color: #000000;            /* 文字颜色 */
    }}
    QPushButton:hover {{
        background-color:rgba({accentColor1[0]},{accentColor1[1]},{accentColor1[2]},{alpha*0.5})
    }}
    QPushButton:pressed {{
        background-color: rgba({accentColor[0]},{accentColor[1]},{accentColor[2]},{alpha*0.5}); /* 按钮被按下时的背景颜色 */
    }}
        """)

    def set(self, s: str):
        #设置路径
        self.rawText = os.path.normpath(s)
        parts = re.split(r'[/\\]', self.rawText)
        fm = QFontMetrics(qf)
        space = fm.width(" ")
        if len(parts) == 2 and parts[1] == '' and parts[0]:
            self.setText(parts[0]+" "*(15//space))
        else:
            self.setText(parts[-1]+" "*(15//space))

class Icon:
    def __init__(self):
        self.dict={}
        if(1):
            self.add_("apk","c","class","cpp","cs","css","exe","file","jar","java","js","json")
            self.add("bat","bat","cmd","com")
            self.add("folder","*folder")
            self.add("audio","mp3","wav","flac","aac","ogg","mid","midi")
            self.add("html","html","htm")
            self.add("pic","png","jpg","jpeg","bmp","gif","tiff","webp","svg")
            self.add("py","py","pyc","pyd","pyi","pyz","pyo","pys")
            self.add("sb","sb2","sb3")
            self.add("txt","txt","ini","log")
            self.add("video","mp4","mov","avi","wmv","mkv","flv")
            self.add("yml","yaml","yml")
            self.add("zip","zip","rar","gz","7z","tar")

            self.add("ui/settings","*settings")
            self.add("ui/add","*add")


    def add(self,*args):
        l=QPixmap("assets/ico/"+args[0]+".png")
        for i in args[1:]:
            self.dict.update({i:l.scaled(20,20)})

    def add_(self,*args):
        for i in args:
            l=QPixmap("assets/ico/"+i+".png")
            self.dict.update({i:l.scaled(20,20)})

    def get(self,itm:str):return self.dict.get(itm) if self.dict.get(itm) else self.dict.get("file")

icons = Icon()

def setIcon():
    try:
        return Icon()
    except Exception as e:
        showError("图标文件缺失。请重新安装程序")
        EXIT()

class Button(QPushButton):
    def __init__(self,*args):
        super().__init__(*args)
        self.resize(20,20)
        self.setFont(qf)
        self.setStyleSheet(f"""
        QPushButton {{
        border: none; /* 白色边框 */
        background-color: none;  /* 原始背景颜色 */
        color: #000000;            /* 文字颜色 */
        text-align: center; 
    }}
    QPushButton:hover {{
        background-color:rgba({accentColor[0]-25*(2-alpha)},{accentColor[1]-25*(2-alpha)},{accentColor[2]-25*(2-alpha)},{alpha*0.5})
    }}
    QPushButton:pressed {{
        background-color: rgba({accentColor[0]-75*(2-alpha)},{accentColor[1]-75*(2-alpha)},{accentColor[2]-75*(2-alpha)},{alpha*0.5}); /* 按钮被按下时的背景颜色 */
    }}
        """)
class LButton(QPushButton):
    def __init__(self,*args):
        super().__init__(*args)
        self.resize(20,20)
        self.setFont(qf)
        self.setStyleSheet(f"""
        QPushButton {{
        border: none; /* 白色边框 */
        background-color: none;  /* 原始背景颜色 */
        color: #000000;            /* 文字颜色 */
        text-align: left; 
    }}
    QPushButton:hover {{
        background-color:rgba({accentColor[0]-25*(2-alpha)},{accentColor[1]-25*(2-alpha)},{accentColor[2]-25*(2-alpha)},{alpha*0.5})
    }}
    QPushButton:pressed {{
        background-color: rgba({accentColor[0]-75*(2-alpha)},{accentColor[1]-75*(2-alpha)},{accentColor[2]-75*(2-alpha)},{alpha*0.5}); /* 按钮被按下时的背景颜色 */
    }}
        """)



class fileLine(QPushButton):
    def __init__(self,*args):
        super().__init__(*args)
        self.setFont(qf)
        self.master=self.parent().getMaster()
        self.setGeometry(0,90,960,30)
        self.oldY=self.y()
        self.absname=re.sub(r'[\\/]{2,}', '/', self.text())
        self.name=os.path.basename(self.absname)
        if(os.path.isfile(self.absname)):
            self.type = os.path.splitext(self.name)[-1].replace(".","").lower()
        else:self.type="*folder"

        self.unc()
        self.clicked.connect(self.c)
        self.deleted=False

        w=self.width()
        self.setIco(self.master.icons.get(self.type))
        self.icoLabel.setFont(qf)
        self.icoLabel.setGeometry(35,5,20,20)
        self.icoLabel.setStyleSheet("background-color:none")

        self.nameLabel=QLabel(self.name,self)
        self.nameLabel.setFont(qf)
        self.nameLabel.setStyleSheet(f"background-color:none;color:{('#000000','#'+'7'*6)[os.stat(self.absname).st_file_attributes&2>0]}")
        self.nameLabel.setGeometry(75,0,w,30)

        self.infoButton = Button(self)
        self.infoButton.setIcon(QIcon("assets/ico/ui/info.png"))
        self.infoButton.move(w-45,5)
        self.infoButton.setToolTip("信息")

        self.delButton=QPushButton(self)
        self.delButton.setFont(qf)
        self.delButton.setIcon(QIcon("assets/ico/ui/x.png"))
        self.delButton.setToolTip("删除")
        self.delButton.setStyleSheet(f"""
        QPushButton {{
        border: none;
        background-color: none;  /* 原始背景颜色 */
        text-align: center; 
    }}
    QPushButton:hover {{
        background-color:rgba(255,0,0,{alpha*0.5}); /* 鼠标悬停时的背景颜色 */
    }}
    QPushButton:pressed {{
        background-color: rgba(200,0,0,{alpha*0.5}); /* 按钮被按下时的背景颜色 */
    }}""")
        self.delButton.setGeometry(w-70,5,20,20)
        self.delButton.clicked.connect(self.dele)

        self.renameButton = Button(self)
        self.renameButton.setIcon(QIcon("assets/ico/ui/rename.png"))
        self.renameButton.move(w-95,5)
        self.renameButton.clicked.connect(self.rename)
        self.renameButton.setToolTip("重命名")

        self.execButton = Button(self)
        self.execButton.setIcon(QIcon("assets/ico/ui/exec.png"))
        self.execButton.move(w-120,5)
        self.execButton.clicked.connect(self.exec)
        self.execButton.setToolTip("运行")

        self.ToolTip_ed = 0

    def rename(self):
        logger.info("Renaming "+self.absname)
        qd = renameDialog()
        qd.exec_()
        if qd.accepted:
            filename = qd.lineEdit.text()
            if(qd.is_accepted and filename):
                if(legitFN(filename) and not (os.path.exists(filename))):
                    try:
                        os.rename(self.absname,os.path.dirname(self.absname)+"\\"+filename)
                        logger.info("Successfully renamed "+self.absname+" to "+filename)
                    except Exception as e:
                        logger.info(f"Failed: {e}")
                else:
                    showError("无效文件名，取消重命名")
                    logger.info("Cancelled: invalid filename")
            else:
                logger.info("Cancelled: User")
    def enterEvent(self, a0):
        if(self.ToolTip_ed):return
        try:
            if(self.type=="*folder"):
                tt=f"""文件夹名称: {self.name}
创建时间: {datetime.datetime.fromtimestamp(os.path.getctime(self.absname)).strftime('%Y-%m-%d %H:%M:%S')}
"""
                fl = ", ".join(i for i in os.listdir(self.absname))
                if(fl):
                    if(fl.__len__()>50):fl=fl[:50]+"..."
                    tt+="文件: "+fl
                else:
                    tt+="空文件夹"
                self.setToolTip(tt)
            elif(self.type=="txt" or self.type=="log"):
                self.setToolTip(f"""文件名: {self.name}
文件大小: {os.path.getsize(self.absname)}字节
创建时间: {datetime.datetime.fromtimestamp(os.path.getctime(self.absname)).strftime('%Y-%m-%d %H:%M:%S')}
文件格式: {self.type}
文件内容: 
{open(self.absname).read(256)}""")
            elif(self.type in ("png","jpg","jpeg","bmp","tiff","webp")):
                self.setToolTip(f"""文件名: {self.name}
文件大小: {os.path.getsize(self.absname)}字节
创建时间: {datetime.datetime.fromtimestamp(os.path.getctime(self.absname)).strftime('%Y-%m-%d %H:%M:%S')}
文件格式: {self.type}
分辨率: {PIL.Image.open(self.absname).size}""")
            else:
                self.setToolTip(f"""文件名: {self.name}
文件大小: {os.path.getsize(self.absname)}字节
创建时间: {datetime.datetime.fromtimestamp(os.path.getctime(self.absname)).strftime('%Y-%m-%d %H:%M:%S')}
文件格式: {self.type}""")
        except:self.setToolTip(f"""文件名: {self.name}
文件大小: {os.path.getsize(self.absname)}字节
创建时间: {datetime.datetime.fromtimestamp(os.path.getctime(self.absname)).strftime('%Y-%m-%d %H:%M:%S')}
文件格式: {self.type.replace("*folder",'文件夹')}
文件详细信息获取失败！""")
        self.ToolTip_ed=1
    def dele(self):
        try:
            send2trash(self.absname)
            logger.info(f"Deleted {self.absname}")
            self.deleted=True
            self.hide()
        except Exception as e:
            showError(f"删除失败！{e}\n文件名:{self.absname}")
            print(e)
    def cdele(self):
        try:
            os.remove(self.absname)
            logger.info(f"Completely deleted {self.absname}")
            self.deleted=True
            self.hide()
        except Exception as e:
            showError(f"删除失败！{e}\n文件名:{self.absname}")
            print(e)


    def exec(self):
        self.master.executeFile(self)

    def mouseDoubleClickEvent(self, a0):
        self.unc()
        self.exec()


    def c(self):
        if(self.isclicked):self.unc()
        else:self.normal_c()
    def normal_c(self):
        self.isclicked=True
        self.setText("✔")
        self.setStyleSheet(f"""
        QPushButton {{
        border: 1px solid rgb({accentColor[0]-50},{accentColor[1]-50},{accentColor[2]-50}); /* 白色边框 */
        background-color: rgba({accentColor[0]},{accentColor[1]},{accentColor[2]},{alpha*0.5});  /* 原始背景颜色 */
        color: #000000;            /* 文字颜色 */
        text-align: left; 
    }}""")

    def unc(self):
        self.isclicked=False
        self.setText("o")
        self.setStyleSheet(f"""
        QPushButton {{
        border:none; /* 白色边框 */
        background-color: rgba(255,255,255,{alpha*0.5});  /* 原始背景颜色 */
        color: #000000;            /* 文字颜色 */
        text-align: left; 
    }}
    QPushButton:hover {{
        background-color:rgba({accentColor1[0]},{accentColor1[1]},{accentColor1[2]},{alpha*0.5})
    }}
    QPushButton:pressed {{
        background-color: rgba({accentColor[0]},{accentColor[1]},{accentColor[2]},{alpha*0.5}); /* 按钮被按下时的背景颜色 */
    }}
        """)

    def moveEvent(self, a0):
        if(self.oldY>=60 and self.y()<=60):self.move(0,-31)
        if(self.oldY<=-30 and self.y()>=-30):self.move(0,61)
        self.oldY=self.y()
        super().moveEvent(a0)

    def setIco(self,ico:QPixmap):
        self.icoLabel=QLabel(self)
        self.icoLabel.setPixmap(ico)
        self.icoLabel.move(35,5)
        self.icoLabel.setStyleSheet("background-color:none")
    def resizeEvent(self, a0):
        w=self.width()
        self.infoButton.move(w-45,5)
        self.delButton.setGeometry(w-70,5,20,20)
        self.renameButton.move(w-95,5)
        self.nameLabel.setGeometry(75,0,w,30)
        self.execButton.move(w-120,5)
        super().resizeEvent(a0)

    def keyPressEvent(self, a0):
        if(keyboard.is_pressed("ctrl")):
            if(a0.key()==Qt.Key_M):
                self.rename()
        super().keyPressEvent(a0)

class renameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    def initUI(self):
        self.is_accepted=0
        self.lineEdit = QLineEdit(self)
        self.lineEdit.returnPressed.connect(self.on_accepted)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout = QVBoxLayout()
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
        self.buttonBox.accepted.connect(self.on_accepted)
        self.buttonBox.rejected.connect(self.on_rejected)
        self.setWindowTitle("重命名......")
    def on_rejected(self):
        self.is_accepted=0
        filename = self.lineEdit.text()
        self.close()
        return self.is_accepted,filename
    def on_accepted(self):
        self.is_accepted=1
        filename = self.lineEdit.text()
        self.close()
        return self.is_accepted, filename

class newFileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    def initUI(self):
        # 创建两个复选框，用于选择文件或文件夹
        self.is_accepted=0
        self.checkboxFile = QCheckBox("文件", self)
        self.checkboxFolder = QCheckBox("文件夹", self)
        self.checkboxFile.setChecked(True)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.returnPressed.connect(self.on_accepted)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        layout = QVBoxLayout()
        layout.addWidget(self.checkboxFile)
        layout.addWidget(self.checkboxFolder)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)
        self.checkboxFile.stateChanged.connect(lambda checked: self.checkboxFolder.setChecked(not checked))
        self.checkboxFolder.stateChanged.connect(lambda checked: self.checkboxFile.setChecked(not checked))
        self.buttonBox.accepted.connect(self.on_accepted)
        self.buttonBox.rejected.connect(self.on_rejected)
        self.setWindowTitle("创建文件......")
    def on_rejected(self):
        self.is_accepted=0
        # 获取选择和文件名
        choice = "file" if self.checkboxFile.isChecked() else "*folder"
        filename = self.lineEdit.text()
        self.close()
        return self.is_accepted,choice, filename
    def on_accepted(self):
        self.is_accepted=1
        # 获取选择和文件名
        choice = "file" if self.checkboxFile.isChecked() else "*folder"
        filename = self.lineEdit.text()
        self.close()
        return self.is_accepted,choice, filename
def legitFN(filename):
    invalid_chars = r'[<>:"/\\|?*\x00-\x1F]'
    reserved_names = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
                      'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
    if re.search(invalid_chars, filename):
        return False
    if filename.upper() in reserved_names:
        return False
    if filename.startswith(' ') or filename.endswith(' '):
        return False
    if len(filename) > 255:
        return False
    if '  ' in filename:
        return False
    return True
class cBar(QLabel):
    def __init__(self,*args):
        super().__init__(*args)
        self.master=self.parent().getMaster()

        self.selectButton=LButton(self)
        self.selectButton.setGeometry(0,5,20,20)
        self.selectButton.setText("o")
        self.selectButton.clicked.connect(self.select)

        self.orderButton=LButton(self)
        self.orderButton.setGeometry(35,0,200,30)
        self.orderButton.setText("按照文件名 A-Z")
        self.orderButton.setToolTip("按照字典法排序(文件夹优先)")
        self.orderButton.clicked.connect(self.order)

        w=self.width()
        #+文件
        self.addFileButton = Button(self)
        self.addFileButton.setIcon(QIcon("assets/ico/ui/add.png"))
        self.addFileButton.setGeometry(w-30,30,30,30)
        self.addFileButton.setToolTip("新建文件......")
        self.addFileButton.clicked.connect(self.newFile)
        #共xxx，已选中xxxx
        self.selectedLabel = QLabel(f"0/{self.master.files.__len__()}",self)
        self.selectedLabel.setStyleSheet("background-color:none")
        self.selectedLabel.setFont(qf)
        self.metrics = QFontMetrics(qf)
        self.setSelectedFile(0)
        #↑
        self.upButton = Button("↑",self)
        self.upButton.setGeometry(w-60,0,30,30)
        self.upButton.setToolTip("返回上级目录")
        self.upButton.clicked.connect(self.master.up)
        #刷新
        self.flushButton = Button(self)
        self.flushButton.setIcon(QIcon("assets\\ico\\ui\\flush.png"))
        self.flushButton.setGeometry(w-90,0,30,30)
        self.flushButton.setToolTip("刷新")
        self.flushButton.clicked.connect(self.master.reFile)
    def setSelectedFile(self,number:int):
        self.selectedFile=number
        l=self.master.files.__len__()
        self.selectedLabel.setText(f"{self.selectedFile}/{l}")
        width=self.metrics.width(self.selectedLabel.text())
        self.selectedLabel.setGeometry(self.width()-width-90,5,width,20)
        self.selectedLabel.setToolTip(f"共{l}个文件,选中{self.selectedFile}个")
    def select(self):
        t=self.selectButton.text()
        if(t=="o"):self.selectAll()
        elif(t=="✔" or t=="···"):
            for i in self.master.fileLines:
                i.unc()
                self.setTxt("o")
            logger.info("Unselected all files")
    def setTxt(self, a0):
        self.selectButton.setText(a0)
        if(a0=="o"):
            self.selectButton.setToolTip("全选")
        else:
            self.selectButton.setToolTip("全不选")
    def selectAll(self):
        for i in self.master.fileLines:
            i.normal_c()
            self.setTxt("✔")
        logger.info("Selected all files")

    def order(self):
        if(self.master.sortOrder=="az"):
            self.orderButton.setText("按照文件名 Z-A")
            self.orderButton.setToolTip("按照反字典法排序(文件优先)")
            self.master.sortOrder="za"
            logger.info("Setting file-sort-order to Z-A")
        elif(self.master.sortOrder=="za"):
            self.orderButton.setText("按照文件名 A-Z")
            self.orderButton.setToolTip("按照字典法排序(文件夹优先)")
            self.master.sortOrder="az"
            logger.info("Setting file-sort-order to A-Z")
        self.master.reFile()
    def resizeEvent(self, a0):
        w=self.width()
        self.addFileButton.move(w-30,0)
        self.upButton.move(w-60,0)
        self.flushButton.move(w-90,0)
        super().resizeEvent(a0)
    def newFile(self):
        logger.info("Creating new File")
        qd = newFileDialog()
        qd.exec_()
        if qd.accepted:
            apt,choice, filename = qd.on_accepted()
            if(apt and filename):
                if(legitFN(filename) and not (os.path.exists(filename))):
                    try:
                        if(choice=="file"):
                            open(filename,"w").close()
                            logger.info("Successfully created file: "+filename)
                        else:
                            os.makedirs(filename)
                            logger.info("Successfully created folder: "+filename)
                    except Exception as e:
                        logger.info(f"Failed: {e}")
                else:
                    showError("无效文件名，取消创建")
                    logger.info("Cancelled: invalid filename")
            else:
                logger.info("Cancelled: User")
class fileBox(QLabel):
    def __init__(self,*args):
        super().__init__(*args)
        self.setStyleSheet("background-color:none;color:none;border:none")
        self.master = self.parentWidget()
    def getMaster(self):return self.master
    def resizeEvent(self, a0):
        super().resizeEvent(a0)
    def wheelEvent(self, a0):
        self.master.wheelEVT_fb(a0)
        super().wheelEvent(a0)
    def mousePressEvent(self, a0):
        x,y = a0.pos().x(),a0.pos().y()
        if(x-self.x()>0 and y>90):
            index = (y-90+self.master.slider.value())//30
            if(index<self.master.fileLines.__len__()):
                if(self.master.fileLines[index].isclicked):
                    fileMenu(self.master.fileLines[index],self).exec_(self.mapToGlobal(a0.pos()))
                    return
        super().mouseMoveEvent(a0)
class fileMenu(QMenu):
    def __init__(self,fl:fileLine,master:QWidget):
        super().__init__(master)
        self.fl = fl
        self.master=master.getMaster()

        execute = QAction("打开",self)
        execute.setIcon(QIcon("assets/ico/ui/exec.png"))
        execute.triggered.connect(lambda:keyboard.press_and_release("enter"))
        self.addAction(execute)

        dele = QAction("删除",self)
        dele.setIcon(QIcon("assets/ico/ui/x.png"))
        dele.triggered.connect(lambda:keyboard.press_and_release("delete"))
        self.addAction(dele)

        rename = QAction("重命名",self)
        rename.setIcon(QIcon("assets/ico/ui/rename.png"))
        rename.triggered.connect(self.fl.rename)
        self.addAction(rename)
        
        copy = QAction("复制",self)
        copy.triggered.connect(self.master.ctrlc)
        self.addAction(copy)

        def exec_(c:str,path:str):
            cc=c.replace("<s>",path).split()
            logger.info(f"Executing {cc}")
            subprocess.Popen(cc,shell=True)
        for i in fileMenus:
            ii = QAction(i[0],self)
            ii.triggered.connect(lambda :exec_(i[1],self.fl.absname))
            if(i.__len__()>2):ii.setIcon(QIcon(i[2]))
            self.addAction(ii)



class fastLine(QPushButton):
    def __init__(self,*args):
        super().__init__(*args)
        self.unc()
        self.absname = self.text()
        self.setFont(qf)
        self.master = self.parent()
        self.name = self.absname.split("\\")[-1]
        self.setText("")
        self.clicked.connect(self.c)
        self.setIco(icons.get("*folder"))
        fm = QFontMetrics(qf)

        self.nameLabel=QLabel(self.name,self)
        self.nameLabel.setFont(qf)
        self.nameLabel.setStyleSheet("background-color:none;color:#000000;border:none")
        self.nameLabel.setGeometry(30,0,fm.width(self.name)+30,30)

        self.setToolTip(self.name if(self.absname[0]=="*") else self.absname)
        self.addMenu()
        self.customContextMenuRequested.connect(self.onMenu)
    def addMenu(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.menu = QMenu(self)

        execute = QAction("启动" if self.absname[0]=="*" else "在新标签页打开",self)
        execute.setIcon(QIcon("assets/ico/ui/exec.png"))
        execute.triggered.connect(self.exec)

        self.menu.addAction(execute)
    def onMenu(self, position):
        self.menu.exec_(self.mapToGlobal(position))

    def setIco(self,ico:QPixmap):
        self.icoLabel=QLabel(self)
        self.icoLabel.setPixmap(ico)
        self.icoLabel.move(5,5)
        self.icoLabel.setStyleSheet("background-color:none;border:none")


    def c(self):
        if(self.isclicked):self.unc()
        else:self.normal_c()
    def normal_c(self):
        self.isclicked=True
        self.setStyleSheet(f"""
        QPushButton {{
        border: 1px solid rgb({accentColor[0]-50},{accentColor[1]-50},{accentColor[2]-50}); /* 白色边框 */
        background-color: rgba({accentColor[0]},{accentColor[1]},{accentColor[2]},{alpha*0.5});  /* 原始背景颜色 */
        color: #000000;            /* 文字颜色 */
        text-align: left; 
    }}""")

    def unc(self):
        self.isclicked=False
        self.setStyleSheet(f"""
        QPushButton {{
        border:none; /* 白色边框 */
        background-color: rgba(255,255,255,{alpha*0.5});  /* 原始背景颜色 */
        color: #000000;            /* 文字颜色 */
        text-align: left; 
    }}
    QPushButton:hover {{
        background-color:rgba({accentColor1[0]},{accentColor1[1]},{accentColor1[2]},{alpha*0.5})
    }}
    QPushButton:pressed {{
        background-color: rgba({accentColor[0]},{accentColor[1]},{accentColor[2]},{alpha*0.5}); /* 按钮被按下时的背景颜色 */
    }}
        """)
    def mouseDoubleClickEvent(self, a0):
        self.exec()
        super().mousePressEvent(a0)
    def keyPressEvent(self, a0):
        if(a0.key()==Qt.Key_Return):
            self.exec()
        super().keyPressEvent(a0)
    def exec(self):
        self.master.execFile(self)
class fastBox(QLabel):
    def __init__(self, master:QWidget,fastDirs:list):
        self.fastDirs = sorted(fastDirs)
        self.fastLines = []
        super().__init__(master)

        self.setStyleSheet(f"background-color:none;border:1px solid rgba({accentColor[0]},{accentColor[1]},{accentColor[2]},{alpha*0.5})")
        self.master = master
        self.smallWidth = 180
        self.setFont(qf)

        self.titleLabel=QLabel("★快速访问",self)
        self.titleLabel.setFont(qf)
        self.titleLabel.setGeometry(0,30,100,30)
        self.titleLabel.setStyleSheet("background-color:rgba(255,255,255,0.5);color:#000000;border:none;")

        self.LRButton = QPushButton(">>",self)
        self.LRButton.setStyleSheet(self.master.addDirButton.styleSheet())
        self.LRButton.setFont(qf)
        self.LRButton.setGeometry(self.smallWidth-30,0,30,30)
        self.LRButton.clicked.connect(self.triggered)

        self.cBar = QLabel(self)
        self.cBar.setStyleSheet(self.titleLabel.styleSheet())
        self.cBar.setGeometry(0,60,240,30)

        self.initFL()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.upd)
        self.timer.start(10)
    def initFL(self):
        logger.info("Adding fastDirs")
        for i in self.fastLines:
            i.hide()
            del i

        self.settingFL = fastLine("*01\\设置",self)
        self.settingFL.icoLabel.hide()
        self.settingFL.setIco(icons.get("*settings"))
        self.fastLines.append(self.settingFL)

        for i in self.fastDirs:
            if(os.path.isabs(i) and os.path.exists(i) and (os.path.isdir(i) or os.path.ismount(i)) or (not i.replace(" ",""))):
                self.fastLines.append(fastLine(i,self))
            else:
                logger.error(f"'{i}' is not an absolute path of directory that exists and is legitimate, and is not added")
                showError(f"{i} 不是存在且合法的绝对文件夹路径，不添加")
    def upd(self):
        ii = 0
        for i in self.fastLines:
            i.setGeometry(0,90+ii*30,self.width(),30)
            ii+=1

        if(self.LRButton.text()=="<<"):
            self.resize(self.master.width(),self.height())
    def getMaster(self):return self.master
    def triggered(self):
        if(self.LRButton.text()=="<<"):
            self.LRButton.setText(">>")
            self.resize(self.smallWidth,self.height())
        else:
            self.resize(self.master.width(),self.height())
            self.LRButton.setText("<<")
        self.upd()

    def resizeEvent(self, a0):
        self.LRButton.move(self.width()-30,0)
        self.titleLabel.resize(self.width(),30)
        self.cBar.resize(self.width(),30)
        super().resizeEvent(a0)


    def execFile(self,obj:fastLine):
        if(obj.absname[0]!="*"):
            self.master.executeFile(obj,"ctrl")