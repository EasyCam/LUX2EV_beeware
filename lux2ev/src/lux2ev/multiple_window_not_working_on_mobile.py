import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class MainScreen(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))

        button_a = toga.Button('A', style=Pack(flex=1), on_press=self.open_a)
        button_b = toga.Button('B', style=Pack(flex=1), on_press=self.open_b)
        button_c = toga.Button('C', style=Pack(flex=1), on_press=self.open_c)
        button_d = toga.Button('D', style=Pack(flex=1), on_press=self.open_d)

        main_box.add(button_a)
        main_box.add(button_b)
        main_box.add(button_c)
        main_box.add(button_d)

        self.main_window = toga.MainWindow(title=self.name)
        self.main_window.content = main_box
        self.main_window.show()

    def open_a(self, widget):
        a_window = toga.Window(title='A')
        a_box = toga.Box(style=Pack(direction=COLUMN))

        # Number input
        number_input_a = toga.NumberInput(style=Pack(flex=1))
        a_box.add(number_input_a)

        # List selection
        list_selection_a = toga.Selection(style=Pack(flex=1))
        a_box.add(list_selection_a)

        # Data table
        data_table_a = toga.Table(['Aperture', 'Shutter Speed'], style=Pack(flex=1,alignment='center',text_align='center'))
        a_box.add(data_table_a)

        # Save button
        save_button_a = toga.Button('Save', style=Pack(flex=1), on_press=self.save_a)
        a_box.add(save_button_a)

        a_window.content = a_box
        a_window.show()

    def open_b(self, widget):
        b_window = toga.Window(title='B')
        b_box = toga.Box(style=Pack(direction=COLUMN))

        # Number input
        number_input_b = toga.NumberInput(style=Pack(flex=1))
        b_box.add(number_input_b)

        # List selection
        list_selection_b = toga.Selection(style=Pack(flex=1))
        b_box.add(list_selection_b)

        # Data table
        data_table_b = toga.Table(['Aperture', 'Shutter Speed'], style=Pack(flex=1,alignment='center',text_align='center'))
        b_box.add(data_table_b)

        # Save button
        save_button_b = toga.Button('Save', style=Pack(flex=1), on_press=self.save_b)
        b_box.add(save_button_b)

        b_window.content = b_box
        b_window.show()

    def open_c(self, widget):
        c_window = toga.Window(title='C')
        c_box = toga.Box(style=Pack(direction=COLUMN))

        # Number input
        number_input_c = toga.NumberInput(style=Pack(flex=1))
        c_box.add(number_input_c)

        # List selection
        list_selection_c = toga.Selection(style=Pack(flex=1))
        c_box.add(list_selection_c)

        # Data table
        data_table_c = toga.Table(['Aperture', 'Shutter Speed'], style=Pack(flex=1,alignment='center',text_align='center'))
        c_box.add(data_table_c)

        # Save button
        save_button_c = toga.Button('Save', style=Pack(flex=1), on_press=self.save_c)
        c_box.add(save_button_c)

        c_window.content = c_box
        c_window.show()

    def open_d(self, widget):
        d_window = toga.Window(title='D')
        d_box = toga.Box(style=Pack(direction=COLUMN))

        # Number input
        number_input_d = toga.NumberInput(style=Pack(flex=1))
        d_box.add(number_input_d)

        # List selection
        list_selection_d = toga.Selection(style=Pack(flex=1))
        d_box.add(list_selection_d)

        # Data table
        data_table_d = toga.Table(['Aperture', 'Shutter Speed'], style=Pack(flex=1,alignment='center',text_align='center'))
        d_box.add(data_table_d)

        # Save button
        save_button_d = toga.Button('Save', style=Pack(flex=1), on_press=self.save_d)
        d_box.add(save_button_d)

        d_window.content = d_box
        d_window.show()

    def save_a(self, widget):
        # Save logic for A window
        pass

    def save_b(self, widget):
        # Save logic for B window
        pass

    def save_c(self, widget):
        # Save logic for C window
        pass

    def save_d(self, widget):
        # Save logic for D window
        pass


def main():
    return MainScreen('Lux2Ev', 'easy.cam.lux')


if __name__ == '__main__':
    main().main_loop()
