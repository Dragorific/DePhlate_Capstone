# Import all Kivy modules
import json
import os
import socket
import webbrowser
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.video import Video
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.config import Config
from kivy.core.window import Window

# Import the Screen compo
from frontend_assets.HomeScreen import HomeScreen
from frontend_assets.ChatScreen import ChatScreen
from frontend_assets.SettingsScreen import SettingsScreen
from frontend_assets.JournalScreen import JournalScreen
from frontend_assets.HelpScreen import HelpScreen

# Set window size to mobile
Config.set('graphics', 'width', 500)
Config.set('graphics', 'height', 850)
Window.size = (500, 850)

class MyLoadingScreen(Screen):
    def __init__(self, **kwargs):
        super(MyLoadingScreen, self).__init__(**kwargs)
        self.add_widget(Image(source='assets/logo_loading.png'))
        # # Create an Image widget

class MyMainScreen(Screen):
    def __init__(self, **kwargs):
        super(MyMainScreen, self).__init__(**kwargs)

        background_image = Image(source='assets/dephlate_bg.jpg', allow_stretch=True, keep_ratio=False)
        self.add_widget(background_image)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=5)

        # Title bar
        self.title_bar = Label(text='DePhlate Home', size_hint_y=0.05)
        with self.title_bar.canvas.before:
            Color(0.2, 0.2, 0.2)  # Dark grey color in RGB format
            self.title_bar_rect = Rectangle(size=self.title_bar.size, pos=self.title_bar.pos)

        self.title_bar.bind(size=self.update_title_bar_rect, pos=self.update_title_bar_rect)
        layout.add_widget(self.title_bar)

        # Main content area
        self.content_area = BoxLayout(size_hint_y=0.8)
        self.home_screen = HomeScreen(name='home_screen', opacity=0, size_hint_x=0)
        self.chat_screen = ChatScreen(name='chat_screen', opacity=0, size_hint_x=0, disabled=True)
        self.settings_screen = SettingsScreen(name='settings_screen', opacity=0, size_hint_x=0, disabled=True)
        self.journal_screen = JournalScreen(name='journal_screen', opacity=0, size_hint_x=0, disabled=True)
        self.help_screen = HelpScreen(name='help_screen', opacity=0, size_hint_x=0, disabled=True)

        self.content_area.add_widget(self.home_screen)
        self.content_area.add_widget(self.chat_screen)
        self.content_area.add_widget(self.settings_screen)
        self.content_area.add_widget(self.journal_screen)
        self.content_area.add_widget(self.help_screen)
        layout.add_widget(self.content_area)

        # Navigation bar
        nav_bar = GridLayout(cols=5, size_hint_y=0.1)

        with nav_bar.canvas.before:
            Color(0.2, 0.2, 0.2)  # Dark grey color in RGB format
            self.rect = Rectangle(size=nav_bar.size, pos=nav_bar.pos)

        nav_bar.bind(size=self.update_rect, pos=self.update_rect)

        home_button = Button(background_normal='assets/home.png')
        chat_button = Button(background_normal='assets/chat_icon.png')
        settings_button = Button(background_normal='assets/gear.png')
        journal_button = Button(background_normal='assets/journal.png')
        help_button = Button(background_normal='assets/web.png')

        home_button.bind(on_release=self.home_pressed)
        chat_button.bind(on_release=self.chat_pressed)
        settings_button.bind(on_release=self.settings_pressed)
        journal_button.bind(on_release=self.journal_pressed)
        help_button.bind(on_release=self.help_pressed)

        nav_bar.add_widget(chat_button)
        nav_bar.add_widget(journal_button)
        nav_bar.add_widget(home_button)
        nav_bar.add_widget(help_button)
        nav_bar.add_widget(settings_button)

        layout.add_widget(nav_bar)
        self.add_widget(layout)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def update_title_bar_rect(self, instance, value):
        self.title_bar_rect.pos = instance.pos
        self.title_bar_rect.size = instance.size

    def home_pressed(self, instance):
        self.title_bar.text = 'DePhlate Home'
        self.switch_to_screen('home_screen')

    def chat_pressed(self, instance):
        self.title_bar.text = 'Health Advice'
        self.switch_to_screen('chat_screen')

    def settings_pressed(self, instance):
        self.title_bar.text = 'Settings'
        self.switch_to_screen('settings_screen')

    def journal_pressed(self, instance):
        self.title_bar.text = 'Health Journal'
        self.journal_screen = JournalScreen(name='journal_screen', opacity=0, size_hint_x=0, disabled=True)
        self.switch_to_screen('journal_screen')

    def help_pressed(self, instance):
        current_dir = os.getcwd()
        url = current_dir + '/landing_page/index.html'
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
        try:
            chrome = webbrowser.get(chrome_path)
            chrome.open(url)
        except Exception as e:
            print(f"Error: {e}")
            webbrowser.open(url)  # Fallback to the default browser if Chrome is not available

    def switch_to_screen(self, screen_name):
        # Hide all screens
        for screen in self.content_area.children:
            if screen.name != screen_name:
                screen.opacity = 0
                screen.width = 0
                screen.disabled = True
        
        # Find the screen and show it
        for screen in self.content_area.children:
            if screen.name == screen_name:
                screen.opacity = 1
                screen.width = 480
                screen.disabled = False

        print()

class MyApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        loading_screen = MyLoadingScreen(name='loading_screen')
        main_screen = MyMainScreen(name='main_screen')

        self.screen_manager.add_widget(loading_screen)
        self.screen_manager.add_widget(main_screen)

        Clock.schedule_once(lambda dt: self.switch_to_main_screen(), 3)

        return self.screen_manager

    def switch_to_main_screen(self):
        self.screen_manager.current = 'main_screen'

if __name__ == '__main__':
    system_name = socket.gethostname()
    filename = "user_data/data.json"

    try:
        with open(filename, 'r') as file:
            json_data = file.read()

        data = json.loads(json_data)

        if system_name in data:
            age = data[system_name]["user-info"]["age"]
            weight = data[system_name]["user-info"]["weight"]
            gender = data[system_name]["user-info"]["gender"]
            height = data[system_name]["user-info"]["height"]
        else:
            print(f"No data found for user: {system_name}")
    except (FileNotFoundError, json.JSONDecodeError):
        print("No data found in the file or file not found.")

    MyApp().run()
