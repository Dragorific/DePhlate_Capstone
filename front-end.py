import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.clock import Clock
from kivy.core.window import Window
from tqdm import tqdm
import time
from openAIAPI import get_response
import subprocess
import json

QUESTION = ""

class MyApp(App):
    def build(self):
        # Create the root widget
        root_widget = MyGridLayout()

        # Return the root widget
        return root_widget


class AIAdvice(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Health Advice"
        self.size_hint = (0.9,0.9)

        self.form_layout = GridLayout(cols=1)
               
        self.advice_text = Label(text= QUESTION, halign='center', valign='top', size_hint_y=None, height=500, text_size=(self.width*7, None))
        self.advice_scrollview = ScrollView(size_hint=(0.8, 0.8))
        self.advice_scrollview.add_widget(self.advice_text)
        self.form_layout.add_widget(self.advice_scrollview)


        # Add a TextInput for the user to input their question
        self.question_input = TextInput(multiline=False, hint_text='Enter your question here', size_hint_y=None, height=50)
        self.form_layout.add_widget(self.question_input)

        # Add a Button to submit the question
        self.submit_button = Button(text='Submit', size_hint_y=None, height=50, on_press=self.submit_question)
        self.form_layout.add_widget(self.submit_button)

        self.add_widget(self.form_layout)
        

    def submit_question(self, instance):
        # Read any new user data
        with open('data.txt', 'r') as file:
            json_data = file.read()

        data = json.loads(json_data)

        age = data["user-info"]["age"]
        gender = data["user-info"]["gender"]
        weight = data["user-info"]["weight"]
        height = data["user-info"]["height"]

        info = [age, gender, weight, height]
        
        # Process the user's question and display the response
        response = get_response(info, self.question_input.text)
        self.advice_text.text = response

class SettingsForm(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Settings"
        self.size_hint = (0.8, 0.6)

        self.form_layout = GridLayout(cols=2)

        # Add the "Age" field
        self.form_layout.add_widget(Label(text="Age"))
        self.age_input = Spinner(
            text='Select Age',
            values=["{:02d}".format(x) for x in range(16,81)],
            size_hint=(None, None),
            size=(200, 50)
        )
        self.form_layout.add_widget(self.age_input)

        # Add the "Weight" field
        self.form_layout.add_widget(Label(text="Weight"))
        self.weight_input = Spinner(
            text='Select Weight in Pounds(lbs)',
            values=["{:02d}".format(x) for x in range(80, 300, 2)],
            size_hint=(None, None),
            size=(200, 50)
        )
        self.form_layout.add_widget(self.weight_input)

        # Add the "Gender" field
        self.form_layout.add_widget(Label(text="Gender"))
        self.gender_input = Spinner(
            text='Select Gender',
            values=['Male', 'Female'],
            size_hint=(None, None),
            size=(200, 50)
        )
        self.form_layout.add_widget(self.gender_input)

        # Add the "Height" field
        self.form_layout.add_widget(Label(text="Height"))
        self.height_input = Spinner(
            text='Select Height in cm',
            values=["{:02d}".format(x) for x in range(140, 200, 5)],
            size_hint=(None, None),
            size=(200, 50)
        )
        self.form_layout.add_widget(self.height_input)

        # Add the "Submit" button
        self.submit_button = Button(text="Submit", font_size=16)
        self.submit_button.bind(on_press=self.save_form_data)

        # Add a BoxLayout to center the "Submit" button
        button_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        button_box.add_widget(Label())
        button_box.add_widget(self.submit_button)
        button_box.add_widget(Label())
        self.form_layout.add_widget(button_box)

        self.add_widget(self.form_layout)

    def save_form_data(self, instance):
        data = {
            "user-id": "test_id_123",
            "user-info": 
            {
                "age": self.age_input.text,
                "weight": self.weight_input.text,
                "gender": self.gender_input.text,
                "height": self.height_input.text,
            }
        }

        # Save the data to a text file in JSON format
        with open("data.txt", "w") as f:
            f.write(json.dumps(data))
            f.write("\n")
            f.close()
            
        data = json.loads(json_data)    

        # Close the popup
        self.dismiss()
    
# Main Parent Grid Layout -> contains the primary app components
class MyGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1

        # Add the logo
        self.logo = Image(source="assets/logo.png")
        self.add_widget(self.logo)

        self.logo2 = Image(source="assets/logoo.png")
        self.add_widget(self.logo2)
        
        # Add the title
        self.title = Label(text="DePhlate AI Diet Tracker", font_size=40)
        self.add_widget(self.title)

        # Load the background image using a rectangle
        with self.canvas.before:
            self.background = Image(source="assets/dephlate_bg2.jpg").texture
            self.rect = Rectangle(size=self.size, pos=self.pos, texture=self.background)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Add the "Start" button
        # self.start_button = Button(text="Start", font_size=40, size_hint=(None, 1), width=300, size_hint_x=0.4)
        # self.start_button.bind(on_press=self.open_program)
        cam_icon ='assets/cam.png'
        cam_image = Image(source=cam_icon)
        self.start_button = Button(background_normal=cam_icon, font_size=40, size_hint=(0.125 , 2), size=cam_image.texture_size)
        self.start_button.bind(on_press=self.open_program)

        # Add the "Settings" button
        # self.settings_button = Button(text="Settings", font_size=40, size_hint=(None, 1), width=300, size_hint_x=0.4)
        # self.settings_button.bind(on_press=self.open_settings)
        gear_icon ='assets/gear.png'
        gear_image = Image(source=gear_icon)
        self.settings_button = Button(background_normal=gear_icon, font_size=40, size_hint=(0.125 , 2), size=gear_image.texture_size)
        self.settings_button.bind(on_press=self.open_settings)


        # Add the "Health Adivce" button
        chat_icon ='assets/chaticon.png'
        chat_image = Image(source=chat_icon)
        self.advice_button = Button(background_normal=chat_icon, font_size=40, size_hint=(0.125 , 2), size=chat_image.texture_size)
        self.advice_button.bind(on_press=self.open_AIAdvice)
        

        # Create a BoxLayout to center the two buttons horizontally
        button_box = BoxLayout(orientation='horizontal', size_hint_y=0.3, width=self.width, spacing=20)
        button_box.padding = (50, 0, 50, 20)             # Set the left and right padding to 50 pixels, (left, top, right, bottom)
        button_box.add_widget(self.start_button)
        button_box.add_widget(self.settings_button)
        button_box.add_widget(self.advice_button)
        button_box.align = 'center'                     # Set the align property to center the buttons horizontally
        self.add_widget(button_box)

    def open_program(self, instance):
        subprocess.Popen(['python', 'camera_stream.py'])

    def open_settings(self, instance):
        form = SettingsForm()
        form.open()

    def open_AIAdvice(self, instance):
        form = AIAdvice()
        form.open()
        
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loading_gif = AsyncImage(source="./assets/load1.gif", anim_delay=0.1)
        self.add_widget(self.loading_gif)

    def on_enter(self):
        Clock.schedule_once(self.fake_loading, 0.5)

    def fake_loading(self, dt):
        for _ in tqdm(range(100), desc="Loading..."):
            time.sleep(0.02)
        self.manager.current = "main"

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "main"
        self.add_widget(MyGridLayout())

class MyKivyApp(App):
    def build(self):
        # Set the size of the window to 800x600
        Window.size = (500, 800)
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(LoadingScreen(name="loading"))
        sm.add_widget(MainScreen())
        return sm

if __name__ == "__main__":
    with open('data.txt', 'r') as file:
        json_data = file.read()

    data = json.loads(json_data)

    age = data["user-info"]["age"]
    weight = data["user-info"]["weight"]
    gender = data["user-info"]["gender"]
    height = data["user-info"]["height"]

    MyKivyApp().run()