from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.lang.builder import Builder
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
import sqlite3
from kivy.metrics import dp
from kivymd.uix.datatables import  MDDataTable
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
Window.size = (700,700)
from kivymd.uix.dialog import MDDialog
screen_manager = """

ScreenManager:
    FirstPage:
    HomePage:
    Passcodepage:




<FirstPage>
    name: "first"
    MDLabel:
        text: "Welcome Back, Boss!"
        pos_hint : {"center_x" : 0.5, "center_y" : 0.8}
        font_color : "blue"
        halign : "center"
        font_style : "H5"

    MDTextField:
        id : user_box
        hint_text : "Enter Your Username"
        helper_text : "Enter Name"
        helper_text_mode : "on_focus"
        pos_hint : {"center_x" : 0.5, "center_y": 0.6}
        size_hint_x : None
        width : 300

    MDTextField:
        id : passthing
        hint_text : "Enter Your Passcode"
        helper_text : "Enter Passcode"
        helper_text_mode : "on_focus"
        pos_hint : {"center_x" : 0.5, "center_y": 0.5}
        size_hint_x : None
        width : 300

    MDRaisedButton:
        id : disabled_check
        text : "Verify Yourselves"
        disabled : False
        pos_hint : {"center_x" : 0.5, "center_y" : 0.3}
        halign : "center"
        on_press : app.user_name_check()


    MDRaisedButton:
        id : disabled
        text : "Login Here!"
        disabled : True
        pos_hint : {"center_x" : 0.5, "center_y" : 0.2}
        halign : "center"
        on_press : root.manager.current = "home"

    MDRaisedButton:
        id : disabled1
        text : "Show Records"
        disabled : True
        pos_hint : {"center_x" : 0.5, "center_y" : 0.1}
        halign : "center"
        on_press : root.manager.current = "passcode"

<HomePage>
    name : "home"
    MDBoxLayout:
        orientation : "vertical"
        MDToolbar:
            title : "Personal Password Manager!"
            anchor_title : "center"
            ad_bg_color : "Blue"
        Widget:

    MDLabel:
        id : label
        text : ""
        pos_hint : {"center_x" : 0.5, "center_y" : 0.7}
        halign: "center"
        font_color : "Blue"

    MDTextField:
        id : username
        hint_text : "Enter Organisation"
        helper_text : "Enter Name of Organisation"
        helper_text_mode : "on_focus"
        pos_hint: {"center_x" : 0.5, "center_y": 0.6}
        size_hint_x : None
        width : 300
    MDTextField:
        id : password
        hint_text : "Enter Password"
        helper_text : "Enter Name of Password"
        helper_text_mode : "on_focus"
        pos_hint: {"center_x" : 0.5, "center_y": 0.5}
        size_hint_x : None
        width : 300
    MDRaisedButton:
        text : "Save Into Db"
        pos_hint : {"center_x" : 0.5, "center_y" : 0.4}
        on_press : app.add_user_db()
    MDRaisedButton:
        text : "Back"
        pos_hint : {"center_x" : 0.1, "center_y" : 0.95}
        on_press : root.manager.current = "first"
    MDRaisedButton:
        text : "Show Records"
        pos_hint : {"center_x" : 0.9, "center_y" : 0.95}
        on_press : root.manager.current = "passcode"



<Passcodepage>
    name: "passcode"
    MDBoxLayout:
        orientation : "vertical"
        MDToolbar:
            title : "Saved Records"
            anchor_title : "center"
            ad_bg_clor : "Navy"
        Widget:
    MDRaisedButton:
        text : "Back"
        pos_hint : {"center_x" : 0.1, "center_y" : 0.95}
        on_press : root.manager.current = "first"



"""


class FirstPage(Screen):
    pass

class HomePage(Screen):
    pass

class Passcodepage(Screen):
    def load_table(self):
        layout = AnchorLayout()
        connection = sqlite3.connect("first.db")
        c = connection.cursor()
        c.execute("SELECT * FROM data")
        results = c.fetchall()
        c.execute("SELECT COUNT(*) FROM data")
        length_of_table = c.fetchall()
        i = 0
        self.data_tables = MDDataTable(
            pos_hint={'center_y': 0.5, 'center_x': 0.5},
            size_hint=(0.9, 0.6),
            use_pagination=True,
            check=False,
            column_data=[
                ("No.", dp(30)),
                ("Organisation", dp(30)),
                ("Password", dp(30))],
            row_data=[
                (f"{i + 1}", f"{word[0]}", f"{word[1]}")
                for word in results], )
        self.add_widget(self.data_tables)
        return layout

    def on_enter(self):
        self.load_table()



screen = ScreenManager()
screen.add_widget(FirstPage(name = "first"))
screen.add_widget(HomePage(name = "home"))
screen.add_widget(Passcodepage(name = "passcode"))

class FirstApp(MDApp):
    def build(self):
        connection = sqlite3.connect("first.db")
        c = connection.cursor()
        c.execute(""" CREATE TABLE if not exists data(name text, passccode text)""")
        connection.commit()
        connection.close()
        self.strng = Builder.load_string(screen_manager)
        return self.strng

    def open_error_box1(self):
        self.dialog = MDDialog(title = "Invalid Username and Password", pos_hint = {"center_x" : 0.5, "center_y" : 0.5}, text = "Enter Correct Credentials")
        self.dialog.open()

    def user_name_check(self):
        self.text_user = self.strng.get_screen("first").ids.user_box.text
        print(self.text_user)
        if self.text_user == "Salman":
            self.strng.get_screen("first").ids.disabled.disabled = False
            self.strng.get_screen("first").ids.disabled1.disabled =  False
        else:
            self.open_error_box1()

    def add_user_db(self):
        self.text_userapp = self.strng.get_screen("home").ids.username.text
        self.text_passcode = self.strng.get_screen("home").ids.password.text
        connection = sqlite3.connect('first.db')
        c = connection.cursor()
        c.execute("INSERT INTO data VALUES (:name, :passcode)",{
        'name' : self.text_userapp,
        'passcode' : self.text_passcode
        })
        connection.commit()
        connection.close()
        self.strng.get_screen("home").ids.label.text = "Records Added"
        self.strng.get_screen("home").ids.username.text = ""
        self.strng.get_screen("home").ids.password.text = ""







if __name__ == "__main__":
    FirstApp().run()
