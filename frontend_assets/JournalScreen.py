from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
import json

class JournalScreen(Screen):
    def __init__(self, **kwargs):
        super(JournalScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', spacing=5, padding=5)
        with layout.canvas.before:
            Color(0.2, 0.2, 0.2, 0.7)  # Grey color in RGBA format
            self.bg_rect = Rectangle(size=layout.size, pos=layout.pos)

        layout.bind(size=self.update_bg_rect, pos=self.update_bg_rect)

        # Breakfast title
        breakfast_title = Label(text='Breakfast', size_hint_y=None, size_hint_x=None, width=self.width, height=30)
        with breakfast_title.canvas.before:
            Color(0.2, 0.2, 0.2, 0.7)  # Grey color in RGBA format
            self.breakfast_rect = Rectangle(size=breakfast_title.size, pos=breakfast_title.pos)
        breakfast_title.bind(size=self.update_breakfast_rect, pos=self.update_breakfast_rect)
        layout.add_widget(breakfast_title)
        
        # Breakfast text
        self.breakfast_text = Label(text = "", valign='top', size_hint_y=None, size_hint_x=None, width=self.width, text_size=(self.width, None))
        breakfast_scroll = ScrollView(size_hint=(1, 0.3))
        breakfast_scroll.add_widget(self.breakfast_text)
        layout.add_widget(breakfast_scroll)
        self.get_breakfast()

        # Lunch title
        lunch_title = Label(text='Lunch', size_hint_y=None, size_hint_x=None, width=self.width, height=30)
        with lunch_title.canvas.before:
            Color(0.2, 0.2, 0.2, 0.7)  # Grey color in RGBA format
            self.lunch_rect = Rectangle(size=lunch_title.size, pos=lunch_title.pos)
        lunch_title.bind(size=self.update_lunch_rect, pos=self.update_lunch_rect)
        layout.add_widget(lunch_title)
        
        # Lunch text
        self.lunch_text = Label(text="", valign='top', size_hint_y=None, size_hint_x=None, width=self.width, text_size=(self.width, None))
        lunch_scroll = ScrollView(size_hint=(1, 0.3))
        lunch_scroll.add_widget(self.lunch_text)
        layout.add_widget(lunch_scroll)
        self.get_lunch()

        # Dinner title
        dinner_title = Label(text="Dinner", size_hint_y=None, size_hint_x=None, width=self.width, height=30)
        with dinner_title.canvas.before:
            Color(0.2, 0.2, 0.2, 0.7)  # Grey color in RGBA format
            self.dinner_rect = Rectangle(size=dinner_title.size, pos=dinner_title.pos)
        dinner_title.bind(size=self.update_dinner_rect, pos=self.update_dinner_rect)     
        layout.add_widget(dinner_title)

        # Dinner text
        self.dinner_text = Label(text="", valign='top', size_hint_y=None, size_hint_x=None, width=self.width, text_size=(self.width, None))
        dinner_scroll = ScrollView(size_hint=(1, 0.3))
        dinner_scroll.add_widget(self.dinner_text)
        layout.add_widget(dinner_scroll)
        self.get_dinner()

        # Total calories
        layout.add_widget(Label(text='Total calories', size_hint_y=None, size_hint_x=None, width=self.width))

        self.add_widget(layout)

    def update_bg_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
    
    def update_breakfast_rect(self, instance, value):
        self.breakfast_rect.pos = instance.pos
        self.breakfast_rect.size = instance.size
    
    def update_lunch_rect(self, instance, value):
        self.lunch_rect.pos = instance.pos
        self.lunch_rect.size = instance.size

    def update_dinner_rect(self, instance, value):
        self.dinner_rect.pos = instance.pos
        self.dinner_rect.size = instance.size
    
    # A function returning a list of the items eaten for breakfast by the user, in str format
    def get_breakfast(self):
        with open('user_data/breakfast.json') as file:
            breakfast_data = json.load(file)

        breakfast_string = ""
        print(breakfast_data.items())
        for item, value in breakfast_data.items():
            breakfast_string += f"- {item.capitalize()} ({value})\n"

        self.breakfast_text.text = breakfast_string
    
    # A function returning a list of the items eaten for lunch by the user, in str format
    def get_lunch(self):
        with open('user_data/lunch.json') as file:
            lunch_data = json.load(file)

        lunch_string = ""
        print(lunch_data.items())
        for item, value in lunch_data.items():
            lunch_string += f"- {item.capitalize()} ({value})\n"

        self.lunch_text.text = lunch_string
    
    # A function returning a list of the items eaten for dinner by the user, in str format
    def get_dinner(self):
        with open('user_data/dinner.json') as file:
            dinner_data = json.load(file)

        dinner_string = ""
        print(dinner_data.items())
        for item, value in dinner_data.items():
            dinner_string += f"- {item.capitalize()} ({value})\n"

        self.dinner_text.text = dinner_string
