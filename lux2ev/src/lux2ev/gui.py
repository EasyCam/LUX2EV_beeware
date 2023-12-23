import toga, math
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class MainScreen(toga.App):
    def startup(self):

        self.iso_list = [50,64,100,125,160,200,250,320,400,500,640,800,1000,1250,1600,2000,2500,3200,4000,5000,6400,8000,10000,12500,16000,20000,25000,32000,40000,50000,64000,80000,100000,128000,160000,200000,256000,512000,1024000]
        self.aperture_list = [0.95, 1.2, 1.4, 1.7, 1.8, 2, 2.8, 3.5, 4, 4.5, 5.6, 6.3, 7.1, 8, 11, 16, 22, 32]
        self.aperture_str_list = ['0.95', '1.2', '1.4', '1.7', '1.8', '2', '2.8', '3.5', '4', '4.5', '5.6', '6.3', '7.1', '8', '11', '16', '22', '32']
        self.shutter_speed_list =[30, 25, 20, 15, 13, 10, 8, 6, 5 , 4, 3.2, 2.5 , 2, 1.6, 1.3, 1, 0.8, 0.6, 0.5, 0.4, 1/3, 1/4, 1/5, 1/6, 1/8, 1/10, 1/13, 1/15, 1/20, 1/25, 1/30, 1/40, 1/50, 1/60, 1/80, 1/100, 1/125, 1/160, 1/200, 1/250, 1/320, 1/400, 1/500, 1/640, 1/800, 1/1000, 1/1250, 1/1600, 1/2000, 1/2500, 1/3200, 1/4000, 1/5000, 1/6400, 1/8000]
        self.shutter_speed_str_list = ['30','25','20','15','13','10','8','6','5','4','3.2','2.5','2','1.6','1.3','1','0.8','0.6','0.5','0.4','1/3','1/4','1/5','1/6','1/8','1/10','1/13','1/15','1/20','1/25','1/30','1/40','1/50','1/60','1/80','1/100','1/125','1/160','1/200','1/250','1/320','1/400','1/500','1/640','1/800','1/1000','1/1250','1/1600','1/2000','1/2500','1/3200','1/4000','1/5000','1/6400','1/8000']
        self.ev_srt_list=['+0.0','-5.0','-4.67','-4.5','-4.33','-4.0','-3.67','-3.5','-3.33','-3.0','-2.67','-2.5','-2.33','-2.0','-1.67','-1.5','-1.33','-1.0','-0.67','-0.5','-0.33','+0.0','+0.33','+0.5','+0.67','+1.0','+1.33','+1.5','+1.67','+2.0','+2.33','+2.5','+2.67','+3.0','+3.33','+3.5','+3.67','+4.0','+4.33','+4.5','+4.67','+5.0']
        self.nd_list=[1,1/2,1/4,1/8,1/16,1/32,1/64,1/128,1/256,1/512,1/1024]
        # self.nd_str_list=['1','1/2','1/4','1/8','1/16','1/32','1/64','1/128','1/256','1/512','1/1024']
        self.nd_str_list=['1','2','4','8','16','32','64','128','256','512','1024']

        self.suitable_scene_list =[]
        self.lux_value = 0.1
        self.iso_value = 50
        self.ev_adjust_value = 0 
        self.nd_adjust_value = 1 
        self.aperture_value = 0.95
        self.shutter_value = 30

        self.vertical_layout_box = toga.Box(style=Pack(direction=COLUMN))
        self.horizontal_layout_box =  toga.Box(style=Pack(direction=ROW))
        self.horizontal_layout_box1 =  toga.Box(style=Pack(direction=ROW))

        button_a = toga.Button('Set ISO', style=Pack(flex=1), on_press=self.show_a)
        button_b = toga.Button('Set Aperture', style=Pack(flex=1), on_press=self.show_b)
        button_c = toga.Button('Set Shutter', style=Pack(flex=1), on_press=self.show_c)
        button_d = toga.Button('Long Exposure', style=Pack(flex=1), on_press=self.show_d)
        button_e = toga.Button('Home', style=Pack(flex=1), on_press=self.show_e)

        self.label_lux = toga.Label('Lux: ')
        self.input_lux = toga.TextInput(placeholder='Input Lux', on_change=self.set_lux_value)     
        self.label_ev = toga.Label('EV: ')
        self.label_ev_value = toga.Label('  ')   
        self.select_ev_adjust = toga.Selection(items=self.ev_srt_list, on_change=self.set_ev_value)
        self.label_nd = toga.Label('ND: ')
        self.select_nd_adjust = toga.Selection(items=self.nd_str_list, on_change=self.set_nd_value)
        

        self.horizontal_layout_box.add(button_e)
        self.horizontal_layout_box.add(button_a)
        self.horizontal_layout_box.add(button_b)
        self.horizontal_layout_box.add(button_c)
        self.horizontal_layout_box.add(button_d)

        for i in [self.label_lux, self.input_lux, self.label_ev,self.label_ev_value,self.select_ev_adjust,self.label_nd,self.select_nd_adjust]:
            self.horizontal_layout_box1.add(i)

        self.vertical_layout_box.add(self.horizontal_layout_box,self.horizontal_layout_box1)
        self.main_window = toga.MainWindow(title=self.formal_name, size=(280, 480),)
        self.main_window.content = self.vertical_layout_box
        self.main_window.show()

        self.build_a()
        self.build_b()
        self.build_c()
        self.build_d()
        self.build_e()
        self.show_e(self.main_window)


    def build_a(self):
        self.a_label = toga.Label('Select ISO')
        self.label_iso = toga.Label('ISO: ')
        self.select_iso = toga.Selection(items=self.iso_list, on_change=self.set_iso_value)
        self.button_calcuate = toga.Button('Calculate', on_press=self.calculate)
        self.a_table_view = toga.Table(['Aperture', 'Shutter Speed'], style=Pack(flex=1,alignment='center',text_align='center'))
        # Create layout box
        horizontal_layout_box1 = toga.Box(style=Pack(direction=ROW))  
        horizontal_layout_box1.add(self.label_iso)
        horizontal_layout_box1.add(self.select_iso)
        horizontal_layout_box1.add(self.button_calcuate)
        # Center align the elements in horizontal_layout_box        
        horizontal_layout_box_list = [horizontal_layout_box1]
        for box in horizontal_layout_box_list:
            for widget in box.children:
                widget.style.update(alignment='center',text_align='center')
        self.a_content_list = [self.a_label,horizontal_layout_box1, self.a_table_view]

    def build_b(self):
        self.b_label = toga.Label('Select Aperture')
        self.b_label_aperture = toga.Label('Aperture (F/): ')
        self.b_select_aperture = toga.Selection(items=self.aperture_list, on_change=self.set_aperture_value)
        self.b_button_calcuate = toga.Button('Calculate', on_press=self.calculate_b)
        
        self.b_table_view = toga.Table(['ISO', 'Shutter Speed'], style=Pack(flex=1,alignment='center',text_align='center'))
        # Create layout box
        horizontal_layout_box1 = toga.Box(style=Pack(direction=ROW))

        horizontal_layout_box1.add(self.b_label_aperture)
        horizontal_layout_box1.add(self.b_select_aperture)
        horizontal_layout_box1.add(self.b_button_calcuate)

        # Center align the elements in horizontal_layout_box
        
        horizontal_layout_box_list = [horizontal_layout_box1]
        for box in horizontal_layout_box_list:
            for widget in box.children:
                widget.style.update(alignment='center',text_align='center')


        self.b_content_list = [self.b_label,horizontal_layout_box1, self.b_table_view]

    

    def build_c(self):
        self.c_label = toga.Label('Select Shutter')
        self.c_label_shutter = toga.Label('Shutter Speed (S): ')
        self.c_select_shutter = toga.Selection(items=self.shutter_speed_str_list, on_change=self.set_shutter_value)
        self.c_button_calcuate = toga.Button('Calculate', on_press=self.calculate_c)
        
        self.c_table_view = toga.Table(['ISO', 'Aperture'], style=Pack(flex=1,alignment='center',text_align='center'))
        # Create layout box
        horizontal_layout_box1 = toga.Box(style=Pack(direction=ROW))

        
        horizontal_layout_box1.add(self.c_label_shutter)
        horizontal_layout_box1.add(self.c_select_shutter)
        horizontal_layout_box1.add(self.c_button_calcuate)

        # Center align the elements in horizontal_layout_box
        
        horizontal_layout_box_list = [horizontal_layout_box1]
        for box in horizontal_layout_box_list:
            for widget in box.children:
                widget.style.update(alignment='center',text_align='center')


        self.c_content_list = [self.c_label,horizontal_layout_box1, self.c_table_view]

    def build_d(self):
        self.d_label = toga.Label('Long Exposure.')
        self.d_label_shutter = toga.Label('Shutter Speed (S): ')
        self.d_select_shutter = toga.TextInput(placeholder='30', on_change=self.set_shutter_value_d)
        self.d_button_calcuate = toga.Button('Calculate', on_press=self.calculate_d)        
        self.d_table_view = toga.Table(['ISO', 'Aperture'], style=Pack(flex=1,alignment='center',text_align='center'))
        # Create layout box
        horizontal_layout_box1 = toga.Box(style=Pack(direction=ROW))

        
        horizontal_layout_box1.add(self.d_label_shutter)
        horizontal_layout_box1.add(self.d_select_shutter)
        horizontal_layout_box1.add(self.d_button_calcuate)

        # Center align the elements in horizontal_layout_box
        
        horizontal_layout_box_list = [horizontal_layout_box1]
        for box in horizontal_layout_box_list:
            for widget in box.children:
                widget.style.update(alignment='center',text_align='center')

        self.d_content_list = [self.d_label,horizontal_layout_box1, self.d_table_view]



    def build_e(self):
        self.e_label = toga.Label('\nInput Lux value and then:\n\n')
        self.e_description = toga.Label('''Set ISO: Select ISO to get Aperture and Shutter.\n\nSet Aperture: Select Aperture to get ISO and Shutter.\n\nSet Shutter: Select Shutter speed to get ISO and Aperture.\n\nInput Shutter: Input Shutter speed to get ISO and Aperture. ''')
        self.e_content_list = [self.e_label, self.e_description]

    def show_a(self, widget):
        for item in self.a_content_list:
            self.vertical_layout_box.add(item)
        for item in self.b_content_list:
            self.vertical_layout_box.remove(item)
        for item in self.c_content_list:
            self.vertical_layout_box.remove(item)
        for item in self.d_content_list:
            self.vertical_layout_box.remove(item)
        for item in self.e_content_list:
            self.vertical_layout_box.remove(item)

    def show_b(self, widget):
        for item in self.a_content_list:
            self.vertical_layout_box.remove(item)
        for item in self.b_content_list:
            self.vertical_layout_box.add(item)
        for item in self.c_content_list:
            self.vertical_layout_box.remove(item)
        for item in self.d_content_list:
            self.vertical_layout_box.remove(item)
        for item in self.e_content_list:
            self.vertical_layout_box.remove(item)

    def show_c(self, widget):
        for item in self.a_content_list:
            self.vertical_layout_box.remove(item)
        for item in self.b_content_list:
            self.vertical_layout_box.remove(item)
        for item in self.c_content_list:
            self.vertical_layout_box.add(item)
        for item in self.d_content_list:
            self.vertical_layout_box.remove(item)
        for item in self.e_content_list:
            self.vertical_layout_box.remove(item)

    def show_d(self, widget):
        for item in self.a_content_list:
            self.vertical_layout_box.remove(item)
        for item in self.b_content_list:
            self.vertical_layout_box.remove(item)
        for item in self.c_content_list:
            self.vertical_layout_box.remove(item)
        for item in self.d_content_list:
            self.vertical_layout_box.add(item)
        for item in self.e_content_list:
            self.vertical_layout_box.remove(item)

    def show_e(self, widget):
        for item in self.a_content_list:
            self.vertical_layout_box.remove(item)
        for item in self.b_content_list:
            self.vertical_layout_box.remove(item)
        for item in self.c_content_list:
            self.vertical_layout_box.remove(item)
        for item in self.d_content_list:
            self.vertical_layout_box.remove(item)
        for item in self.e_content_list:
            self.vertical_layout_box.add(item)

    def clear_content(self):
        content = self.vertical_layout_box
        if content:
            for child in content.children:
                content.remove(child)


    def set_lux_value(self, widget):
        self.lux_value = 0
        try:
            self.lux_value = float(widget.value)
        except ValueError:
            # Show dialog for invalid lux input
            toga.window.info_dialog('Invalid Input', 'Lux value must be a number.')
        
        print('LUX is input as ',self.lux_value)

    def set_nd_value(self, widget):
        self.nd_adjust_value = int(widget.value)
        pass

    def set_iso_value(self, widget):
        self.iso_value = widget.value
        print('ISO is selected as ',self.iso_value)
        

    def set_ev_value(self, widget):
        self.ev_adjust_value = widget.value
        print('EV  adjusted ',self.ev_adjust_value)

    
    def set_aperture_value(self, widget):
        self.aperture_value = widget.value
        print('Aperture is selected as ',self.aperture_value)

    def set_shutter_value(self, widget):
        index = self.shutter_speed_str_list.index(widget.value)
        self.shutter_value = self.shutter_speed_list[index]
        print('Shutter Speed is selected as ',widget.value)


    def set_shutter_value_d(self,widget):
        try:
            self.shutter_value = float(widget.value)
        except ValueError:
            self.shutter_value = 30

    def calculate(self, widget):
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
        ev_used = ev_used/(self.nd_adjust_value)
                   
        data = []
        for i in range(aperture_count):
            aperture = self.aperture_list[i]
            shutter_speed = self.calculate_shutter_speed(aperture, ev_used, iso)
            data.append([str(aperture), shutter_speed])
            self.a_table_view.data.append([str(aperture), shutter_speed])


    def calculate_b(self, widget):
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
            data.append([str(iso), shutter_speed])
            self.b_table_view.data.append([str(iso), shutter_speed])


    def calculate_c(self, widget):
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

    def calculate_d(self, widget):
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

    

    # 根据ISO计算光圈和对应快门速度
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
        # 如果快门速度小于1/8000，则返回“Too Fast”
        else:
            return ('Faster Than 1/8000')


    # 根据快门速度计算ISO和对应光圈
    def calculate_aperture(self,shutter_speed,ev,iso):        
        # shutter_speed = (aperture*aperture/math.pow(2,ev)*100/iso)
        aperture = math.sqrt(shutter_speed *(math.pow(2,ev)/100*iso))
        print('Calculated aperture is ',aperture)
        if 0.95 <= aperture <= 32:
            aperture_list = self.aperture_list
            aperture_str_list = self.aperture_str_list
            closest_aperture= min(aperture_list, key=lambda x: abs(x - aperture))
            closest_aperture_index = aperture_list.index(closest_aperture)
            return str(aperture_str_list[closest_aperture_index])
        # 如果光圈数值大于30，则返回"Too Small"
        elif aperture > 32:
            return (str(int(aperture))+' Not Small Enough')
        # 如果光圈数值小于0.95，则返回"Too Big"
        else:
            return ('Not Big Enough')
        pass


def main():
    return MainScreen('Lux2Ev', 'easy.cam.lux')


if __name__ == '__main__':
    main().main_loop()
