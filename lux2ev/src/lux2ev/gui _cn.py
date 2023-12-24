'''
基于Beeware和Toga的LUX2EV软件
版本号：V1.0
# This project was generated with 0.3.16 using template: https://github.com/beeware/briefcase-template@v0.3.16
[tool.briefcase]
project_name = "LUX2EV"
bundle = "easy.cam"
version = "2023.12.24.1"
url = "https://github.com/EasyCam/LUX2EV_beeware"
license = "GNU General Public License v3 or later (GPLv3+)"
author = "EasyCam"
author_email = "hopephoto@outlook.com"

[tool.briefcase.app.lux2ev]
formal_name = "LUX2EV"
description = "A very easy-to-use small software that uses the lux value measured by the illuminance meter to calculate the shutter speed under different ISO and aperture, and assist photography."
long_description = """More details about the app should go here.
"""
icon = "src/lux2ev/resources/lux2ev"
sources = [
    "src/lux2ev",
]
test_sources = [
    "tests",
]

requires = [
    "matplotlib",
    "numpy",
    "pandas",
]
test_requires = [
    "pytest",
]

[tool.briefcase.app.lux2ev.macOS]
universal_build = true
requires = [
    "toga-cocoa~=0.4.0",
    "std-nslog~=1.0.0"
]

[tool.briefcase.app.lux2ev.linux]
requires = [
    "toga-gtk~=0.4.0",
]

[tool.briefcase.app.lux2ev.linux.system.debian]
system_requires = [
    # Needed to compile pycairo wheel
    "libcairo2-dev",
    # Needed to compile PyGObject wheel
    "libgirepository1.0-dev",
]

system_runtime_requires = [
    # Needed to provide GTK and its GI bindings
    "gir1.2-gtk-3.0",
    "libgirepository-1.0-1",
    # Dependencies that GTK looks for at runtime
    "libcanberra-gtk3-module",
    # Needed to provide WebKit2 at runtime
    # "gir1.2-webkit2-4.0",
]

[tool.briefcase.app.lux2ev.linux.system.rhel]
system_requires = [
    # Needed to compile pycairo wheel
    "cairo-gobject-devel",
    # Needed to compile PyGObject wheel
    "gobject-introspection-devel",
]

system_runtime_requires = [
    # Needed to support Python bindings to GTK
    "gobject-introspection",
    # Needed to provide GTK
    "gtk3",
    # Dependencies that GTK looks for at runtime
    "libcanberra-gtk3",
    # Needed to provide WebKit2 at runtime
    # "webkit2gtk3",
]

[tool.briefcase.app.lux2ev.linux.system.suse]
system_requires = [
    # Needed to compile pycairo wheel
    "cairo-devel",
    # Needed to compile PyGObject wheel
    "gobject-introspection-devel",
]

system_runtime_requires = [
    # Needed to provide GTK
    "gtk3",
    # Needed to support Python bindings to GTK
    "gobject-introspection", "typelib(Gtk)=3.0",
    # Dependencies that GTK looks for at runtime
    "libcanberra-gtk3-0",
    # Needed to provide WebKit2 at runtime
    # "libwebkit2gtk3",
    # "typelib(WebKit2)",
]

[tool.briefcase.app.lux2ev.linux.system.arch]
system_requires = [
    # Needed to compile pycairo wheel
    "cairo",
    # Needed to compile PyGObject wheel
    "gobject-introspection",
    # Runtime dependencies that need to exist so that the
    # Arch package passes final validation.
    # Needed to provide GTK
    "gtk3",
    # Dependencies that GTK looks for at runtime
    "libcanberra",
    # Needed to provide WebKit2
    # "webkit2gtk",
]

system_runtime_requires = [
    # Needed to provide GTK
    "gtk3",
    # Needed to provide PyGObject bindings
    "gobject-introspection-runtime",
    # Dependencies that GTK looks for at runtime
    "libcanberra",
    # Needed to provide WebKit2 at runtime
    # "webkit2gtk",
]

[tool.briefcase.app.lux2ev.linux.appimage]
manylinux = "manylinux2014"

system_requires = [
    # Needed to compile pycairo wheel
    "cairo-gobject-devel",
    # Needed to compile PyGObject wheel
    "gobject-introspection-devel",
    # Needed to provide GTK
    "gtk3-devel",
    # Dependencies that GTK looks for at runtime, that need to be
    # in the build environment to be picked up by linuxdeploy
    "libcanberra-gtk3",
    "PackageKit-gtk3-module",
    "gvfs-client",
]
linuxdeploy_plugins = [
    "DEPLOY_GTK_VERSION=3 gtk",
]

[tool.briefcase.app.lux2ev.linux.flatpak]
flatpak_runtime = "org.gnome.Platform"
flatpak_runtime_version = "44"
flatpak_sdk = "org.gnome.Sdk"

[tool.briefcase.app.lux2ev.windows]
requires = [
    "toga-winforms~=0.4.0",
]

# Mobile deployments
[tool.briefcase.app.lux2ev.iOS]
requires = [
    "toga-iOS~=0.4.0",
    "std-nslog~=1.0.0"
]

[tool.briefcase.app.lux2ev.android]
requires = [
    "toga-android~=0.4.0"
]

# Web deployments
[tool.briefcase.app.lux2ev.web]
requires = [
    "toga-web~=0.4.0",
]
style_framework = "Shoelace v2.3"
'''

