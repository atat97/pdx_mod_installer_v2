from operator import mod
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget
from PyQt5.QtCore import pyqtSlot
import sys
from pathlib import Path
import os
import zipfile

#GUI
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Pdx Mod Installer by rekyn"
        self.left = 10
        self.top = 10
        self.width = 700
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        button_stell = QPushButton('Stellaris', self)
        button_stell.move(10, 300)
        button_stell.setAccessibleName('Stellaris')
        button_stell.clicked.connect(self.on_click)
        
        
        button_eu4 = QPushButton('EU4', self)
        button_eu4.move(110, 300)
        button_stell.setAccessibleName('Europa Universalis IV')
        button_eu4.clicked.connect(self.on_click)

        button_ck3 = QPushButton('CK3', self)
        button_stell.setAccessibleName('Crusader Kings III')
        button_ck3.move(10, 330)
        button_ck3.clicked.connect(self.on_click)

        button_ck3 = QPushButton('CK2', self)
        button_stell.setAccessibleName('Crusader Kings II')
        button_ck3.move(110, 330)
        button_ck3.clicked.connect(self.on_click)

        button_ck3 = QPushButton('HOI4', self)
        button_stell.setAccessibleName('Crusader Kings III')
        button_ck3.move(10, 360)
        button_ck3.clicked.connect(self.on_click)

        button_ck3 = QPushButton('Imperator', self)
        button_stell.setAccessibleName('Imperator')
        button_ck3.move(10, 360)
        button_ck3.clicked.connect(self.on_click)
        #TODO: Display default mod path and add an option to change it

        #mod_zip_path = 

        #TODO: Display the progress of unpacking in a text window

        self.show()

    @pyqtSlot()
    def on_click(self):
        mod_path = str(Path.home()) + "\Documents\Paradox Interactive\\" + self.sender().accessibleName()
        unpack(mod_path)
        

def unpack(path):
    #TODO: Replace print statements with graphical progress or some shit like that (terminal window)
    directory = os.fsencode(path) if os.path.exists(path) == True else print("Invalid path")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".zip"): #TODO: Works only with .zip extension            
            #Unzip the mod files
            folder_name = os.path.splitext(filename.lstrip("0123456789_"))[0]#Optional: Strips any numbers at the front
            print("Unpacking " + folder_name + "...")
            with zipfile.ZipFile(path + "/" + filename, 'r') as zip_ref:
                zip_ref.extractall(path + "/" + folder_name)
            #Delete the archive (Optional) #TODO: tickbox
            os.remove(path + "/" + filename)
            
            #Extract descriptor #TODO: Specifically checks for "descriptor.mod"/Should check for "*.mod"
            for file in os.listdir(path + "/" + folder_name):
                if os.fsdecode(file).endswith(".mod"):
                    desc = os.fsdecode(file)
            os.replace(path + "/" + folder_name + "/" + desc, path + "/" + folder_name + ".mod")
            #Strip the existing path and name line
            desc_path = path + "/" + folder_name + ".mod"
            
            #Add the path and name lines to the descriptor
            preappend_line(desc_path, "path=\"" + path + "/" + folder_name + "\"\n" + "name=\"" + folder_name + "\"\n")
            print("Done")

def preappend_line(file_name, line):
    dummy = file_name + ".mod"
    with open(file_name, 'r') as read_obj, open(dummy, 'w') as write_obj:
        write_obj.write(line)
        for line in read_obj:
            if ("path" not in line) and ("name" not in line) :
                write_obj.write(line)
    os.remove(file_name)
    os.rename(dummy,file_name)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    
    sys.exit(app.exec_())