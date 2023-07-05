import json
import time
import paho.mqtt.client as mqtt
from MqttSign import AuthIfo
import sys
from PyQt5.Qt import *
from test1 import Ui_Form
import subprocess

class windows(QWidget,Ui_Form):
    def __init__(self,parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 解决背景图片资源不显示的问题
        self.setupUi(self)


    def publish(self):
        file_path = "qidong.py"
        subprocess.call(["python",file_path])






if __name__ == '__main__':
    app = QApplication(sys.argv)  # sys.argv:当别人通过命令行执行此文件下的程序可以在提前设定（设定的接受命令行的参数来判定）来执行不同的业务

    window = windows()
    window.show()

    sys.exit(app.exec_())  # 让整个程序进入到消息循环，检测整个程序所接收到的用户交互