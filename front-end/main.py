from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from src.database import salvar_roteiro, obter_roteiros
from src.utils import falar, ouvir

class MimheanApp(App):
    def build(self):
        # Layout principal
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Entrada de título
        self.titulo_input = TextInput(hint_text="Título do Roteiro", size_hint_y=None, height=50)
        self.layout.add_widget(self.titulo_input)

        # Entrada de texto
        self.texto_input = TextInput(hint_text="Texto do Roteiro", multiline=True)
        self.layout.add_widget(self.texto_input)

        # Botão para salvar roteiro
        salvar_btn = Button(text="Salvar Roteiro", size_hint_y=None, height=50)
        salvar_btn.bind(on_press=self.salvar)
        self.layout.add_widget(salvar_btn)

        # Botão para ouvir comando
        ouvir_btn = Button(text="Ouvir Comando", size_hint_y=None, height=50)
        ouvir_btn.bind(on_press=self.ouvir_comando)
        self.layout.add_widget(ouvir_btn)

        # Label de resultado
        self.resultado_label = Label(text="", size_hint_y=None, height=50)
        self.layout.add_widget(self.resultado_label)

        return self.layout

    def salvar(self, instance):
        titulo = self.titulo_input.text
        texto = self.texto_input.text
        if titulo and texto:
            salvar_roteiro(titulo, texto)
            self.resultado_label.text = "Roteiro salvo com sucesso!"
            self.titulo_input.text = ""
            self.texto_input.text = ""
        else:
            self.resultado_label.text = "Preencha todos os campos!"

    def ouvir_comando(self, instance):
        comando = ouvir()
        if comando:
            self.resultado_label.text = f"Comando ouvido: {comando}"
        else:
            self.resultado_label.text = "Não foi possível ouvir."

if __name__ == '__main__':
    MimheanApp().run()
