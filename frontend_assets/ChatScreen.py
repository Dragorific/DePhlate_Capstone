from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from openAIAPI import get_response
import json
import socket

class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Adding the grey background
        with layout.canvas.before:
            Color(0.2, 0.2, 0.2, 0.7)  # Grey color in RGBA format
            self.bg_rect = Rectangle(size=layout.size, pos=layout.pos)

        layout.bind(size=self.update_bg_rect, pos=self.update_bg_rect)

        # Chat content
        # self.advice_text = Label(text="", halign='left', valign='top', size_hint_y=None, text_size=(self.width * 7, None))
        self.advice_text = Label(text="", halign='center', valign='top', size_hint_y=None, height=500, text_size=(self.width*7, None), pos_hint={'top': 1})
        
        self.advice_text.bind(width=lambda *x: self.advice_text.setter('text_size')(self.advice_text, (self.advice_text.width, None)))

        advice_inner_layout = BoxLayout(orientation='vertical', size_hint_y=None, pos_hint={'bottom': 1})
        advice_inner_layout.add_widget(self.advice_text)

        # Set the height of advice_inner_layout to the height of its widgets
        advice_inner_layout.bind(minimum_height=advice_inner_layout.setter('height'))

        advice_scrollview = ScrollView(size_hint=(1, None), pos_hint={'top': 1})
        advice_scrollview.add_widget(advice_inner_layout)
        layout.add_widget(advice_scrollview)

        # TextInput for user questions
        self.question_input = TextInput(multiline=False, hint_text='Enter your question here', size_hint=(1, None), height = 50)
        layout.add_widget(self.question_input)

        # Ask button
        ask_button = Button(text='Ask', size_hint=(1, None), on_press=self.submit_question, height= 40)
        layout.add_widget(ask_button)

        self.add_widget(layout)

    def update_bg_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def submit_question(self, instance):
        print("Submitting question...")
        # Find user name
        system_name = socket.gethostname()
        # Read any new user data
        with open('user_data/data.json', 'r') as file:
            json_data = file.read()

        data = json.loads(json_data)

        age = data[system_name]["user-info"]["age"]
        gender = data[system_name]["user-info"]["gender"]
        weight = data[system_name]["user-info"]["weight"]
        height = data[system_name]["user-info"]["height"]

        info = [age, gender, weight, height]
        
        # Process the user's question and display the response
        # response = "This is some example test output, we dont wanna use all our tokens This is some example test output, we dont wanna use all our tokens This is some example test output, we dont wanna use all our tokens This is some example test output, we dont wanna use all our tokens This is some example test output, we dont wanna use all our tokens This is some example test output, we dont wanna use all our tokens This is some example test output, we dont wanna use all our tokens This is some example test output, we dont wanna use all our tokens This is some example test output, we dont wanna use all our tokens This is some example test output, we dont wanna use all our tokens This is some example test output, we dont wanna use all our tokens This is some example test output, we dont wanna use all our tokens This is some example test output, we dont wanna use all our tokens This is some example test output, we dont wanna use all our tokens This is some example test output, we dont wanna use all our tokens This is some example test output, we dont wanna use all our tokens This is some example test output, we dont wanna use all our tokens This is some example test output, we dont wanna use all our tokens This is some example test output, we dont wanna use all our tokens This is some example test output, we dont wanna use all our tokens " #
        response = get_response(info, self.question_input.text)
        print("Got response!")
        self.advice_text.text = response