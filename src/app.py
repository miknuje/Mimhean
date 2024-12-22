from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from database import salvar_roteiro, obter_roteiros
from utils import falar, ouvir
from flask import Flask, request, jsonify

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

app = Flask(__name__)

@app.route('/registar_google', methods=['POST'])
def registar_google():
    token = request.json.get('token')
    if not token:
        return jsonify({"message": "Token não fornecido"}), 400
    # Processar o token
    return jsonify({"message": "Registro bem-sucedido com Google"}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

if __name__ == '__main__':
    MimheanApp().run()
