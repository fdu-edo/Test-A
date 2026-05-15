from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

class HomeScreen(Screen):
    pass

class FormScreen(Screen):
    pass

class ListScreen(Screen):
    pass

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(FormScreen(name="form"))
        sm.add_widget(ListScreen(name="list"))
        return sm

MyApp().run()
