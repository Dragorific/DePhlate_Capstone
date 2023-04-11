from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
import subprocess

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=(10,10,10,10), spacing=30)
        layout.gravity = 'center'
        
        with layout.canvas.before:
            Color(0.2, 0.2, 0.2, 0.7)  # Grey color in RGBA format
            self.bg_rect = Rectangle(size=layout.size, pos=layout.pos)
        
        layout.bind(size=self.update_bg_rect, pos=self.update_bg_rect)

        logo_image = Image(source='assets/logoo.png', size_hint=(0.3, 0.3), pos_hint={'center_x': 0.5}) # Set size_hint and pos_hint for logo_image
        layout.add_widget(logo_image)

        self.start_button = Button(background_normal='assets/start_2.png', size_hint=(0.8, 0.3), pos_hint={'center_x': 0.5}) # Set size_hint and pos_hint for start_button
        self.start_button.bind(on_press=self.on_start_button_press)
        layout.add_widget(self.start_button)

        example_text = "Click \"Start\" to begin tracking your macros and calories!" # Define example text
        label = Label(text=example_text, size_hint_y=0.2, pos_hint={'center_x': 0.5}) # Set size_hint and pos_hint for label
        layout.add_widget(label)

        self.add_widget(layout)

    def update_bg_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def on_start_button_press(self, instance):
        subprocess.Popen(['python', 'camera_stream.py'])