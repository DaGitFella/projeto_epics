from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView

class Gerenciador(ScreenManager):
    pass

class Menu(Screen):
    pass


class Tarefas(Screen):
    def __init__(self, tarefas=[], **kwargs):  # keyword arguments letra = 'a'
        super().__init__(**kwargs)
        for tarefa in tarefas:
            self.ids.box.add_widget(Tarefa(text=tarefa))

    '''eventos da tela
        on_enter
        on_pre_enter
        on_pre_leave'''

    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltar) #captura evento de teclado

    def voltar(self, window, key, *args):
        if key == 27:
            App.get_running_app().root.current = 'menu' #get_running_app() - retorna o app que está rodando(test app)
            # print(key) - retorna o valor da tecla
            return True # o evento de teclado é capturado e não mais é passado para outros eventos

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)

    def addwidget(self):
        texto = self.ids.text.text
        self.ids.box.add_widget(Tarefa(text=texto))
        self.ids.text.text = ''

class Tarefa(BoxLayout):
    def __init__(self, text='bababoi', **kwargs):
        super().__init__(**kwargs)
        self.ids.cancelar.text = text


class test(App):
    def build(self):
        Window.clearcolor = 203 / 255, 178 / 255, 121 / 255, 1
        return Gerenciador()
            # Tarefas(['fazer compras', 'matar o Bolsonaro', 'matar o L','pedra','sjaij','ok viado lixo'])


if __name__ == "__main__":
    test().run()
