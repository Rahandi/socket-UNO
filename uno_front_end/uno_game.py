from kivy.app import App
from kivy.uix.label import Label
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

class LoginPage(Screen):
    user_id = 1
    def change_screen(self, *args):
        if self.user_id == 1:
            App.get_running_app().root.current = "start_page"
        else:
            App.get_running_app().root.current = "waiting_page"

class WaitingPage(Screen):
    pass

class StartPage(Screen):
    pass

class GamePage(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

# Config.set('kivy','window_icon','path/to/icon.ico')

game = Builder.load_file("uno.kv")

class MainGame(App):
    def build(self):
        return game

if __name__ == "__main__":
    MainGame().run()