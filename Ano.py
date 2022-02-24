import threading
import sys
import cv2
import webbrowser
import os
import base64
from PIL import Image
import json
import random
import time
import numpy as np
import shutil
import datetime
import glob
import time
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui,QtWidgets
from PyQt5.QtGui import QIcon
from xml.etree.ElementTree import *
from werkzeug.utils import secure_filename

classlist=[]
ext=".jpg"
ansize = 640
fname=["",""]
trainpath=None
pyaml=""
npyf=1
date=str(datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))

class ExampleWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.initUI()


    def initUI(self):
        global date,randback,backgroundimg
        backgroundimg=glob.glob('./back/*.jpg')
        if backgroundimg ==[] and randback==1:
            QMessageBox.critical(None, "ERROR:", "There are no images for compositing in the back folder.\nPlease put one or more images in the back folder, or set back to 0 in auto.conf.", QMessageBox.Yes)
            sys.exit()

        self.statusBar().showMessage('Ready')
        self.resize(600, 400)
        self.move(300, 300)
        self.setWindowTitle('Auto_Annotation.exe')
        app.setWindowIcon(QIcon('icon.png'))
        self.setMinimumHeight(200)
        self.setMinimumWidth(250)
        self.show()

        MainWidget = QWidget()
        Home  = QGridLayout()
        Home.setSpacing(0)
        grid = QGridLayout()
        grid.setSpacing(20)

        grid1 = QGridLayout()
        grid1.setSpacing(10)

        grid2 = QGridLayout()
        grid2.setSpacing(10)

        grid3 = QGridLayout()
        grid3.setSpacing(1)

        Menu = self.menuBar()


        weba = QAction("&Tutorial",self)
        weba.setShortcut('Ctrl+H')
        weba.setStatusTip('Open Github Page')
        weba.triggered.connect(self.web)

        actionFile = Menu.addMenu("Help")
        actionFile.addSeparator()
        actionFile.addAction(weba)


        Ex = Menu.addMenu("Exit")
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        Ex.addAction(exitAction)

        Home.addLayout(grid,0,0,1,1)

        MainWidget.setLayout(Home)
        self.setCentralWidget(MainWidget)

        self.imgbox =  QGraphicsView()
        self.img =QtWidgets.QGraphicsScene()
        im = QtGui.QImage('test.png')
        self.pixmap = QtGui.QPixmap.fromImage(im)
        self.img.addPixmap(self.pixmap)
        self.imgbox.setScene(self.img)

        self.classbox = QTextEdit()
        self.classbox.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.classbox.setReadOnly(True)
        self.classbox.setText("--- Log ---")
        self.classbox.append("[Generat Path]")
        self.classbox.append(" data/custom/"+date)

        grid.addWidget(self.imgbox,0,3,8,1)
        grid.addWidget(self.classbox,8,3,2,1)
        grid.addLayout(grid1,0,0,10,1)

        self.fileDD = QPushButton("Open the Video \n or \n Open the .yaml ")
        self.fileDD.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.fileDD.clicked.connect(self.showFileDialog)


        grid1.addWidget(self.fileDD,0,0,5,1)
        grid1.addLayout(grid2,5,0,3,1)
        self.logbox = QTextEdit()
        self.logbox.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.logbox.setReadOnly(True)
        self.logbox.setText("--- Example --- \n\n   Please Load Movie or data.yaml")

        grid2.addWidget(self.logbox,0,0,1,4)

        list = QWidget()
        list.resize(300,300)
        vlist = QtWidgets.QComboBox(list)
        vlist.addItem("Yolo-v5 (.yaml)")
        grid2.addWidget(vlist,2,0,1,4)

        labname = QLabel()
        labname.setText("Label Name:")
        grid2.addWidget(labname,3,0,1,1)

        self.label = QLineEdit()
        self.label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        grid2.addWidget(self.label,3,1,1,2)


        self.startB = QPushButton("Start")
        self.startB.clicked.connect(self.start)
        grid2.addWidget(self.startB,3,3,1,1)

        if randback:
            self.statusBar().showMessage("Generating npy... Please wait a moment.")
            th = threading.Thread(target=self.npy)
            th.setDaemon(True)
            th.start()

    def web(self):
        webbrowser.open("https://github.com/micro111/Auto_Annotation-Yolo-V5")

    def npy(self):
        global backgroundimg,npyf
        for i,p in enumerate(backgroundimg):
            path, ext = os.path.splitext(p)
            backgroundimg[i]= path+".npy"
            if not os.path.isfile(path+".npy"):
                im = np.array(Image.open(p))
                im = cv2.resize(cv2.cvtColor(im,cv2.COLOR_BGR2RGB),dsize=(ansize,ansize))
                np.save(path+".npy",im)
        self.statusBar().showMessage("Ready..!!")
        npyf=0

    def closeEvent(self, event):
        print("close")

    def showFileDialog(self):
        global fname,CFlag,cnumber,classlist,trainpath,validpath,pyaml
        tmp = fname
        fname = QFileDialog.getOpenFileName(self, 'Open file','',"Video or Yaml (*.mp4 *.mov *.yaml)")
        if pyaml !="":
            with open(pyaml) as f:
                for line in f:
                    line=line.strip()
                    a=line.split(": ")
                    if a[1:2]:
                        if a[0]=="train":
                            trainpath=a[1]
                        elif a[0]=="val":
                            validpath=a[1]
                        elif a[0]=="nc":
                            cnumber = int(a[1])
                        elif a[0]=="names":
                            a[1]=a[1].strip("[]").replace("\"","").replace("'","").replace(" ","")
                            classlist=a[1].split(",")
                f.close()
            self.classbox.setText("--- Log ---")
            self.classbox.append("[Train Path]")
            self.classbox.append(" "+trainpath)
            self.classbox.append("[Valid Path]")
            self.classbox.append(" "+validpath)
            self.classbox.append("[Class]")
            self.classbox.append(" "+str(cnumber))
            self.classbox.append("[Classname]")
            for i in classlist:
                self.classbox.append(" "+i)
            pyaml=""
        if fname[0]!="":
            trainpath=None
            validpath=None
            cnumber =1
            classlist=[""]
            path, ext = os.path.splitext(fname[0])
            if ext ==".yaml":
                self.classbox.setText("--- Log ---\n\n")
                with open(fname[0]) as f:
                    for line in f:
                        line=line.strip()
                        a=line.split(": ")
                        if a[1:2]:
                            if a[0]=="train":
                                trainpath=a[1]
                            elif a[0]=="val":
                                validpath=a[1]
                            elif a[0]=="nc":
                                cnumber = int(a[1])
                            elif a[0]=="names":
                                a[1]=a[1].strip("[]").replace("\"","").replace("'","").replace(" ","")
                                classlist=a[1].split(",")

                    if trainpath and validpath and cnumber and classlist and classlist!=['']:
                        self.statusBar().showMessage("Finished loading yml!")
                        self.classbox.append("[Train Path]")
                        self.classbox.append(" "+trainpath)
                        self.classbox.append("[Valid Path]")
                        self.classbox.append(" "+validpath)
                        self.classbox.append("[Class]")
                        self.classbox.append(" "+str(cnumber))
                        self.classbox.append("[Classname]")
                        for i in classlist:
                            self.classbox.append(" "+i)
                    else:
                        self.statusBar().showMessage("ERROR: The format of yml is not correct. Please try a different yml file.")

            else:
                self.logbox.setText("--- Example --- \n\n YourSelectVideo　:\n\n ----\n "+path+ext+"\n ----\n\n To start, press the \"START\" button.")
                cap = cv2.VideoCapture(fname[0])
                ret, frame = cap.read()
                frame = frame_resize(cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2RGB))
                h, w = frame.shape[:2]
                qimg = QtGui.QImage(frame.copy().flatten(), w, h, QtGui.QImage.Format_RGB888)
                self.pixmap = QtGui.QPixmap.fromImage(qimg)
                self.img.clear()
                self.img.addPixmap(self.pixmap)


                ret,frame1=cv2.threshold(cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY), 0, 255,cv2.THRESH_OTSU)
                whole_area=frame1.size
                white_area=cv2.countNonZero(frame1)
                if white_area/whole_area*100 > 50:
                    CFlag=1
                else:
                    CFlag=0
                cap.release()
        else:
            if tmp[0]!=[""]:
                fname = tmp



    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, e):
        global fname,CFlag,cnumber,classlist,trainpath,validpath,pyaml
        urls = e.mimeData().urls()
        path = urls[0].toLocalFile()
        if pyaml !="":
            with open(pyaml) as f:
                for line in f:
                    line=line.strip()
                    a=line.split(": ")
                    if a[1:2]:
                        if a[0]=="train":
                            trainpath=a[1]
                        elif a[0]=="val":
                            validpath=a[1]
                        elif a[0]=="nc":
                            cnumber = int(a[1])
                        elif a[0]=="names":
                            a[1]=a[1].strip("[]").replace("\"","").replace("'","").replace(" ","")
                            classlist=a[1].split(",")
                f.close()
            self.classbox.setText("--- Log ---")
            self.classbox.append("[Train Path]")
            self.classbox.append(" "+trainpath)
            self.classbox.append("[Valid Path]")
            self.classbox.append(" "+validpath)
            self.classbox.append("[Class]")
            self.classbox.append(" "+str(cnumber))
            self.classbox.append("[Classname]")
            for i in classlist:
                self.classbox.append(" "+i)
            pyaml=""
        if path:
            tmp = [path,""]
            path, ext = os.path.splitext(path)
            if ext ==".yaml":
                self.classbox.setText("--- Log ---\n\n")
                with open(path+ext) as f:
                    for line in f:
                        line=line.strip()
                        a=line.split(": ")
                        if a[1:2]:
                            if a[0]=="train":
                                trainpath=a[1]
                            elif a[0]=="val":
                                validpath=a[1]
                            elif a[0]=="nc":
                                cnumber = int(a[1])
                            elif a[0]=="names":
                                a[1]=a[1].strip("[]").replace("\"","").replace("'","").replace(" ","")
                                classlist=a[1].split(",")

                    if trainpath and validpath and cnumber and classlist and classlist!=['']:
                        self.statusBar().showMessage("Finished loading yml!")
                        self.classbox.append("[Train Path]")
                        self.classbox.append(" "+trainpath)
                        self.classbox.append("[Valid Path]")
                        self.classbox.append(" "+validpath)
                        self.classbox.append("[Class数]")
                        self.classbox.append(" "+str(cnumber))
                        self.classbox.append("[Classname]")
                        for i in classlist:
                            self.classbox.append(" "+i)
                    else:
                        self.statusBar().showMessage("ERROR: The format of yml is not correct. Please try a different yml file.")

            else:
                fname=tmp
                self.logbox.setText("--- Example --- \n\n YourSelectVideo　:\n\n ----\n "+path+ext+"\n ----\n\n To start, press the \"START\" button.")
                cap = cv2.VideoCapture(path+ext)
                ret, frame = cap.read()
                frame = frame_resize(cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2RGB))
                h, w = frame.shape[:2]
                qimg = QtGui.QImage(frame.copy().flatten(), w, h, QtGui.QImage.Format_RGB888)
                self.pixmap = QtGui.QPixmap.fromImage(qimg)
                self.img.clear()
                self.img.addPixmap(self.pixmap)


                ret,frame1=cv2.threshold(cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY), 0, 255,cv2.THRESH_OTSU)
                whole_area=frame1.size
                white_area=cv2.countNonZero(frame1)
                if white_area/whole_area*100 > 50:
                    CFlag=1
                else:
                    CFlag=0
                cap.release()

    def start(self):
        global fname,npyf
        if fname[0]:
            if self.label.text():
                if npyf==0:
                    th = threading.Thread(target=self.annotation)
                    th.setDaemon(True)
                    th.start()
                    self.logbox.setText("--- Example --- \n\n   Please Load Movie or data.yaml")
                    self.img.clear()

                else:
                    self.statusBar().showMessage("ERROR: The generation of npy has not been finished. Please wait until it finishes.")
            else:
                self.statusBar().showMessage("ERROR:There is no Classname label.Please describe the classname to be added in labelbox.")
        else:
            self.statusBar().showMessage("ERROR: The video is not selected. Please select it or perform D&D.")


    def annotation(self):
        global fname,CFlag,backgroundimg,cnumber,classlist,trainpath,validpath,date,pyaml,randback,fp
        self.label.setReadOnly(True)
        self.startB.setEnabled(False)
        self.fileDD.setEnabled(False)
        cap = cv2.VideoCapture(fname[0])
        fp=os.path.splitext(os.path.basename(fname[0]))[0].replace(" ","")
        classlist.append(self.label.text())
        if trainpath == None:
            cn = 0
            dir="/data/custom/"+date
            Fpath = os.getcwd().replace("\\","/")
            os.makedirs("back", exist_ok=True)
            os.makedirs(Fpath+dir+"/bbox", exist_ok=True)
            os.makedirs(Fpath+dir+"/train", exist_ok=True)
            os.makedirs(Fpath+dir+"/train/images/",exist_ok=True)
            os.makedirs(Fpath+dir+"/train/labels/",exist_ok=True)
            os.makedirs(Fpath+dir+"/valid", exist_ok=True)
            os.makedirs(Fpath+dir+"/valid/images/",exist_ok=True)
            os.makedirs(Fpath+dir+"/valid/labels/",exist_ok=True)
            os.makedirs(Fpath+dir+"/yaml", exist_ok=True)
            os.makedirs('images', exist_ok=True)
            yamlF = open(Fpath+dir+"/yaml/data.yaml",'a+')
            yamlF.write("train: "+Fpath+dir+"/train/images\nval: "+Fpath+dir+"/valid/images\n\nnc: "+str(cn+1)+"\nnames: "+str(classlist))
            yamlF.close()
            cnumber=cn
            trainpath = Fpath+dir+"/train/images"
            validpath = Fpath+dir+"/valid/images"

        else:
            date= trainpath.split("/train")[0].split("/data/custom/")[1]
            dir="data/custom/"+date
            Fpath= trainpath.split("/train")[0].split("data/custom")[0].replace("\\","/")
            yamlF = open(Fpath+dir+"/yaml/data.yaml",'w')
            yamlF.write("train: "+trainpath +"\nval: "+validpath+"\nnc: "+str(cnumber+1)+"\nnames: "+str(classlist))
            yamlF.close()

        pyaml=Fpath+dir+"/yaml/data.yaml"

        if debug:
            os.makedirs(Fpath+dir+"/debug/frame", exist_ok=True)
            os.makedirs(Fpath+dir+"/debug/gray", exist_ok=True)
            os.makedirs(Fpath+dir+"/debug/bin", exist_ok=True)
            os.makedirs(Fpath+dir+"/debug/mask", exist_ok=True)
            os.makedirs(Fpath+dir+"/debug/masked", exist_ok=True)

        digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
        n = 0
        ex=0
        self.statusBar().showMessage("Runs...")
        while True:
            ret, frame = cap.read()
            if ret:
                if debug:
                    cv2.imwrite(Fpath+dir+"/debug/frame/"+fp+"-"+str(n)+".jpg", frame)
                frame=cv2.resize(frame,dsize=(ansize,ansize))

                gray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)

                ret, binary = cv2.threshold(gray.copy(), 0, 255,cv2.THRESH_OTSU)

                if CFlag == 1:
                    binary = cv2.bitwise_not(binary)

                contours, hierarchy = cv2.findContours(binary.copy(),
                                                       cv2.RETR_LIST,
                                                       cv2.CHAIN_APPROX_SIMPLE)

                contour = max(contours, key=lambda x: cv2.contourArea(x))

                img_contour = cv2.drawContours(frame.copy(), contour, -1, (0, 255, 0), 5)

                mask = np.zeros_like(frame)
                mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
                cv2.drawContours(mask, [contour], -1, color=255, thickness=-1)

                toukaimg = cv2.bitwise_and(frame,frame,mask=mask)

                if randback:
                    back= np.load(backgroundimg[random.randint(0,len(backgroundimg)-1)])

                    mas2=cv2.bitwise_and(back,back,mask=cv2.bitwise_not(mask))
                    gousei = cv2.bitwise_or(mas2,toukaimg)
                else:
                    gousei=toukaimg

                if debug:
                    cv2.imwrite(Fpath+dir+"/debug/gray/"+fp+"-"+str(n)+".jpg", gray)
                    cv2.imwrite(Fpath+dir+"/debug/bin/"+fp+"-"+str(n)+".jpg", binary)
                    cv2.imwrite(Fpath+dir+"/debug/result/"+fp+"-"+str(n)+".jpg",img_contour)
                    cv2.imwrite(Fpath+dir+"/debug/mask/"+fp+"-"+str(n)+".jpg",mask)
                    cv2.imwrite(Fpath+dir+"/debug/masked/"+fp+"-"+str(n)+".jpg",toukaimg)

                x1,y1,x2,y2 = cv2.boundingRect(contour)

                pos=" 1 "+str(x1)+" "+str(y1)+" "+str(x2)+" "+str(y2)
                pathnumber=str(n).zfill(digit)

                xcen = float(x1 + (x1 + x2)) / 2 / ansize
                ycen = float(y1 + (y1 + y2)) / 2 / ansize
                w = float(x2) / ansize
                h = float(y2) / ansize

                jpgfullname=date+'-'+pathnumber+".jpg"

                if random.randint(0,100)<20:
                    cv2.imwrite(os.path.join(Fpath+dir+"/valid/images/"+fp+'-{}-{}.{}'.format(date,pathnumber,ext)),gousei)
                    anotxt = open(Fpath+dir+"/valid/labels/"+fp+date+'-'+pathnumber+".txt", 'a+')
                    anotxt.write(str(cnumber)+" "+'{:.6g}'.format(xcen)+" "+'{:.6g}'.format(ycen)+" "+'{:.6g}'.format(w)+" "+'{:.6g}'.format(h)+"\n")
                    anotxt.close()
                else:
                    cv2.imwrite(os.path.join(Fpath+dir+"/train/images/"+fp+'-{}-{}.{}'.format(date,pathnumber,ext)),gousei)

                    anotxt = open(Fpath+dir+"/train/labels/"+fp+date+'-'+pathnumber+".txt", 'a+')
                    anotxt.write(str(cnumber)+" "+'{:.6g}'.format(xcen)+" "+'{:.6g}'.format(ycen)+" "+'{:.6g}'.format(w)+" "+'{:.6g}'.format(h)+"\n")
                    anotxt.close()

                cv2.rectangle(gousei,(x1,y1),(x1+x2,y1+y2),(255),10)
                cv2.imwrite(os.path.join(Fpath+dir+"/bbox/"+fp+'-{}-{}{}'.format(date,pathnumber,ext)),gousei)
                n += 1
                cv2.imshow("Annotation..", gousei)
                key = cv2.waitKey(1)
                if key == 27: #esc
                    ex=1
                    break
            else:
                break
        if ex:
            self.statusBar().showMessage("Done (Interrupted in the middle)")
        else:
            self.statusBar().showMessage("Done! ")
        cap.release()
        cv2.destroyAllWindows()
        self.label.setReadOnly(False)
        self.startB.setEnabled(True)
        self.fileDD.setEnabled(True)
        fname=["",""]
        self.label.setText("")

def frame_resize(frame, n=2):
    return cv2.resize(frame, (int(frame.shape[1]*0.25), int(frame.shape[0]*0.25)))

if __name__ == '__main__':
    global randback,debug
    if os.path.isfile("auto.conf"):
        with open("auto.conf") as f:
            for line in f:
                line=line.split(":")
                if line[0]=="back":
                    randback = int(line[1].replace("\n",""))
                elif line[0]=="debug":
                    debug = int(line[1].replace("\n",""))
    else:
        conf = open("auto.conf",'a+')
        conf.write("debug:0\nback:1")
        debug=0
        randback=1
    os.makedirs("back", exist_ok=True)
    os.makedirs("data/custom/", exist_ok=True)

    app = QApplication(sys.argv)
    ew = ExampleWidget()
    sys.exit(app.exec_())
