"""
A very easy-to-use small software that uses the lux value measured by the illuminance meter to calculate the shutter speed under different ISO and aperture, and assist photography.
"""
import math
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW



class LUX2EV(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.iso_list = [50,64,100,125,160,200,250,320,400,500,640,800,1000,1250,1600,2000,2500,3200,4000,5000,6400,8000,10000,12500,16000,20000,25000,32000,40000,50000,64000,80000,100000,128000,160000,200000,256000,512000,1024000]
        self.aperture_list = [0.95, 1.2, 1.4, 1.7, 1.8, 2, 2.8, 3.5, 4, 4.5, 5.6, 6.3, 7.1, 8, 11, 16, 22, 32]
        self.shutter_speed_list =[30, 25, 20, 15, 13, 10, 8, 6, 5 , 4, 3.2, 2.5 , 2, 1.6, 1.3, 1, 0.8, 0.6, 0.5, 0.4, 1/3, 1/4, 1/5, 1/6, 1/8, 1/10, 1/13, 1/15, 1/20, 1/25, 1/30, 1/40, 1/50, 1/60, 1/80, 1/100, 1/125, 1/160, 1/200, 1/250, 1/320, 1/400, 1/500, 1/640, 1/800, 1/1000, 1/1250, 1/1600, 1/2000, 1/2500, 1/3200, 1/4000, 1/5000, 1/6400, 1/8000]
        self.shutter_speed_str_list = ['30','25','20','15','13','10','8','6','5','4','3.2','2.5','2','1.6','1.3','1','0.8','0.6','0.5','0.4','1/3','1/4','1/5','1/6','1/8','1/10','1/13','1/15','1/20','1/25','1/30','1/40','1/50','1/60','1/80','1/100','1/125','1/160','1/200','1/250','1/320','1/400','1/500','1/640','1/800','1/1000','1/1250','1/1600','1/2000','1/2500','1/3200','1/4000','1/5000','1/6400','1/8000']
        self.ev_srt_list=['+0.0','-5.0','-4.67','-4.5','-4.33','-4.0','-3.67','-3.5','-3.33','-3.0','-2.67','-2.5','-2.33','-2.0','-1.67','-1.5','-1.33','-1.0','-0.67','-0.5','-0.33','+0.0','+0.33','+0.5','+0.67','+1.0','+1.33','+1.5','+1.67','+2.0','+2.33','+2.5','+2.67','+3.0','+3.33','+3.5','+3.67','+4.0','+4.33','+4.5','+4.67','+5.0']
        
        self.suitable_scene_list =[]
        # self.lux_value = 0
        self.iso_value = 50
        self.ev_adjust_value = 0 
        self.aperture_value = 0



        self.main_box = toga.Box(style=Pack(direction=COLUMN))
        
        label_lux = toga.Label('Lux: ')
        label_iso = toga.Label('ISO: ')
        label_ev = toga.Label('EV: ')
        self.label_ev_value = toga.Label('  ')
        self.input_lux = toga.TextInput(placeholder='Input Lux', on_change=self.set_lux_value, style=Pack(width=80))
        self.select_iso = toga.Selection(items=self.iso_list, on_change=self.set_iso_value, style=Pack(width=80))
        self.select_ev_adjust = toga.Selection(items=self.ev_srt_list, on_change=self.set_ev_value, style=Pack(width=80))
        button_calcuate = toga.Button('Calculate', on_press=self.calculate)

        # Create layout box
        horizontal_layout_box1 = toga.Box(style=Pack(direction=ROW))
        horizontal_layout_box2 = toga.Box(style=Pack(direction=ROW))

        
        horizontal_layout_box1.add(label_lux)
        horizontal_layout_box1.add(self.input_lux)
        horizontal_layout_box1.add(label_iso)
        horizontal_layout_box1.add(self.select_iso)
        horizontal_layout_box2.add(label_ev)
        horizontal_layout_box2.add(self.label_ev_value)
        horizontal_layout_box2.add(self.select_ev_adjust)
        horizontal_layout_box2.add(button_calcuate)

        # Center align the elements in horizontal_layout_box
        
        horizontal_layout_box_list = [horizontal_layout_box1,horizontal_layout_box2]
        for box in horizontal_layout_box_list:
            for widget in box.children:
                widget.style.update(alignment='center',text_align='center')

        # Create a table to display aperture, shutter speed, and suitable scene
        # self.table = toga.Table(['Aperture', 'Shutter Speed', 'Suitable Scene'], style=Pack(flex=1))
        self.table = toga.Table(['Aperture', 'Shutter Speed'], style=Pack(flex=1,alignment='center',text_align='center'))

        vertical_layout_box = toga.Box(style=Pack(direction=COLUMN))
        vertical_layout_box.add(self.table)

        for box in horizontal_layout_box_list:
            self.main_box.add(box)
        vertical_layout_box.style.update(flex=1)
        self.main_box.add(vertical_layout_box)

        self.main_window = toga.MainWindow(title=self.formal_name, size=(280, 480),)
        self.main_window.content = self.main_box

        # Call on_resize to display the resized width and height
        self.main_window.show()
        self.main_window.on_resize = self.on_resize  # Attach the resize event handler
        self.on_resize(self.main_window)
    def on_resize(self, widget):
        width, height = widget.size
        print(f"width is {width}px, height is {height}px")

    def set_lux_value(self, widget):
        self.lux_value = 0
        try:
            self.lux_value = float(widget.value)
        except ValueError:
            # Show warning dialog for invalid lux input
            toga.window.info_dialog('Invalid Input', 'Lux value must be a number.')
        
        print('LUX is input as ',self.lux_value)
    def set_iso_value(self, widget):
        self.iso_value = widget.value
        print('ISO is selected as ',self.iso_value)
        

    def set_ev_value(self, widget):
        self.ev_adjust_value = widget.value
        print('EV  adjusted ',self.ev_adjust_value)

    def calculate(self, widget):
        self.table.data.clear()
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
                   
        data = []
        for i in range(aperture_count):
            aperture = self.aperture_list[i]
            shutter_speed = self.calculate_shutter_speed(aperture, ev_used, iso)
            data.append([str(aperture), shutter_speed])
            self.table.data.append([str(aperture), shutter_speed])

    # 计算快门速度
    def calculate_shutter_speed(self,aperture,ev,iso):
        # 计算快门速度
        shutter_speed = (aperture*aperture/math.pow(2,ev)*100/iso)
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
        # 如果快门速度小于1/8000，则返回“Overexposure Warning”
        else:
            return ('Overexposure Warning')

def main():
    # return LUX2EV()
    return LUX2EV('Lux2Ev', 'easy.cam.lux2ev')

if __name__ == '__main__':
    main().main_loop()
