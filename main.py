import gc
import json
import os.path
import random
import re
import subprocess
import sys
import keyboard
import pyperclip
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

app = QApplication([])
clpd = app.clipboard()
from stds import *

class ChiraelExplorer(QWidget):
    def __init__(self,argv):
        super().__init__()
        self.setWindowTitle("文件资源管理器")
        self.varUpdCodes=[]
        self.varResizeEventCodes=["w=self.width()","h=self.height()","ww=w-self.fileBox.x()"]
        self.dirs=[os.path.dirname(__file__)]
        if(len(argv)>1):
            self.dirs=argv[1:]
        self.dirBars=[]
        self.nowDir=0

        self.config={
            "bg": {
                "enabled": 0,
                "stretch": 0,
            },
            "font": {
                "name": "Microsoft YaHei",
                "italic": 0,
                "bold": 0
            },
            "logger": 1,
            "accentColor": [
                204,
                232,
                255
            ],
            "fastDirs":[
            ],
            "menus":{
                "file":[
                    ["用记事本打开","notepad <s>","assets/ico/txt.png"]
                ]
            }
        }
        if(not os.path.exists("config.json")):
            showInfo("配置文件不存在，使用默认配置")
            json.dump(self.config,open("config.json","w",encoding="utf-8"),indent=4,ensure_ascii=False)
        elif(os.path.isfile("config.json")):
            try:
                tmp_config=json.load(open("config.json","r",encoding="utf-8"))
                if(tmp_config.keys()==self.config.keys()):
                    if(list(i>74for i in tmp_config.get("accentColor"))==[1,1,1]):
                        self.config=tmp_config
                    else:showInfo("配置文件格式错误，使用默认配置")
                else:showInfo("配置文件格式错误，使用默认配置")
            except:showError("配置文件语法错误，使用默认配置")
        else:
            showInfo("读取配置文件失败，使用默认配置")

        logger.enable(self.config.get("logger"))
        logger.info("Enabled logger")
        self.saveCfg()
        setfileMenu(self.config.get("menus").get("file"))

        f_config=self.config.get("font" )
        logger.info("Setting font")
        setFont(f_config.get("name"),f_config.get("italic"),f_config.get("bold"))
        self.f = QFont(f_config.get("name"),10)
        self.f.setItalic(f_config.get("italic"))
        self.f.setBold(f_config.get("bold"))
        setAC(self.config.get("accentColor"))
        setAlpha(self.config.get("bg").get("enabled"))



        self.icons=setIcon()
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.upd)
        self.timer.start(10)
        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.upd1)
        self.timer1.start(10)

    def initUI(self):
        logger.info("Initializing UserInterface")
        self.setWindowIcon(QIcon("assets/ico.png"))

        #处理背景
        self.setStyleSheet("background-color:#ffffff")
        logger.info("Making background")
        if os.path.exists("assets/background") and self.config.get("bg").get("enabled"):
            picDir = [f for f in os.listdir("assets/background") if os.path.isfile(os.path.join("assets/background", f))]
            if picDir:
                self.bg = QLabel(self)
                self.bg.setAlignment(Qt.AlignLeft | Qt.AlignTop)
                self.BGpic = "assets/background/" + random.choice(picDir)
                self.bgImg = QPixmap(self.BGpic)
                self.varUpdCodes.append("newimg=self.bgImg.scaled(self.width(), self.height()"+", Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation"*(not self.config.get("bg").get("stretch"))+")\nself.bg.setPixmap(newimg)\nself.bg.move(self.width()//2-newimg.size().width()//2,self.height()//2-newimg.size().height()//2)")
                self.bg.setPixmap(self.bgImg)
        #右边那个显示文件的部分
        self.fileBox = fileBox(self)
        self.fileBox.setGeometry(0,0,960,600)
        self.varResizeEventCodes.append("if(not keyboard.is_pressed('f1')):self.fileBox.resize(ww,h)")
        self.varUpdCodes.append("self.fileBox.move(self.fastBox.width()-1,self.fileBox.y())")
        #标签
        logger.info("Adding tabs")
        self.reBar()
        #+标签
        self.addDirButton=QPushButton(self.fileBox)
        self.addDirButton.setIcon(QIcon("assets/ico/ui/add.png"))
        self.addDirButton.setToolTip("新建标签页......")
        c=self.config.get("accentColor")
        c1=[(255+i)//2 for i in c]
        self.addDirButton.setStyleSheet(f"""
        QPushButton {{
        border: none; /* 白色边框 */
        background-color: rgba(255,255,255,0.5);  /* 原始背景颜色 */
        color: #000000;            /* 文字颜色 */
    }}
    QPushButton:hover {{
        background-color:rgba({c1[0]},{c1[1]},{c1[2]},0.5)
    }}
    QPushButton:pressed {{
        background-color: rgba({c[0]},{c[1]},{c[2]},0.5); /* 按钮被按下时的背景颜色 */
    }}
        """)
        self.addDirButton.setFixedSize(30,30)
        self.addDirButton.clicked.connect(self.newDir)
        self.varUpdCodes.append("self.addDirButton.move(self.dirBars.__len__()*150+30,0)")

        #标签栏编辑
        self.barEdit = QLineEdit(self.dirBars[self.nowDir].rawText,self.fileBox)
        self.barEdit.setStyleSheet("""
        color:#000000;
        background-color:rgba(255,255,255,0.5);
        """)
        self.barEdit.setFont(self.f)
        self.barEdit.returnPressed.connect(self.setDir)
        self.varResizeEventCodes.append("self.barEdit.setGeometry(0,30,ww,30)")
        self.sortOrder="az"#a-z

        #右侧滑动条
        self.slider = Slider(0,self.fileBox)
        self.slider.move(940,90)
        self.varResizeEventCodes.append("self.slider.setGeometry(ww-20,90,20,h-90)")
        self.slider.valueChanged.connect(self.slideValueChanged)

        self.files=[]
        self.fileLines=[]
        self.reFile()


        self.cBar=cBar(self.fileBox)#中间分割的
        self.cBar.setGeometry(0,60,960,30)
        self.cBar.setStyleSheet("""
        color:#000000;
        background-color:rgba(255,255,255,0.5);
        """)
        self.varResizeEventCodes.append("self.cBar.resize(ww,30)")

        self.fastBox = fastBox(self,self.config.get("fastDirs"))
        self.fastBox.setGeometry(-1,-1,0,0)
        self.varResizeEventCodes.append("if(not keyboard.is_pressed('f1')):self.fastBox.resize(self.fastBox.width(),h+2)")

        self.fileBoxLRButton = QPushButton(">>",self.fileBox)
        self.fileBoxLRButton.setFont(self.f)
        self.fileBoxLRButton.setGeometry(0,0,30,30)
        self.fileBoxLRButton.setStyleSheet(self.addDirButton.styleSheet())
        self.fileBoxLRButton.clicked.connect(self.movefileBox)

        self.fileBoxLRButton.click()

        self.resize(960,600)
        logger.info("Finished initialization")
    def movefileBox(self):
        if(self.fastBox.width()):
            self.fastBox.resize(0,0)
            self.fileBox.move(self.fastBox.width()-1,self.fileBox.y())
            self.fileBoxLRButton.setText(">>")
        else:
            self.fastBox.resize(self.fastBox.smallWidth+1,self.height())
            self.fileBox.move(self.fastBox.width()-1,self.fileBox.y())
            self.fileBoxLRButton.setText("<<")
        self.resize(self.width(),self.height())
    def slideValueChanged(self):
        self.dirBars[self.nowDir].tqdm=self.slider.value()

    def reBar(self):
        #刷新标签栏
        for i in self.dirBars:
            i.hide()
            del i
        self.dirBars=[]
        for i in range(len(self.dirs)):
            b=Bar(self.dirs[i],self.fileBox)
            b.show()
            self.dirBars.append(b)
            self.dirs[i]=self.dirBars[i].rawText

    def upd(self):
        ww = self.width()-self.fileBox.x()
        for i in self.varUpdCodes:exec(i)
        for i in self.varResizeEventCodes:exec(i)
        #标题栏
        l=[]#这个是收集要被清理的的
        for i in range(len(self.dirBars)):
            now=self.dirBars[i]
            if(now.isquited):
                l.append(i)#收集
            if(now.isclicked):
                if(i!=self.nowDir):#如果当前的被点了，但是不是当前预览
                    self.dirBars[self.nowDir].unc()
                    self.nowDir=i
                    self.flushEdit()
                    self.slider.setValue(self.dirBars[self.nowDir].tqdm)
            if(i==self.nowDir):
                now.c()#以防他被点了但是没出现反应
            now.move(i*150+30,0)
        for i in l[::-1]:
            logger.info("Closing "+self.dirs[i])
            del self.dirBars[i]
            del self.dirs[i]
            self.nowDir=min(i,self.dirBars.__len__()-1)
            self.flushEdit()
            if(not self.dirBars):
                self.close()
                self.dirs=[os.path.dirname(__file__)]
        #文件栏
        while(not os.path.exists(self.dirs[self.nowDir])):
            self.up()
            if(self.dirs[self.nowDir].replace("\\","")==self.dirs[self.nowDir]):
                self.dirBar(self.nowDir).q()
        try:
            if(sorted(os.listdir(self.dirs[self.nowDir]))!=sorted(self.files)):
                self.reFile()
        except Exception as e:
            showError(f"无法访问!\n{e}")
            self.up()
        ii=0
        iii=0
        for i in range(len(self.fileLines)):
            fl=self.fileLines[i]
            if(fl):
                iii+=1
                if(fl.isclicked):ii+=1
                if(90-self.slider.value()+i*30 <= 60):
                    fl.setGeometry(0,-100,ww,30)
                else:
                    fl.setGeometry(0,90-self.slider.value()+i*30,ww,30)
        if(ii!=iii and ii>0):
            self.cBar.setTxt("·"*(ii*100//iii//50+1))
        elif(ii==0):
            self.cBar.setTxt("o")
        self.cBar.raise_()
        self.cBar.setSelectedFile(ii)

    def upd1(self):
        if(keyboard.is_pressed("up")):
            self.slider.setValue(self.slider.value()-1)
            self.slider.triggerAction(QSlider.SliderSingleStepSub)
        elif(keyboard.is_pressed("down")):
            self.slider.setValue(self.slider.value()+1)
            self.slider.triggerAction(QSlider.SliderSingleStepAdd)
        elif(keyboard.is_pressed("f1")):
            self.fastBox.resize(self.fastBox.width(),0)
            self.fileBox.resize(self.fileBox.width(),0)


    def resizeEvent(self, a0):
        self.resize(a0.size())
        super().resizeEvent(a0)

    def resize(self, *__args):
        for i in self.varResizeEventCodes:exec(i)
        super().resize(*__args)

    def flushEdit(self):
        try:
            self.barEdit.setText(self.dirs[self.nowDir])
        except Exception as e:
            pass
    def setDir(self):
        #当写标签栏时回车
        txt=self.barEdit.text()
        self.barEdit.clearFocus()
        if(os.path.isabs(txt) and os.path.exists(txt) and (os.path.isdir(txt) or os.path.ismount(txt)) or (not txt.replace(" ",""))):
            self.dirBars[self.nowDir].set(txt)
            self.dirs[self.nowDir]=self.dirBars[self.nowDir].rawText
            self.flushEdit()
        else:
            showError("这不是一个合法且存在的绝对路径",self)

    def closeEvent(self, a0):
        logger.info("Closing...")
        self.saveCfg()
        logger.info("Saving log")
        EXIT()
        super().closeEvent(a0)
    def saveCfg(self):
        logger.info("Saving config")
        json.dump(self.config,open("config.json","w",encoding="utf-8"),indent=4,ensure_ascii=False)
    def newDir(self):
        logger.info("Creating new tab")
        self.dirs.append("")
        self.nowDir=len(self.dirs)-1
        self.reBar()
        self.flushEdit()

    def executeFile(self,file,args=""):
        #跑文件
        try:
            if(os.path.isdir(file.absname)):
                if(keyboard.is_pressed("ctrl") or args=="ctrl"):
                    self.addDirButton.click()
                    logger.info(f"Opening {file.absname} in new tab")
                else:
                    logger.info("Opening "+file.absname)
                self.dirs[self.nowDir]=file.absname
                self.flushEdit()
                self.reBar()
                self.dirBars[self.nowDir].tqdm=0
                self.slider.setValue(0)
                self.slider.triggerAction(QSlider.SliderSingleStepSub)

            else:
                logger.info(f"Trying to execute {file.absname}")
                if(file.type=="exe"):
                    subprocess.run(f'{file.absname}',  creationflags=subprocess.CREATE_NEW_CONSOLE)
                else:
                    logger.info(f'Starting "{file.absname}"')
                    subprocess.Popen(['start', f'{file.absname}'],shell=True)
        except Exception as e:
            showError(f"访问失败!\n{e}")
            logger.error(f"Failed: {e}")
            raise e

    def reFile(self):
        #刷新fileLine列表
        logger.info("Flushing fileLines in "+self.dirs[self.nowDir])
        self.files=os.listdir(self.dirs[self.nowDir])
        for i in self.fileLines:
            i.hide()
            i.destroy()
            del i
        gc.collect()
        self.fileLines=[]
        fiLines,foLines=[],[]
        for i in self.files:
            l=self.dirs[self.nowDir]+"\\"+i
            if(os.path.isdir(l)):foLines.append(i)
            else:fiLines.append(i)
        del self.files
        self.files=sorted(foLines)+sorted(fiLines)
        for i in self.files:
            fl=fileLine(self.dirs[self.nowDir]+"\\"+i,self.fileBox)
            fl.show()
            self.fileLines.append(fl)
        self.slider.raise_()
        self.slider.setRange(0,(self.files.__len__()-1)*30)
        self.slider.setValue(min(self.slider.value(),(self.files.__len__()-1)*30))
        if(self.sortOrder=="za"):self.fileLines.reverse()
    def up(self):#到父目录
        self.dirs[self.nowDir]=os.path.dirname(self.dirs[self.nowDir])
        logger.info("Returning to "+self.dirs[self.nowDir])
        self.slider.setValue(0)
        self.slider.triggerAction(QSlider.SliderSingleStepSub)
        self.reBar()
        self.flushEdit()
    def mousePressEvent(self, a0):
        if(not self.barEdit.underMouse()):self.barEdit.clearFocus()
        super().mousePressEvent(a0)
    def keyReleaseEvent(self, a0):
        if(a0.key()==16777219 and not self.barEdit.hasFocus()):#backspace
            self.up()
        if(a0.key()==16777223):#del
            delList=[]
            for i in self.fileLines:
                if(i.isclicked):
                    delList.append(i)
            l=len(delList)
            if(l):
                e="delList[i].dele()"
                if(keyboard.is_pressed("shift")):
                    if(AskIf("删除",f"你真的要永久删除这{l}个文件吗")):
                        e="delList[i].cdele()"
                    else:e=""
                for i in range(len(delList)):
                    exec(e)
                    self.setWindowTitle(f"删除中:{str(i/l*100)[:4]}%")
                self.setWindowTitle("文件资源管理器")
        if(a0.key()==16777220):#enter
            for i in self.fileLines:
                if(i.isclicked):
                    self.executeFile(i)
                    i.unc()
        super().keyReleaseEvent(a0)
    def keyPressEvent(self, a0):
        if keyboard.is_pressed("ctrl"):
            key=a0.key()
            if(key == Qt.Key_A):
                if(self.cBar.selectButton.text()=="✔"):
                    self.cBar.selectButton.click()
                else:
                    self.cBar.selectAll()
            elif(key == Qt.Key_Equal):
                self.cBar.addFileButton.click()
            elif(key == Qt.Key_E):
                self.cBar.flushButton.click()
            elif(key == Qt.Key_S):
                if(self.config.get("bg").get("enabled")):
                    try:
                        logger.info("Saving BGimg to "+self.BGpic)
                        self.bgImg.save(self.BGpic)
                        showInfo("背景图片已经成功保存为"+self.BGpic)
                    except Exception as e:
                        showError("保存"+self.BGpic+f"失败：{e}")
                        logger.error(f"Failed:{e}")
            elif(key == Qt.Key_C):self.ctrlc()
        elif(keyboard.is_pressed("alt")):
            key=a0.key()
            if(key==Qt.Key_Equal):
                self.addDirButton.click()
        elif(keyboard.is_pressed("home")):
            self.slider.setValue(0)
            self.slider.triggerAction(QSlider.SliderSingleStepSub)
        elif(keyboard.is_pressed("end")):
            self.slider.setValue(self.files.__len__()*30-30)
            self.slider.triggerAction(QSlider.SliderSingleStepAdd)
        elif(a0.key()==Qt.Key_F2):
            logger.info("Trying to restart")
            if(AskIf("重启","确定要重启程序吗")):
                self.restart(AskIf("重启","确定要继续现已打开的目录吗"))
            else:
                logger.info("Cancelled : User")
        super().keyPressEvent(a0)

    def restart(self,saveDir:bool):
        logger.info(f"RESTART | with now dirs:{saveDir}")
        subprocess.Popen(["python",__file__,*((""),self.dirs)[saveDir]],  shell=True)
        self.close()
    def getMaster(self):return self
    def wheelEVT_fb(self,a0):#处理fileBox的wheelEvent
        self.slider.setValue(self.slider.value()-a0.angleDelta().y())
        self.slider.triggerAction(QSlider.SliderSingleStepSub)
    def ctrlc(self):
        fls=[]
        for fl in self.fileLines:
            if(fl.isclicked):
                fls.append(f"file:\\\\\\{fl.absname}".replace("\\","/"))
        qmd = QMimeData()
        qmd.setText("\n".join(fls))
        clpd.setMimeData(qmd)
    def addFast(self):
        add = renameDialog()
        add.setWindowTitle("添加目录......")
        logger.info("Adding fast dirs......")
        add.exec_()
        if(add.accepted):
            filename = add.lineEdit.text()
            if(add.is_accepted and filename):
                if(os.path.isabs(filename) and os.path.exists(filename) and os.path.isdir(filename)):
                    self.config.get('fastDirs').append(filename.replace("/","\\"))
                    self.fastBox.initFL(self.config.get('fastDirs'))
                else:
                    showError("这就是不是存在的绝对路径")
                    logger.info("Cancelled: invalid dirname")
            else:logger.info("Cancelled : User")



if __name__ == "__main__":
    m = ChiraelExplorer(sys.argv)
    m.show()
    sys.exit(app.exec_())