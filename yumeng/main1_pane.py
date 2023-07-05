import json
import time

import numpy as np
import sys
import random
from PyQt5.Qt import *
from main1 import Ui_Keyuan_Dream
from PyQt5.QtChart import QChart, QValueAxis, QChartView, QSplineSeries, QDateTimeAxis
import subprocess
import paho.mqtt.client as mqtt
from MqttSign import AuthIfo
import folium
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl
import chuanganqi
import threading


# latitude = None
# longitude = None

class Window(QWidget, Ui_Keyuan_Dream):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setup_ui()  # 渲染画布
        self.update_data_thread = UpdateDataThread()  # 创建更新波形数据线程对象updata_data_thead
        self.connect_signals()  # 绑定触发事件
        a = None
        # 定位显示
        #latitude = chuanganqi.latitude
        #longitude = chuanganqi.longitude
        #print(latitude)

        # 创建Qt应用程序
        self.view = QWebEngineView(self.dingwei1)
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.dingwei1.setLayout(layout)
        # 创建地图HTML代码
        #html = self.create_map(latitude, longitude)
        # 将地图HTML代码加载到QtWebEngineView窗口中
        #self.view.setHtml(html)
        self.updata_location(chuanganqi.latitude,chuanganqi.longitude)
        self.view.show()

    def updata_location(self,latitude,longitude):
        self.latitude = 35.280752
        self.longitude = 113.9272888
        html = self.create_map(latitude, longitude)
        self.view.setHtml(html)

    def create_map(self, latitude, longitude):
        # 创建一个基于folium的地图对象
        attribution = 'Map data &copy; <a href="https://www.amap.com/">高德地图</a> contributors'
        map = folium.Map(location=[latitude, longitude], zoom_start=13,
                         tiles='https://webst01.is.autonavi.com/appmaptile?style=7&x={x}&y={y}&z={z}', attr=attribution)

        # 将地图对象转换为HTML格式
        map_html = map._repr_html_()
        return map_html

    # 定位模块结束

    def changePage(self, item):
        index = self.listWidget_3.row(item)
        self.stackedWidget.setCurrentIndex(index)

    def kaishi(self):
        file_qidong = "qidong.py"
        subprocess.call(["python", file_qidong])

    def zidong(self):
        file_zidong = "zidong.py"
        subprocess.call(["python", file_zidong])

    def shoudong(self):
        file_shoudong = "shoudong.py"
        subprocess.call(["python", file_shoudong])

    def dingdian(self):
        global a
        a = 1

    def disu(self):
        global a
        a = 2
        file_disu = "disu.py"
        subprocess.call(["python", file_disu])

    def zhongsu(self):
        global a
        a = 3
        file_zhongsu = "zhongsu.py"
        subprocess.call(["python", file_zhongsu])

    def gaosu(self):
        global a
        a = 4
        file_gaosu = "gaosu.py"
        subprocess.call(["python", file_gaosu])

    def zuozhuan(self):
        global a
        if a == 1:
            file_dingdianzuo = "zuozhuandingdian.py"
            subprocess.call(["python", file_dingdianzuo])

        if a == 2:
            file_disu = "disuzuozhuan.py"
            subprocess.call(["python", file_disu])

        if a == 3:
            file_zhongsu = "zhongsuzuozhuan.py"
            subprocess.call(["python", file_zhongsu])

        if a == 4:
            file_gaosu = "gaosuzuozhuan.py"
            subprocess.call(["python", file_gaosu])

    def youzhuan(self):
        global a
        if a == 1:
            file_dingdianyou = "youzhuandingdian.py"
            subprocess.call(["python", file_dingdianyou])

        if a == 2:
            file_disu = "disuyouzhuan.py"
            subprocess.call(["python", file_disu])

        if a == 3:
            file_zhongsu = "zhongsuyouzhuan.py"
            subprocess.call(["python", file_zhongsu])

        if a == 4:
            file_gaosu = "gaosuyouzhuan.py"
            subprocess.call(["python", file_gaosu])

    def tingzhi(self):
        global a
        if a == 1:
            file_dingdianyou = "tingzhizuozhuan.py"
            subprocess.call(["python", file_dingdianyou])

        if a == 2:
            file_disu = "disu.py"
            subprocess.call(["python", file_disu])

        if a == 3:
            file_zhongsu = "zhongsu.py"
            subprocess.call(["python", file_zhongsu])

        if a == 4:
            file_gaosu = "gaosu.py"
            subprocess.call(["python", file_gaosu])

    def houtui(self):
        file_houtui = "houtui.py"
        subprocess.call(["python", file_houtui])

    def jiting(self):
        file_jiting = "jiting.py"
        subprocess.call(["python", file_jiting])

    def setup_ui(self):
        self.setupUi(self)  # 调用Ui_Keyuan_Dream的setupUi渲染界面

        # 加载Qchart波形界面
        self.plot_qchart = QChartViewPlot()
        self.plot_view.setChart(self.plot_qchart)
        self.plot_view.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        self.plot_view.setRubberBand(QChartView.RectangleRubberBand)

    def closeEvent(self, event):
        self.update_data_thread.is_exit = True

    def connect_signals(self):
        # 绑定触发事件
        self.btn_start.clicked.connect(self.gengxin)
        self.update_data_thread._signal_update.connect(self.update_data_thread_slot)

    def gengxin(self):
        # 开启按钮
        self.update_data_thread.start()  # 启动线程，因为UpdateDataThread(QThread)继承自QTread

    def update_data_thread_slot(self, data):
        # 线程回调函数,将更新的数据传递给plot_qchart对象的handle_updata方法
        data = json.loads(data)
        self.plot_qchart.handle_update(data['sensor_data'])

    def wheelEvent(self, event):
        # 鼠标滚轮:缩放Qchart波形
        if event.angleDelta().y() >= 0:
            #  鼠标滚轮向上
            if event.x() < (
                    self.plot_view.width() + self.plot_view.x()) and event.x() > self.plot_view.x():
                if event.y() < (
                        self.plot_view.height() + self.plot_view.y()) and event.y() > self.plot_view.y():
                    self.plot_qchart.zoomIn()
        else:
            #  鼠标滚轮向下
            if event.x() < (
                    self.plot_view.width() + self.plot_view.x()) and event.x() > self.plot_view.x():
                if event.y() < (
                        self.plot_view.height() + self.plot_view.y()) and event.y() > self.plot_view.y():
                    self.plot_qchart.zoomOut()


