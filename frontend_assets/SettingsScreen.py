from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from plot import gen_plots
import json
import socket

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.form_layout = GridLayout(cols=1)

        with self.form_layout.canvas.before:
            Color(0.2, 0.2, 0.2, 0.7)  # Grey color in RGBA format
            self.bg_rect = Rectangle(size=self.form_layout.size, pos=self.form_layout.pos)
        
        self.form_layout.bind(size=self.update_bg_rect, pos=self.update_bg_rect)

        # Add the "Age" field
        age_layout = GridLayout(cols=2, size_hint_y=None, height=50)
        age_layout.add_widget(Label(text="Age", valign='middle'))
        self.age_input = Spinner(
            text='Select Age',
            values=["{:02d}".format(x) for x in range(16, 81)],
            size_hint=(None, None),
            size=(200, 50)
        )
        age_layout.add_widget(self.age_input)
        self.form_layout.add_widget(age_layout)

        # Add the "Weight" field
        weight_layout = GridLayout(cols=2, size_hint_y=None, height=50)
        weight_layout.add_widget(Label(text="Weight", valign='middle'))
        self.weight_input = Spinner(
            text='Select Weight in Pounds(lbs)',
            values=["{:02d}".format(x) for x in range(80, 300, 2)],
            size_hint=(None, None),
            size=(200, 50)
        )
        weight_layout.add_widget(self.weight_input)
        self.form_layout.add_widget(weight_layout)

        # Add the "Gender" field
        gender_layout = GridLayout(cols=2, size_hint_y=None, height=50)
        gender_layout.add_widget(Label(text="Gender", valign='middle'))
        self.gender_input = Spinner(
            text='Select Gender',
            values=['Male', 'Female'],
            size_hint=(None, None),
            size=(200, 50)
        )
        gender_layout.add_widget(self.gender_input)
        self.form_layout.add_widget(gender_layout)

        # Add the "Height" field
        height_layout = GridLayout(cols=2, size_hint_y=None, height=50)
        height_layout.add_widget(Label(text="Height", valign='middle'))
        self.height_input = Spinner(
            text='Select Height in cm',
            values=["{:02d}".format(x) for x in range(140, 200, 5)],
            size_hint=(None, None),
            size=(200, 50)
        )
        height_layout.add_widget(self.height_input)
        self.form_layout.add_widget(height_layout)

        # Add the "Submit" button
        self.submit_button = Button(text="Submit", font_size=16, size_hint_y=None, height=50)
        self.submit_button.bind(on_press=self.save_form_data)
        self.form_layout.add_widget(self.submit_button)

        self.form_layout.add_widget(Widget(size_hint_y=None, height=150))

        self.statistics_button = Button(text="Show Statistics", font_size=16, size_hint_y=None, height=40, width=320)
        self.statistics_button.bind(on_press=self.open_statistics)
        self.form_layout.add_widget(self.statistics_button)

        self.add_widget(self.form_layout)

    def update_bg_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def open_statistics(self, instance):
        # do something
        gen_plots()

        # Create the images
        title = Label(text="Today's Statistics:", font_size=16, height=30)
        image1 = Image(source="user_data/calories.png")
        image2 = Image(source="user_data/macros.png")

        # Create a layout for the popup
        popup_layout = GridLayout(cols=1)
        popup_layout.add_widget(title)
        popup_layout.add_widget(image1)
        popup_layout.add_widget(image2)

        # Create the popup and add the layout
        statistics_popup = Popup(title="Statistics", content=popup_layout, size_hint=(0.8, 0.8))

        # Open the popup
        statistics_popup.open()

    def save_form_data(self, instance):
        system_name = socket.gethostname()
        filename = "user_data/data.json"

        # Read the existing data from the file
        try:
            with open(filename, "r") as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = {}

        # Check if the os_name is already in the data, and if not, create a new entry
        if system_name not in existing_data:
            existing_data[system_name] = {
                "user-info": {
                    "age": self.age_input.text,
                    "weight": self.weight_input.text,
                    "gender": self.gender_input.text,
                    "height": self.height_input.text,
                }
            }

        # Save the updated data to the file
        with open(filename, "w") as f:
            json.dump(existing_data, f)
            print("Information written...")