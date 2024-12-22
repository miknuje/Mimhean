from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

Window.size = (400, 600)
class ScreenManager(ScreenManager):
    pass

class MainScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

class RegisterScreen(Screen):
    pass

class Mimhean(App):
    def build(self):
        return ScreenManager()

Mimhean().run()