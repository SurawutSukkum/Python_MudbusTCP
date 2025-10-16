from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from pyModbusTCP.client import ModbusClient

class ModbusScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.0, 0.0, 0.5, 1)  # NAVY background
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)


        self.client = ModbusClient(host="192.168.1.254", port=502, auto_open=True)

        layout = MDBoxLayout(orientation="vertical", padding=20, spacing=20)

        self.status_label = MDLabel(
            text="Modbus Status: Connecting...",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 0.8, 1)
        )
        self.ip_input = MDTextField(hint_text="IP Address", mode="rectangle")
        self.ip_input.text = "192.168.3.254"       
        self.addr_input = MDTextField(hint_text="Register Address", mode="rectangle")
        self.value_input = MDTextField(hint_text="Value to Write", mode="rectangle")

        self.result_label = MDLabel(text="Result: ", halign="center")

        read_btn = MDRaisedButton(text="Read Register", on_release=self.read_register)
        write_btn = MDRaisedButton(text="Write Register", on_release=self.write_register)

        layout.add_widget(self.status_label)
        layout.add_widget(self.addr_input)
        layout.add_widget(self.value_input)
        layout.add_widget(write_btn)
        layout.add_widget(read_btn)
        layout.add_widget(self.result_label)

        self.add_widget(layout)
        self.update_connection_status()

        # Simulated register values
        self.simulated_registers = {10: 123, 20: 456, 30: 789}

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def update_connection_status(self):
        if self.client.is_open():
            self.status_label.text = "Modbus Status: Connected"
        else:
            self.status_label.text = "Modbus Status: Disconnected"

    def read_register(self, instance):
        try:
            addr = int(self.addr_input.text)
            value = self.simulated_registers.get(addr, None)
            if value is not None:
                self.result_label.text = f"Value: {value}"
            else:
                self.result_label.text = "Read Error: Address not found"
        except Exception as e:
            self.result_label.text = f"Error: {str(e)}"

    def write_register(self, instance):
        try:
            addr = int(self.addr_input.text)
            value = int(self.value_input.text)
            self.simulated_registers[addr] = value
            self.result_label.text = "Write OK"
        except Exception as e:
            self.result_label.text = f"Error: {str(e)}"

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.0, 0.0, 0.5, 1)  # NAVY background
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = MDBoxLayout(orientation="vertical", padding=20, spacing=20)
        label = MDLabel(text="Main  Screen", halign="center")
        layout.add_widget(label)
        self.add_widget(layout)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class App(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        self.screen_manager = MDScreenManager()

        self.main_screen = MainScreen(name="main")
        self.modbus_screen = ModbusScreen(name="modbus")

        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.modbus_screen)

        root_layout = MDBoxLayout(orientation="vertical")

        self.toolbar = MDTopAppBar(title=self.screen_manager.current.capitalize() + " Screen", elevation=10)
        self.toolbar.left_action_items = [
            ["home", lambda x: self.switch_screen("main")],
            ["server", lambda x: self.switch_screen("modbus")]
        ]

        root_layout.add_widget(self.toolbar)
        root_layout.add_widget(self.screen_manager)

        return root_layout

    def switch_screen(self, screen_name):
        self.screen_manager.current = screen_name
        self.toolbar.title = screen_name.capitalize() + " Screen"

if __name__ == "__main__":
    App().run()