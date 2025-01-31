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

config = {
    'user': 'root',  # Substitua pelo seu utilizador MySQL
    'password': '',  # Substitua pela sua senha
    'host': 'localhost',  # Ou o IP do servidor MySQL
    'database': 'mimhean',  # Nome do Base de dados
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
            toast("Usuário registrado com sucesso!")
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
        self.theme_cls.font_styles.update({
            "Roboto": ["assets/fonts/Roboto-Regular.ttf", 16, False, 0.15],
            "RobotoBold": ["assets/fonts/Roboto-Bold.ttf", 18, True, 0.15],
        })
        self.title = "Mimhean"
        return Builder.load_string(kv)
    
    def send_message(self):
        """Envia uma mensagem para o chat."""
        chat_screen = self.root.get_screen("chat")
        user_input = chat_screen.ids.user_input.text.strip()

        if not user_input:
            toast("Digite algo antes de enviar!")
            return

        chat_screen.display_message("Utilizador", user_input)
        response = self.get_ai_response(user_input)
        chat_screen.display_message("IA", response)
        chat_screen.ids.user_input.text = ""

    def get_ai_response(self, user_input):
        """Simula uma resposta da IA."""
        return f"Resposta simulada para: {user_input}"

    def show_commands(self):
        """Mostra os comandos disponíveis na tela."""
        commands = [
            "Olá - Gera uma saudação",
            "Ajuda - Mostra a lista de comandos",
            "Sair - Encerra a sessão",
        ]

        command_list = self.root.get_screen("chat").ids.command_list
        command_list.clear_widgets()

        for command in commands:
            command_list.add_widget(
                MDLabel(
                    text=f"- {command}",
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    size_hint_y=None,
                    height=30,
                )
            )

    def logout(self):
        """Desconecta o utilizador e retorna à tela de login."""
        self.root.current = "login"
        self.root.transition.direction = "right"
        toast("Logout realizado com sucesso!")
        
    
if __name__ == '__main__':
    Mimhean().run()