import sys
import numpy as np
import threading
import time
import math
# import board
import busio
import adafruit_mma8451
from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

start_millis = int(round(time.time() * 1000))
DBG = True

class SensorHandler:

    def __init__(self, update_p=1):
        if DBG:
            print("Debug sensor setup")
        else:
            i2c = busio.I2C(board.SCL, board.SDA)
            sensor = adafruit_mma8451.MMA8451(i2c)
            self.set_range(2)
            self.set_fs(800)
        self.x = np.zeros((256,), dtype=int)
        self.y = np.zeros((256,), dtype=int)
        self.z = np.zeros((256,), dtype=int)
        self.aq_accel(update_p)

    def set_range(self, accel_range):
        if DBG:
            print("Debug set sensor range")
        else:
            if accel_range==2:
                sensor.range = adafruit_mma8451.RANGE_2G
            elif accel_range==4:
                sensor.range = adafruit_mma8451.RANGE_4G
            elif accel_range==8:
                sensor.range = adafruit_mma8451.RANGE_8G

    def set_fs(self, accel_fs):
        if DBG:
            print("Debug set sensor sampling frequency")
        else:
            if accel_fs==800:
                sensor.data_rate = adafruit_mma8451.DATARATE_800HZ
            elif accel_fs==400:
                sensor.data_rate = adafruit_mma8451.DATARATE_400HZ
            elif accel_fs==200:
                sensor.data_rate = adafruit_mma8451.DATARATE_200HZ
            elif accel_fs==100:
                sensor.data_rate = adafruit_mma8451.DATARATE_100HZ
            elif accel_fs==50:
                sensor.data_rate = adafruit_mma8451.DATARATE_50HZ
            elif accel_fs==12.5:
                sensor.data_rate = adafruit_mma8451.DATARATE_12_5HZ
            elif accel_fs==6.25:
                sensor.data_rate = adafruit_mma8451.DATARATE_6_25HZ
            elif accel_fs==1.56:
                sensor.data_rate = adafruit_mma8451.DATARATE_1_56HZ

    # Read data from accelerometer
    def aq_accel(self, update_p=1):
        if DBG:
            millis = int(round(time.time() * 1000))-start_millis
            xn = math.sin(millis*millis/5000)*255
            yn = math.sin(millis*millis/5000)*255
            zn = math.sin(millis*millis/5000)*255
        else:
            xn, yn, zn = sensor.acceleration
        np.append(self.x,xn)
        np.append(self.y,yn)
        np.append(self.z,zn)
        np.delete(self.x,0)
        np.delete(self.y,0)
        np.delete(self.z,0)
        return self.x

    def reset(self):
        self.x = np.zeros((256,), dtype=int)
        self.y = np.zeros((256,), dtype=int)
        self.z = np.zeros((256,), dtype=int)
        
 
class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'Tremor Analysis'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.s_handler = SensorHandler(0.5)
 
        self.table_widget = TableWidget(self)
        self.setCentralWidget(self.table_widget)
 
        self.show()
 
class TableWidget(QWidget):        
 
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
 
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()	
        self.tab2 = QWidget()	
        self.tab3 = QWidget()
        self.tabs.resize(300,200) 
 
        # Add tabs
        self.tabs.addTab(self.tab1,"Peak Analysis")
        self.tabs.addTab(self.tab2,"Spectrogram")
        self.tabs.addTab(self.tab3,"Settings")
 
        # Create Peak tab
        self.tab1.layout = QVBoxLayout(self)
        self.val_lab = QLabel()
        self.unit_lab = QLabel()
        self.unit_lab.setText("Hz")
        self.val_lab.setText("")
        self.tab1.layout.addWidget(self.val_lab)
        self.tab1.layout.addWidget(self.unit_lab)
        self.tab1.setLayout(self.tab1.layout)
        
        # Create Spectrograph tab
        self.tab2.layout = QVBoxLayout(self)
        self.resetButton1 = QPushButton("Reset")
        self.tab2.layout.addWidget(self.resetButton1)
        self.tab2.setLayout(self.tab2.layout)
        
        # TODO Create third tab
        #self.tab2.layout = QVBoxLayout(self)
        #self.resetButton1 = QPushButton("Reset")
        #self.tab2.layout.addWidget(self.resetButton1)
        #self.tab2.setLayout(self.tab2.layout)
 
        # Add tabs to widget        
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.updateLabel(parent)

    # TODO update peak freq label here
    """
    def updateLabel(self, parent):
        print("updating")
        threading.Timer(0.5, self.updateLabel(parent)).start ()
        x = parent.s_handler.aq_accel()
        self.val_lab.setText(str(x[255]))
    """
 
    @pyqtSlot()
    def on_click(self):
        self.s_handler.reset()
#        print("\n")
#        for currentQTableWidgetItem in self.tableWidget.selectedItems():
#            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
