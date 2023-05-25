from kivy.animation import Animation
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.properties import ListProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
import requests
import random
from kivy.uix.widget import Widget

GUI = Builder.load_file('tela.kv')


class Gerenciador(ScreenManager):
    pass


class Menu(Screen):
    def on_pre_enter(self):
        Window.bind(on_request_close=self.confirmacao)

    def confirmacao(self, *args, **kwargs):
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        botoes = BoxLayout(padding=10, spacing=10)

        pop = Popup(title='quer sair?', content=box, size_hint=(None, None), size=(90, 90))
        sim = Botao(text='Sim', on_release=App.get_running_app().stop)
        nao = Botao(text='Não', on_release=pop.dismiss)

        botoes.add_widget(sim)
        botoes.add_widget(nao)
        box.add_widget(botoes)

        animText = Animation(color=(1, 0, 0, 1)) + Animation(color=(0, 0, 0, 1))
        animText.repeat = True
        animText.start(sim)
        anim = Animation(size=(250, 130), duration=0.2, transition='out_back')
        anim.start(pop)
        pop.open()
        return True


class Leilao(Screen):
    obras = {
        'monalisa': Image(source='imgs/monalisa.png', size_hint_y=None, height=200),
        'Noite Estrelada': Image(source='imgs/noite_estrelada.png', size_hint_y=None, height=200),
        'O grito': Image(source='imgs/o_grito.png', size_hint_y=None, height=200)
    }

    chave = list(obras.keys())
    escolha = random.choice(chave)
    obra = obras[escolha]

    def __init__(self, **kwargs):
        super(Leilao, self).__init__(**kwargs)

    def on_pre_enter(self, *args):
        self.ids.box.add_widget(self.obra)
        Window.bind(on_keyboard=self.voltar)

    def voltar(self, window, key, *args):
        if key == 27:
            print('apertou')
            App.get_running_app().root.current = 'menu'
            return True

    def on_pre_leave(self, *args):
        self.ids.box.remove_widget(self.obra)
        Window.unbind(on_keyboard=self.voltar)


class Botao(ButtonBehavior, Label):
    cor2 = ListProperty([155/255, 164/255, 181/255, 1])
    cor = ListProperty([33/255, 42/255, 62/255, 1])

    def __init__(self, **kwargs):
        super(Botao, self).__init__(**kwargs)
        self.atualizar()

    def on_pos(self, *args):
        self.atualizar()

    def on_size(self, *args):
        self.atualizar()

    def on_press(self, *args):
        self.cor, self.cor2 = self.cor2, self.cor

    def on_release(self, *args):
        self.cor, self.cor2 = self.cor2, self.cor

    def on_cor(self, *args):
        self.atualizar()

    def atualizar(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.cor)
            Ellipse(size=(self.height, self.height), pos=self.pos)
            Ellipse(size=(self.height, self.height), pos=(self.x+self.width-self.height, self.y))
            Rectangle(size=(self.width-self.height, self.height), pos=(self.x+self.height/2, self.y))

        

class Cotacoes(Screen):
    moedas = {
        'Dólar': 'USD',
        'Euro': 'EUR',
        'Peso Chileno': 'CLP',
        'Bitcoin': 'BTC',
        'Dogecoin': 'DOGE'
    }
    cotacoes = {

    }
    busca = {

    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        self.ids.box.clear_widgets()
        Window.bind(on_keyboard=self.voltar)

        for key, value in self.moedas.items():
            moeda = Background_Label(text=f"{key}: R${self.pegar_cotacoes(value)}", font_size=15,
                          color=(0, 0, 0, 1))

            self.busca[key] = moeda
            self.cotacoes[moeda] = key
            self.ids.box.add_widget(moeda)

    def voltar(self, window, key, *args):
        if key == 27:
            print('apertou')
            App.get_running_app().root.current = 'menu'
            return True

    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard=self.voltar)

    def pegar_cotacoes(self, moeda):
        link = f"https://economia.awesomeapi.com.br/last/{moeda}-BRL"
        requisicao = requests.get(link)
        dic_requisicao = requisicao.json()
        cotacao = dic_requisicao[f"{moeda}BRL"]["bid"]
        return cotacao

    def buscar(self):
        texto = self.ids.texto.text
        removidos = []
        print(texto)
        print(self.busca)
        print(self.cotacoes)

        if texto in self.busca.keys():
            for moeda in self.busca.values():
                if self.cotacoes[moeda] != texto:
                    self.ids.box.remove_widget(moeda)
                    removidos.append(moeda)

        else:
            self.ids.box.clear_widgets()
            for cotacao in self.cotacoes.keys():
                self.ids.box.add_widget(cotacao)


class Background_Label(Label):
    background_color = ListProperty([203/255, 178/255, 121/255, 1])

    def __init__(self, **kwargs):
        super(Background_Label, self).__init__(**kwargs)
        self.atualizar()

    def on_pos(self, *args):
        self.atualizar()

    def on_size(self, *args):
        self.atualizar()

    def on_background_color(self, *args):
        self.atualizar()

    def atualizar(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.background_color)
            Ellipse(size=(self.height, self.height), pos=self.pos)
            Ellipse(size=(self.height, self.height), pos=(self.x + self.width - self.height, self.y))
            Rectangle(size=(self.width - self.height, self.height),
                      pos=(self.x + self.height / 2, self.y))


class MyApp(App):
    def build(self):
        Window.set_title('myapp')
        Window.size = (375, 667)
        Window.clearcolor = 203/255, 178/255, 121/255, 1
        return Gerenciador()


if __name__ == '__main__':
    MyApp().run()
