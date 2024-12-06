from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from database import salvar_roteiro, obter_roteiros
from utils import falar, ouvir

class MimheanApp(App):
    def build(self):
        return Interface()

class Interface(BoxLayout):
    def salvar(self):
        titulo = self.ids.titulo_input.text
        texto = self.ids.texto_input.text
        if titulo and texto:
            salvar_roteiro(titulo, texto)
            self.ids.resultado_label.text = "Roteiro salvo com sucesso!"
            self.ids.titulo_input.text = ""
            self.ids.texto_input.text = ""
        else:
            self.ids.resultado_label.text = "Preencha todos os campos!"

    def ouvir_comando(self):
        comando = ouvir()
        if comando:
            self.ids.resultado_label.text = f"Comando ouvido: {comando}"
        else:
            self.ids.resultado_label.text = "Não foi possível ouvir."

if __name__ == '__main__':
    MimheanApp().run()
