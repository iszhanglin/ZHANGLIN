"""import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
import folium
def create_map(latitude, longitude):
    # 创建一个基于folium的地图对象
    attribution = 'Map data &copy; <a href="https://www.amap.com/">高德地图</a> contributors'
    map = folium.Map(location=[latitude, longitude], zoom_start=13, tiles='https://webst01.is.autonavi.com/appmaptile?style=7&x={x}&y={y}&z={z}',attr=attribution)

    # 将地图对象转换为HTML格式
    map_html = map._repr_html_()
    return map_html


if __name__ == "__main__":
    # 设置经纬度
    latitude = 035.2794963
    longitude = 113.9239203

    # 创建Qt应用程序
    app = QApplication([])
    view = QWebEngineView()

    # 创建地图HTML代码
    html = create_map(latitude, longitude)
    # 将地图HTML代码加载到QtWebEngineView窗口中
    view.setHtml(html)
    view.show()

    # 运行Qt应用程序
    app.exec_()
"""

import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
import folium