import toga, math
import numpy as np
import pandas as pd
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import platform


class MainScreen(toga.App):
    def startup(self):    
        # 初始化ISO列表
        self.iso_list = [50,64,100,125,160,200,250,320,400,500,640,800,1000,1250,1600,2000,2500,3200,4000,5000,6400,8000,10000,12500,16000,20000,25000,32000,40000,50000,64000,80000,100000,128000,160000,200000,256000,512000,1024000]
        # 初始化光圈列表
        self.aperture_list = [0.95, 1.2, 1.4, 1.7, 1.8, 2, 2.8, 3.5, 4, 4.5, 5.6, 6.3, 7.1, 8, 11, 16, 22, 32]
        # 初始化光圈字符串列表
        self.aperture_str_list = ['0.95', '1.2', '1.4', '1.7', '1.8', '2', '2.8', '3.5', '4', '4.5', '5.6', '6.3', '7.1', '8', '11', '16', '22', '32']
        # 初始化快门速度列表
        self.shutter_speed_list = [30, 25, 20, 15, 13, 10, 8, 6, 5, 4, 3.2, 2.5, 2, 1.6, 1.3, 1, 0.8, 0.6, 0.5, 0.4, 1/3, 1/4, 1/5, 1/6, 1/8, 1/10, 1/13, 1/15, 1/20, 1/25, 1/30, 1/40, 1/50, 1/60, 1/80, 1/100, 1/125, 1/160, 1/200, 1/250, 1/320, 1/400, 1/500, 1/640, 1/800, 1/1000, 1/1250, 1/1600, 1/2000, 1/2500, 1/3200, 1/4000, 1/5000, 1/6400, 1/8000]
        # 初始化快门速度字符串列表
        self.shutter_speed_str_list = ['30', '25', '20', '15', '13', '10', '8', '6', '5', '4', '3.2', '2.5', '2', '1.6', '1.3', '1', '0.8', '0.6', '0.5', '0.4', '1/3', '1/4', '1/5', '1/6', '1/8', '1/10', '1/13', '1/15', '1/20', '1/25', '1/30', '1/40', '1/50', '1/60', '1/80', '1/100', '1/125', '1/160', '1/200', '1/250', '1/320', '1/400', '1/500', '1/640', '1/800', '1/1000', '1/1250', '1/1600', '1/2000', '1/2500', '1/3200', '1/4000', '1/5000', '1/6400', '1/8000']
        # 初始化EV调整列表
        self.ev_srt_list = ['+0.0', '-5.0', '-4.67', '-4.5', '-4.33', '-4.0', '-3.67', '-3.5', '-3.33', '-3.0', '-2.67', '-2.5', '-2.33', '-2.0', '-1.67', '-1.5', '-1.33', '-1.0', '-0.67', '-0.5', '-0.33', '+0.0', '+0.33', '+0.5', '+0.67', '+1.0', '+1.33', '+1.5', '+1.67', '+2.0', '+2.33', '+2.5', '+2.67', '+3.0', '+3.33', '+3.5', '+3.67', '+4.0', '+4.33', '+4.5', '+4.67', '+5.0']
        # 初始化ND列表
        self.nd_list = [1, 1/2, 1/4, 1/8, 1/16, 1/32, 1/64, 1/128, 1/256, 1/512, 1/1024]
        # 初始化ND字符串列表
        self.nd_str_list = ['1', '2', '4', '8', '16', '32', '64', '128', '256', '512', '1024']
        # 初始化适合的场景列表
        self.suitable_scene_list = []
        # 初始化当前Lux值
        self.lux_value = 0.1
        # 初始化当前ISO值
        self.iso_value = 50
        # 初始化EV调整值
        self.ev_adjust_value = 0
        # 初始化ND调整值
        self.nd_adjust_value = 1
        # 初始化当前光圈值
        self.aperture_value = 0.95
        # 初始化当前快门速度值
        self.shutter_value = 30

        # 创建布局容器
        self.vertical_layout_box = toga.Box(style=Pack(direction=COLUMN))
        self.horizontal_layout_box = toga.Box(style=Pack(direction=ROW))
        self.horizontal_layout_box1 = toga.Box(style=Pack(direction=ROW))

        # 创建按钮
        button_a = toga.Button('感光度', style=Pack(flex=1), on_press=self.show_a)
        button_b = toga.Button('光圈数', style=Pack(flex=1), on_press=self.show_b)
        button_c = toga.Button('快门值', style=Pack(flex=1), on_press=self.show_c)
        button_d = toga.Button('长曝光', style=Pack(flex=1), on_press=self.show_d)
        button_e = toga.Button('主界面', style=Pack(flex=1), on_press=self.show_e)

        # 创建显示Lux值的标签和输入框
        self.label_lux = toga.Label('照度值 LUX: ')
        self.input_lux = toga.TextInput(placeholder='输入照度值', on_change=self.set_lux_value)
        # 创建显示EV值的标签和下拉框
        self.label_ev = toga.Label('电子伏 EV: ')
        self.label_ev_value = toga.Label('  ')
        self.select_ev_adjust = toga.Selection(items=self.ev_srt_list, on_change=self.set_ev_value)
        # 创建显示ND值的标签和下拉框
        self.label_nd = toga.Label('减光镜 ND: ')
        self.select_nd_adjust = toga.Selection(items=self.nd_str_list, on_change=self.set_nd_value)

        # 设置布局
        self.horizontal_layout_box.add(button_e)
        self.horizontal_layout_box.add(button_a)
        self.horizontal_layout_box.add(button_b)
        self.horizontal_layout_box.add(button_c)
        self.horizontal_layout_box.add(button_d)

        for i in [self.label_lux, self.input_lux, self.label_ev, self.label_ev_value, self.select_ev_adjust, self.label_nd, self.select_nd_adjust]:
            self.horizontal_layout_box1.add(i)

        self.vertical_layout_box.add(self.horizontal_layout_box, self.horizontal_layout_box1)
        # 创建主窗口
        self.main_window = toga.MainWindow(title=self.formal_name, size=(280, 480))
        self.main_window.content = self.vertical_layout_box
        self.main_window.show()

        # 初始化各个菜单项的功能
        self.build_a()
        self.build_b()
        self.build_c()
        self.build_d()
        self.build_e()
        self.show_e(self.main_window)


    def build_a(self):
        # 创建 Label 显示 "Select ISO"
        self.a_label = toga.Label('选择 ISO')
        # 创建 Label 显示 "ISO: "
        self.label_iso = toga.Label('ISO: ')
        # 创建 Selection 组件，用于选择 ISO 值，当值改变时调用 set_iso_value 方法
        self.select_iso = toga.Selection(items=self.iso_list, on_change=self.set_iso_value)
        # 创建 Button 组件，点击时调用 calculate 方法
        self.button_calcuate = toga.Button('计算', on_press=self.calculate)
        # 创建 Table 组件，包含两列 ["Aperture", "Shutter Speed"]，样式为 flex=1, alignment='center', text_align='center'
        self.a_table_view = toga.Table(['光圈', '快门'], 
        style=Pack(flex=1,alignment='center',text_align='center'))
        self.a_button_save = toga.Button('保存', on_press=self.save_table_a)
        # 创建布局框，方向为纵向
        horizontal_layout_box1 = toga.Box(style=Pack(direction=ROW))  
        # 将 Label 组件添加到布局框中
        horizontal_layout_box1.add(self.label_iso)
        horizontal_layout_box1.add(self.select_iso)
        horizontal_layout_box1.add(self.button_calcuate)
        # 对布局框中的元素进行居中对齐和文本对齐居中处理
        for box in horizontal_layout_box1.children:
            box.style.update(alignment='center', text_align='center')
        # 将组件列表添加到 a_content_list 中
        self.a_content_list = [horizontal_layout_box1, self.a_table_view,self.a_button_save]
    
    def build_b(self):
        # 创建 Label 显示 "'选择光圈'"
        self.b_label = toga.Label('选择光圈')
        # 创建 Label 显示 "光圈值 (F/): "
        self.b_label_aperture = toga.Label('光圈值 (F/): ')
        # 创建 Selection 组件，用于选择 Aperture 值，当值改变时调用 set_aperture_value 方法
        self.b_select_aperture = toga.Selection(items=self.aperture_list, on_change=self.set_aperture_value)
        # 创建 Button 组件，点击时调用 calculate_b 方法
        self.b_button_calcuate = toga.Button('计算', on_press=self.calculate_b)
        
        # 创建 Table 组件，包含两列 ["ISO", "Shutter Speed"]，样式为 flex=1, alignment='center', text_align='center'
        self.b_table_view = toga.Table(['感光度 ISO', '快门'], style=Pack(flex=1,alignment='center',text_align='center'))
        self.b_button_save = toga.Button('保存', on_press=self.save_table_b)
        # 创建布局框，方向为纵向
        horizontal_layout_box1 = toga.Box(style=Pack(direction=ROW))
        # 将 Label 组件添加到布局框中
        horizontal_layout_box1.add(self.b_label_aperture)
        horizontal_layout_box1.add(self.b_select_aperture)
        horizontal_layout_box1.add(self.b_button_calcuate)
        # 对布局框中的元素进行居中对齐和文本对齐居中处理
        for box in horizontal_layout_box1.children:
            box.style.update(alignment='center', text_align='center')
        # 将组件列表添加到 b_content_list 中
        self.b_content_list = [horizontal_layout_box1, self.b_table_view,self.b_button_save]
    
    def build_c(self):
        # 创建 Label 显示 "'选择快门'"
        self.c_label = toga.Label('选择快门')
        # 创建 Label 显示 "快门速度 (秒): "
        self.c_label_shutter = toga.Label('快门速度 (秒): ')
        # 创建 Selection 组件，用于选择 Shutter 值，当值改变时调用 set_shutter_value 方法
        self.c_select_shutter = toga.Selection(items=self.shutter_speed_str_list, on_change=self.set_shutter_value)
        # 创建 Button 组件，点击时调用 calculate_c 方法
        self.c_button_calcuate = toga.Button('计算', on_press=self.calculate_c)
        
        # 创建 Table 组件，包含两列 ["ISO", "Aperture"]，样式为 flex=1, alignment='center', text_align='center'
        self.c_table_view = toga.Table(['感光度 ISO', '光圈'], style=Pack(flex=1,alignment='center',text_align='center'))
        self.c_button_save = toga.Button('保存', on_press=self.save_table_c)
        # 创建布局框，方向为纵向
        horizontal_layout_box1 = toga.Box(style=Pack(direction=ROW))
        # 将 Label 组件添加到布局框中
        horizontal_layout_box1.add(self.c_label_shutter)
        horizontal_layout_box1.add(self.c_select_shutter)
        horizontal_layout_box1.add(self.c_button_calcuate)
        # 对布局框中的元素进行居中对齐和文本对齐居中处理
        for box in horizontal_layout_box1.children:
            box.style.update(alignment='center', text_align='center')
        # 将组件列表添加到 c_content_list 中
        self.c_content_list = [horizontal_layout_box1, self.c_table_view,self.c_button_save]
    
    def build_d(self):
        # 创建 Label 显示 "Long Exposure."
        self.d_label = toga.Label('长曝光')
        # 创建 Label 显示 "Shutter Speed (S): "
        self.d_label_shutter = toga.Label('快门速度 (秒): ')
        # 创建 TextInput 组件，用于输入 Shutter speed，当值改变时调用 set_shutter_value_d 方法
        self.d_select_shutter = toga.TextInput(placeholder='30', on_change=self.set_shutter_value_d)
        # 创建 Button 组件，点击时调用 calculate_d 方法
        self.d_button_calcuate = toga.Button('计算', on_press=self.calculate_d)        
        # 创建 Table 组件，包含两列 ["ISO", "Aperture"]，样式为 flex=1, alignment='center', text_align='center'
        self.d_table_view = toga.Table(['感光度 ISO', '光圈'], style=Pack(flex=1,alignment='center',text_align='center'))
        self.d_button_save = toga.Button('保存', on_press=self.save_table_d)
        # 创建布局框，方向为纵向
        horizontal_layout_box1 = toga.Box(style=Pack(direction=ROW))
        # 将 Label 组件添加到布局框中
        horizontal_layout_box1.add(self.d_label_shutter)
        horizontal_layout_box1.add(self.d_select_shutter)
        horizontal_layout_box1.add(self.d_button_calcuate)
        # 对布局框中的元素进行居中对齐和文本对齐居中处理
        for box in horizontal_layout_box1.children:
            box.style.update(alignment='center', text_align='center')
        # 将组件列表添加到 d_content_list 中
        self.d_content_list = [horizontal_layout_box1, self.d_table_view,self.d_button_save]
    
    def build_e(self):
        # 创建 Label 显示介绍性文字
        self.e_label = toga.Label('\n输入照度值 LUX 然后选择计算模式\n\n')
        # 创建 Description 组件，用于显示关于如何选择值的说明文字
        self.e_description = toga.Label('''感光度: 选择感光度ISO然后计算光圈和对应的快门速度.\n\n光圈数:选择光圈大小然后计算感光度ISO和对应的快门速度.\n\nS:快门值：选择快门速度然后计算感光度ISO和对应的光圈数.\n\n长曝光: 输入曝光时间值然后计算感光度ISO和对应的光圈数. ''')
        # 将组件列表添加到 e_content_list 中
        self.e_content_list = [self.e_label, self.e_description]
    
    def show_a(self, widget):
        self.main_window.title = self.formal_name + '\t\t选择感光度ISO然后计算光圈和对应的快门速度'
        # 将 a_content_list 中的组件添加到垂直布局框中
        for item in self.a_content_list:
            self.vertical_layout_box.add(item)
        # 移除 b_content_list 中的组件
        for item in self.b_content_list:
            self.vertical_layout_box.remove(item)            
        # 移除 c_content_list 中的组件
        for item in self.c_content_list:
            self.vertical_layout_box.remove(item)        
        # 移除 d_content_list 中的组件
        for item in self.d_content_list:
            self.vertical_layout_box.remove(item)        
        # 移除 e_content_list 中的组件
        for item in self.e_content_list:
            self.vertical_layout_box.remove(item)

    def show_b(self, widget):
        self.main_window.title = self.formal_name + '\t\t选择光圈大小然后计算感光度ISO和对应的快门速度'
        # 移除 a_content_list 中的组件
        for item in self.a_content_list:
            self.vertical_layout_box.remove(item)
        # 将 b_content_list 中的组件添加到垂直布局框中
        for item in self.b_content_list:
            self.vertical_layout_box.add(item)
        # 移除 c_content_list 中的组件
        for item in self.c_content_list:
            self.vertical_layout_box.remove(item)        
        # 移除 d_content_list 中的组件
        for item in self.d_content_list:
            self.vertical_layout_box.remove(item)        
        # 移除 e_content_list 中的组件
        for item in self.e_content_list:
            self.vertical_layout_box.remove(item)

    def show_c(self, widget):
        self.main_window.title = self.formal_name + '\t\t选择快门速度然后计算感光度ISO和对应的光圈数'
        # 移除 a_content_list 中的组件
        for item in self.a_content_list:
            self.vertical_layout_box.remove(item)
        # 移除 b_content_list 中的组件
        for item in self.b_content_list:
            self.vertical_layout_box.remove(item)
        # 将 c_content_list 中的组件添加到垂直布局框中
        for item in self.c_content_list:
            self.vertical_layout_box.add(item)
        # 移除 d_content_list 中的组件
        for item in self.d_content_list:
            self.vertical_layout_box.remove(item)
        # 移除 e_content_list 中的组件
        for item in self.e_content_list:
            self.vertical_layout_box.remove(item)

    def show_d(self, widget):
        self.main_window.title = self.formal_name + '\t\t输入曝光时间值然后计算感光度ISO和对应的光圈数'
        # 移除 a_content_list 中的组件
        for item in self.a_content_list:
            self.vertical_layout_box.remove(item)
        # 移除 b_content_list 中的组件
        for item in self.b_content_list:
            self.vertical_layout_box.remove(item)
        # 移除 c_content_list 中的组件
        for item in self.c_content_list:
            self.vertical_layout_box.remove(item)
        # 将 d_content_list 中的组件添加到垂直布局框中
        for item in self.d_content_list:
            self.vertical_layout_box.add(item)
        # 移除 e_content_list 中的组件
        for item in self.e_content_list:
            self.vertical_layout_box.remove(item)

    def show_e(self, widget):
        
        self.main_window.title = self.formal_name
        # 移除 a_content_list 中的组件
        for item in self.a_content_list:
            self.vertical_layout_box.remove(item)
        # 移除 b_content_list 中的组件
        for item in self.b_content_list:
            self.vertical_layout_box.remove(item)
        # 移除 c_content_list 中的组件
        for item in self.c_content_list:
            self.vertical_layout_box.remove(item)
        # 移除 d_content_list 中的组件
        for item in self.d_content_list:
            self.vertical_layout_box.remove(item)
        # 将 e_content_list 中的组件添加到垂直布局框中
        for item in self.e_content_list:
            self.vertical_layout_box.add(item)
    


    def save_table_a(self, widget):
        """
        保存表格a到文件a.csv
        :param widget: widgets，用于触发该函数
        """
        print(platform.system())
        if platform.system() == 'Linux':
            file_path = '/storage/emulated/0/Download/a.csv'
        else:
            file_path = 'a.csv'
            
        self.a_df.to_csv(file_path, encoding='gbk',index=False)

    def save_table_b(self, widget):
        """
        保存表格b到文件b.csv
        :param widget: widgets，用于触发该函数
        """
        print(platform.system())
        if platform.system() == 'Linux':
            file_path = '/storage/emulated/0/Download/b.csv'
        else:
            file_path = 'b.csv'
        self.b_df.to_csv(file_path, encoding='gbk',index=False)

    def save_table_c(self, widget):
        """
        保存表格c到文件c.csv
        :param widget: widgets，用于触发该函数
        """
        print(platform.system())
        if platform.system() == 'Linux':
            file_path = '/storage/emulated/0/Download/c.csv'
        else:
            file_path = 'c.csv'
        self.c_df.to_csv(file_path, encoding='gbk',index=False)

    def save_table_d(self, widget):
        """
        保存表格d到文件d.csv
        :param widget: widgets，用于触发该函数
        """
        print(platform.system())
        if platform.system() == 'Linux':
            file_path = '/storage/emulated/0/Download/d.csv'
        else:
            file_path = 'd.csv'
        self.d_df.to_csv(file_path, encoding='gbk',index=False)



    def clear_content(self):
        """
        清空内容
        """
        content = self.vertical_layout_box
        if content:
            for child in content.children:
                content.remove(child)


    def set_lux_value(self, widget):
        """
        设置光照强度值
        """
        self.lux_value = 0
        try:
            self.lux_value = float(widget.value)
        except ValueError:
            # 显示无效光照输入对话框
            toga.window.info_dialog('无效输入', '光照强度必须为数字。')
        
        print('光照强度输入为 ',self.lux_value)

    def set_nd_value(self, widget):
        """
        设置ND调整值
        """
        index = self.nd_str_list.index(widget.value)
        self.nd_adjust_value = self.nd_list[index]
        print('ND设置为 ',self.nd_adjust_value)

    def set_iso_value(self, widget):
        """
        设置ISO值
        """
        self.iso_value = widget.value
        print('ISO设置为 ',self.iso_value)
        

    def set_ev_value(self, widget):
        """
        设置EV调整值
        """
        self.ev_adjust_value = widget.value
        print('EV调整为 ',self.ev_adjust_value)

    
    def set_aperture_value(self, widget):
        """
        设置光圈值
        """
        self.aperture_value = widget.value
        print('光圈设置为 ',self.aperture_value)

    def set_shutter_value(self, widget):
        """
        设置快门速度值
        """
        index = self.shutter_speed_str_list.index(widget.value)
        self.shutter_value = self.shutter_speed_list[index]
        print('快门速度设置为 ',widget.value)


    def set_shutter_value_d(self,widget):
        """
        设置快门速度值（数字）
        """
        try:
            self.shutter_value = float(widget.value)
        except ValueError:
            self.shutter_value = 30

    def calculate(self, widget):
        '''
        计算光圈和快门速度
        '''
        self.a_table_view.data.clear()
        aperture_count = len(self.aperture_list)
        lux = self.lux_value
        # 获取下拉框中的 iso 值
        iso = self.iso_value
        # 计算 ev 值
        ev = 2+math.log2(lux /10)
        # 保留两位小数
        ev = round(ev * 10) / 10
        self.label_ev_value.text = str(ev)
        ev_used = ev - float(self.ev_adjust_value)
        
        ev_used = round(ev_used * 10) / 10
        ev_used = ev_used*(self.nd_adjust_value)
                   
        
        data = []
        for i in range(aperture_count):
            aperture = self.aperture_list[i]
            shutter_speed = self.calculate_shutter_speed(aperture, ev_used, iso)
            data.append([str(aperture), '\''+str(shutter_speed)+'\''])
            self.a_table_view.data.append([str(aperture), str(shutter_speed)])
        self.a_df =pd.DataFrame(data)
        self.a_df.columns = ['光圈F值', '快门速度']        
        print(self.a_df)

    def calculate_b(self, widget):
        '''
        计算iso和快门速度
        '''
        self.b_table_view.data.clear()
        iso_count = len(self.iso_list)
        lux = self.lux_value
        # 获取下拉框中的 aperture 值
        aperture = self.aperture_value
        # 计算 ev 值
        ev = 2+math.log2(lux /10)
        # 保留两位小数
        ev = round(ev * 10) / 10
        self.label_ev_value.text = str(ev)
        ev_used = ev - float(self.ev_adjust_value)
        
        ev_used = round(ev_used * 10) / 10
        ev_used = ev_used/(self.nd_adjust_value)
                   
        data = []
        for i in range(iso_count):
            iso = self.iso_list[i]
            shutter_speed = self.calculate_shutter_speed(aperture, ev_used, iso)
            data.append([str(iso), '\''+str(shutter_speed)+'\''])
            self.b_table_view.data.append([str(iso), str(shutter_speed)])
        self.b_df =pd.DataFrame(data)
        self.b_df.columns = ['感光度ISO', '快门速度']     
        print(self.b_df)

    def calculate_c(self, widget):
        '''
        计算iso和光圈
        '''
        self.c_table_view.data.clear()
        iso_count = len(self.iso_list)
        lux = self.lux_value
        # 获取下拉框中的 shutter 值
        shutter_speed = self.shutter_value
        # 计算 ev 值
        ev = 2+math.log2(lux /10)
        # 保留两位小数
        ev = round(ev * 10) / 10
        self.label_ev_value.text = str(ev)
        ev_used = ev - float(self.ev_adjust_value)
        
        ev_used = round(ev_used * 10) / 10
        ev_used = ev_used/(self.nd_adjust_value)
                   
        data = []
        for i in range(iso_count):
            iso = self.iso_list[i]
            aperture = self.calculate_aperture(shutter_speed, ev_used, iso)
            # if aperture != 'Took Dark':
            #     pass
            data.append([str(iso), aperture])
            self.c_table_view.data.append([str(iso), aperture])
        self.c_df =pd.DataFrame(data)
        self.c_df.columns = ['感光度ISO', '光圈F值']     
        print(self.c_df)

    def calculate_d(self, widget):
        '''
        计算快门速度和光圈
        '''
        self.d_table_view.data.clear()
        iso_count = len(self.iso_list)
        lux = self.lux_value
        # 获取输入的 shutter 值
        shutter_speed = self.shutter_value
        # 计算 ev 值
        ev = 2+math.log2(lux /10)
        # 保留两位小数
        ev = round(ev * 10) / 10
        self.label_ev_value.text = str(ev)
        ev_used = ev - float(self.ev_adjust_value)
        
        ev_used = round(ev_used * 10) / 10
        ev_used = ev_used/(self.nd_adjust_value)
                   
        data = []
        for i in range(iso_count):
            iso = self.iso_list[i]
            aperture = self.calculate_aperture(shutter_speed, ev_used, iso)
            # if aperture != 'Took Dark':
            #     pass
            data.append([str(iso), aperture])
            self.d_table_view.data.append([str(iso), aperture])
        self.d_df =pd.DataFrame(data)
        self.d_df.columns = ['感光度ISO', '光圈F值']     
        print(self.d_df)

    # 根据ISO计算光圈和对应快门速度
    def calculate_shutter_speed(self,aperture,ev,iso):
        # 计算快门速度
        shutter_speed = (aperture*aperture/np.power(2,ev)*100/iso)
        # 如果快门速度在1/8000到30之间，则从shutter_speed_list中取出最接近shutter_speed的值，并返回其字符串表示
        if 1/8000 <= shutter_speed<=30:
            shutter_speed_list = self.shutter_speed_list
            shutter_speed_str_list = self.shutter_speed_str_list
            closest_speed = min(shutter_speed_list, key=lambda x: abs(x - shutter_speed))
            closest_speed_index = shutter_speed_list.index(closest_speed)
            return str(shutter_speed_str_list[closest_speed_index])
        # 如果快门速度大于30，则返回其整数表示
        elif shutter_speed > 30:
            return str(int(shutter_speed))
        # 如果快门速度小于1/8000，则返回“Too Fast”
        else:
            return ('超过 1/8000')


    # 根据快门速度计算ISO和对应光圈
    def calculate_aperture(self,shutter_speed,ev,iso):        
        # shutter_speed = (aperture*aperture/np.power(2,ev)*100/iso)
        try:
            aperture = math.sqrt(shutter_speed *(np.power(2,ev)/100*iso))
            print('Calculated aperture is ',aperture)
            if 0.95 <= aperture <= 32:
                aperture_list = self.aperture_list
                aperture_str_list = self.aperture_str_list
                closest_aperture= min(aperture_list, key=lambda x: abs(x - aperture))
                closest_aperture_index = aperture_list.index(closest_aperture)
                return str(aperture_str_list[closest_aperture_index])
            # 如果光圈数值大于30，则返回"Too Small"
            elif 64>= aperture > 32:
                return (str(int(aperture))+' 光圈可能不够小')
            # 如果光圈数值大于30，则返回"Too Small"
            elif aperture > 64:
                return ('光圈不够小')
            # 如果光圈数值小于0.95，则返回"Too Big"
            else:
                return ('光圈不够大')
        except OverflowError:
            return ('不可用')
        


def main():
    """
    主函数：调用MainScreen类并传入参数，返回创建的屏幕对象

    参数:
        - 'Lux2Ev': 字符串类型，屏幕标签
        - 'easy.cam.lux': 字符串类型，文件路径

    返回值:
        - MainScreen类的实例对象

    示例:
        main()
    """
    return MainScreen('Lux2Ev', 'easy.cam.lux')


if __name__ == '__main__':
    """
    如果当前文件作为主程序运行，则执行main函数并调用创建的屏幕对象的main_loop方法

    参数:
        - main函数返回的屏幕对象

    示例:
        main().main_loop()
    """
    main().main_loop()