# 波形显示
class QChartViewPlot(QChart):
    # 传感器数据折线图
    def __init__(self, parent=None):
        super(QChartViewPlot, self).__init__(parent)
        self.window = parent
        self.xRange = 1024
        self.counter = 0
        self.seriesList = []
        self.legend().show()

        self.axisX = QDateTimeAxis()
        self.axisX.setFormat("hh:mm:ss")
        self.axisX.setRange(QDateTime.currentDateTime(), QDateTime.currentDateTime().addSecs(self.xRange))
        self.addAxis(self.axisX, Qt.AlignBottom)
        # self.setAxisX(self.axisX, series)
        self.y_min = 0
        self.y_max = 100
        self.axisY = QValueAxis()
        self.axisY.setRange(self.y_min, self.y_max)
        self.addAxis(self.axisY, Qt.AlignLeft)
        # self.setAxisY(self.axisY, series)

        self.series = QSplineSeries()
        self.series.setName("传感器数据")
        self.series.setUseOpenGL(True)
        self.addSeries(self.series)
        self.series.attachAxis(self.axisX)
        self.series.attachAxis(self.axisY)

    def handle_update(self, data):
        # 更新传感器参数
        x = QDateTime.currentDateTime()
        y = data

        if self.counter < self.xRange:
            self.series.append(x.toMSecsSinceEpoch(), y)
            self.counter += 1
        else:
            points = self.series.pointsVector()
            for i in range(self.xRange - 1):
                points[i].setX(points[i + 1].x())
                points[i].setY(points[i + 1].y())
            points[-1].setX(x.toMSecsSinceEpoch())
            points[-1].setY(y)
            self.y_min = min(points, key=lambda point: point.y()).y()
            self.y_max = max(points, key=lambda point: point.y()).y()
            self.series.replace(points)
            self.axisX.setRange(QDateTime.fromMSecsSinceEpoch(points[0].x()),
                                QDateTime.fromMSecsSinceEpoch(points[-1], x()))
            self.axisY.setRange(self.y_min - 20, self.y_max + 20)


# 使用线程不断更新波形数据
class UpdateDataThread(QThread):
    _signal_update = pyqtSignal(str)  # 信号

    def __init__(self, parent=None):
        super(UpdateDataThread, self).__init__(parent)
        self.qmut = QMutex()
        self.is_exit = False
        self.x_range = 1024
        # self.sin = Sin()

    def run(self):
        while True:
            self.qmut.lock()
            if self.is_exit:
                break
            self.qmut.unlock()
            data = {"sensor_data": random.randint(0, 100)}
            # for i in range(self.x_range):
            self._signal_update.emit(json.dumps(data))  # 发送信号给槽函数
            time.sleep(10)

        self.qmut.unlock()


"""
#定位类
class Dingwei():
    def __init__(self):
        latitude = 035.2794963
        longitude = 113.9239203
        html = self.create_map(latitude, longitude)
        # 将地图HTML代码加载到QtWebEngineView窗口中
        view.setHtml(html)
        view.show()

    def create_map(latitude, longitude):
        # 创建一个基于folium的地图对象
        attribution = 'Map data &copy; <a href="https://www.amap.com/">高德地图</a> contributors'
        map = folium.Map(location=[latitude, longitude], zoom_start=13,
                         tiles='https://webst01.is.autonavi.com/appmaptile?style=7&x={x}&y={y}&z={z}', attr=attribution)

        # 将地图对象转换为HTML格式
        map_html = map._repr_html_()
        # 创建地图HTML代码

"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = Window(app)
    mywindow.show()
    sys.exit(app.exec_())

