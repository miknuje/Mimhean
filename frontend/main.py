from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from strings import *
import mysql.connector
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.label import MDLabel
from mysql.connector import errorcode
from kivymd.toast import toast
from kivymd.uix.list import OneLineListItem

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.conversas import carregar_conversas

config = {
    'user': 'root',  # Substitua pelo seu utilizador MySQL
    'password': '',  # Substitua pela sua senha
    'host': 'localhost',  # Ou o IP do servidor MySQL
    'database': 'mimhean',  # Nome da Base de dados
}

def connect_db():
    try:
        return mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            toast("Erro: Utilizador ou senha incorretos")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            toast("Erro: Base de dados não encontrada")
        else:
            toast(f"Erro: {err}")
    return None

Window.size = (400, 600)

class MainMenuScreen(Screen):
    pass

class LoginScreen(Screen):
    def login_user(self):
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()

        if not username or not password:
            toast("Por favor, preencha todos os campos")
            return

        cnx = connect_db()
        if cnx is None:
            return

        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM utilizadores WHERE nome = %s AND senha = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            toast(f"Bem-vindo, {user['nome']}!")
            self.manager.current = "chat"
            app = MDApp.get_running_app()
            app.utilizador_atual = user["id_utilizador"]
        else:
            toast("Utilizador ou senha incorretos")

        cursor.close()
        cnx.close()

class RegisterScreen(Screen):
    def register_user(self):
        email = self.ids.email.text.strip()
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()
        passconf = self.ids.passconf.text.strip()

        if not email or not username or not password or not passconf:
            toast("Por favor, preencha todos os campos")
            return

        if password != passconf:
            toast("As senhas não coincidem")
            return

        cnx = connect_db()
        if cnx is None:
            return

        cursor = cnx.cursor()
        query = "INSERT INTO utilizadores (nome, email, senha) VALUES (%s, %s, %s)"

        try:
            cursor.execute(query, (username, email, password))
            cnx.commit()
            toast("Utilizador registrado com sucesso!")
            self.manager.current = "login"
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DUP_ENTRY:
                toast("Erro: E-mail já registrado")
            else:
                toast(f"Erro ao registrar: {err}")
        finally:
            cursor.close()
            cnx.close()

class ChatScreen(Screen):
    def display_message(self, sender, message):
        """Exibe uma mensagem no chat."""
        chat_history = self.ids.chat_history
        chat_history.add_widget(
            MDLabel(
                text=f"{sender}: {message}",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                halign="left" if sender == "Utilizador" else "right",
                size_hint_y=None,
                height=30,
            )
        )

class Mimhean(MDApp):
    def build(self):
        self.utilizador_atual = None
        self.conversa_atual = None  
        self.theme_cls.font_styles.update({
            "Roboto": ["assets/fonts/Roboto-Regular.ttf", 16, False, 0.15],
            "RobotoBold": ["assets/fonts/Roboto-Bold.ttf", 18, True, 0.15],
        })
        self.title = "Mimhean"
        return Builder.load_string(kv)
    def exibir_conversas(self):
        """Lista todas as conversas do utilizador."""
        id_utilizador = self.app.utilizador_atual  # tenho que salvar
        conversas = self.app.carregar_conversas(id_utilizador)

        lista_conversas = self.ids.lista_conversas  # Criar um ID no layout
        lista_conversas.clear_widgets()

        for conversa in conversas:
            item = OneLineListItem(
                text=conversa["titulo"],
                on_release=lambda x, id_conversa=conversa["id_conversa"]: self.carregar_conversa(id_conversa)
            )
            lista_conversas.add_widget(item)

    def carregar_conversa(self, id_conversa):
        """Carrega mensagens da conversa selecionada."""
        mensagens = self.app.carregar_mensagens(id_conversa)
        chat_history = self.ids.chat_history
        chat_history.clear_widgets()

        for msg in mensagens:
            chat_history.add_widget(
                MDLabel(
                    text=f"Utilizador: {msg['mensagem_utilizador']}\nIA: {msg['resposta_ia']}",
                    size_hint_y=None,
                    height=30,
                    text_color=(1, 1, 1, 1),
                    halign="left"
                )
            )

    def send_message(self):
        """Envia uma mensagem e a salva na conversa ativa."""
        chat_screen = self.root.get_screen("chat")
        user_input = chat_screen.ids.user_input.text.strip()

        if not user_input:
            toast("Digite algo antes de enviar!")
            return

        id_utilizador = self.utilizador_atual
        id_conversa = self.conversa_atual  # Deve ser definido ao abrir uma conversa

        chat_screen.display_message("Utilizador", user_input)
        response = self.get_ai_response(user_input)
        chat_screen.display_message("IA", response)

        # Salvar na base de dados
        self.salvar_mensagem(id_utilizador, id_conversa, user_input, response)

        chat_screen.ids.user_input.text = ""

    def exibir_conversas(self):
        """Lista todas as conversas do utilizador."""
        if not self.utilizador_atual:
            toast("Nenhum utilizador logado")
            return

        conversas = carregar_conversas(self.utilizador_atual)  # Obtém conversas do utilizador atual

        lista_conversas = self.root.get_screen("chat").ids.lista_conversas
        lista_conversas.clear_widgets()

        for conversa in conversas:
            item = OneLineListItem(
                text=conversa["titulo"],
                on_release=lambda x, id_conversa=conversa["id_conversa"]: self.carregar_conversa(id_conversa)
            )
            lista_conversas.add_widget(item)
    
    def get_ai_response(self, user_input):
        """Simula uma resposta da IA."""
        return f"Resposta simulada para: {user_input}"

    def logout(self):
        """Desconecta o utilizador e retorna à tela de login."""
        self.root.current = "login"
        self.root.transition.direction = "right"
        toast("Logout realizado com sucesso!")   
    
if __name__ == '__main__':
    Mimhean().run()