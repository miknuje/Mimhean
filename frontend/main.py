import re
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from strings import *
import mysql.connector
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from mysql.connector import errorcode
from kivymd.toast import toast
from kivymd.uix.list import OneLineListItem, MDList
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.uix.scrollview import ScrollView
import bcrypt
import g4f
from kivy.metrics import dp

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.conversas import carregar_conversas, criar_conversa, salvar_mensagem, salvar_titulo, excluir_conversa, carregar_mensagens

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
        query = "SELECT * FROM utilizadores WHERE nome = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user['senha'].encode('utf-8')):
                toast(f"Bem-vindo, {user['nome']}!")
                self.manager.current = "chat"
                app = MDApp.get_running_app()
                app.utilizador_atual = user["id_utilizador"]

                chat_screen = self.manager.get_screen("chat")
                chat_screen.carregar_conversas()
            else:
                toast("Utilizador ou senha incorretos")
        else:
            toast("Utilizador ou senha incorretos")

        cursor.close()
        cnx.close()

class RegisterScreen(Screen):
    def register_user(self):
        email = self.ids.email.text.strip()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            toast("Por favor, insira um e-mail válido.")
            return
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
        password = self.ids.password.text.strip()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor = cnx.cursor()
        query = "INSERT INTO utilizadores (nome, email, senha) VALUES (%s, %s, %s)"
        
        try:
            cursor.execute(query, (username, email, hashed_password))
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
    dialog = None

    def on_enter(self, *args):
        self.carregar_conversas()

    def editar_titulo(self, id_conversa, titulo_atual):
        self.dialog = MDDialog(
            title="Editar Título",
            type="custom",
            content_cls=MDTextField(text=titulo_atual),
            buttons=[
                MDRaisedButton(text="Cancelar", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(
                    text="Salvar",
                    on_release=lambda x: self.salvar_titulo(id_conversa, self.dialog.content_cls.text)
                )
            ]
        )
        self.dialog.open()

    def excluir_conversa(self, id_conversa):
        excluir_conversa(id_conversa)
        self.carregar_conversas()

    def salvar_titulo(self, id_conversa, novo_titulo):
        """Atualiza o título da conversa no banco de dados."""
        salvar_titulo(id_conversa, novo_titulo)
        self.dialog.dismiss()
        self.carregar_conversas()

    def enviar_mensagem(self):
        """Captura a mensagem do usuário, envia para a IA e exibe a resposta."""
        user_input = self.ids.user_input.text.strip()
        if not user_input:
            return

        id_conversa = self.ids.chat_screen.id_conversa 
        resposta_ia = "Resposta gerada pela IA..." 

        salvar_mensagem(self.id_utilizador, id_conversa, user_input, resposta_ia)

        # Exibir no chat
        self.display_message("Utilizador", user_input)
        self.display_message("IA", resposta_ia)

        # Limpar campo de entrada
        self.ids.user_input.text = ""

    def display_message(self, sender, message):
        """Exibe uma mensagem no chat com balão ajustável e responsivo."""
        chat_history = self.ids.chat_history  # MDBoxLayout que contém as mensagens
        scroll_view = self.ids.scroll_view  # ScrollView que contém o MDBoxLayout

        is_user = sender == "Utilizador"  # Verifica se a mensagem é do usuário

        # Container da mensagem
        message_container = MDBoxLayout(
            size_hint_x=None,
            width=dp(300),  # Largura máxima do balão
            padding=[10, 5],
            adaptive_height=True,
            pos_hint={"right": 1} if is_user else {"left": 0}  # Alinha à direita ou esquerda
        )

        # Balão da mensagem
        bubble = MDCard(
            elevation=2,
            radius=[15, 15, 0, 15] if is_user else [15, 15, 15, 0],  # Bordas arredondadas
            md_bg_color=(0.2, 0.6, 1, 1) if is_user else (0.2, 0.2, 0.2, 1),  # Cor do balão
            padding=[10, 10],
            size_hint_x=None,
            width=dp(280),  # Largura do balão
            adaptive_height=True
        )

        # Texto da mensagem
        message_label = MDLabel(
            text=message,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),  # Cor do texto
            halign="right" if is_user else "left",  # Alinhamento do texto
            size_hint_x=None,
            width=dp(260),  # Largura do texto
            size_hint_y=None,
            adaptive_height=True
        )

        # Adiciona o texto ao balão
        bubble.add_widget(message_label)
        # Adiciona o balão ao container
        message_container.add_widget(bubble)
        # Adiciona o container ao histórico de chat
        chat_history.add_widget(message_container)

        # Rola o histórico para a última mensagem
        scroll_view.scroll_to(message_container)

    def carregar_conversas(self):
        """Carrega a lista de conversas disponíveis no menu lateral."""
        app = MDApp.get_running_app()
        if not app.utilizador_atual:
            toast("Nenhum utilizador logado")
            return

        lista_conversas = self.ids.lista_conversas
        lista_conversas.clear_widgets()  # Limpa a lista de conversas atual

        # Carrega as conversas do banco de dados
        conversas = carregar_conversas(app.utilizador_atual)

        for conversa in conversas:
            box = MDBoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=48,
                spacing=2,
                padding=[2, 0]
            )

            # Botão para exibir a conversa
            btn = MDRaisedButton(
                text=conversa["titulo"],
                size_hint_x=0.6,
                on_release=lambda x, id_conversa=conversa["id_conversa"]: app.exibir_conversa(id_conversa),
                md_bg_color=(94/255, 107/255, 145/255, 1),
                text_color=(1, 1, 1, 1)
            )

            # Botão para editar o título da conversa
            btn_editar = MDIconButton(
                icon="pencil",
                size_hint_x=0.1,
                on_release=lambda x, id_conversa=conversa["id_conversa"], titulo=conversa["titulo"]: self.editar_titulo(id_conversa, titulo),
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )

            # Botão para excluir a conversa
            btn_excluir = MDIconButton(
                icon="delete",
                size_hint_x=0.1,
                on_release=lambda x, id_conversa=conversa["id_conversa"]: self.excluir_conversa(id_conversa),
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )

            # Adiciona os botões ao BoxLayout
            box.add_widget(btn)
            box.add_widget(btn_editar)
            box.add_widget(btn_excluir)

            # Adiciona o BoxLayout à lista de conversas
            lista_conversas.add_widget(box)

    def carregar_conversa(self, id_conversa):
        """Carrega mensagens da conversa selecionada."""        
        mensagens = carregar_mensagens(id_conversa)

        self.conversa_atual = id_conversa

        chat_history = self.ids.chat_history
        chat_history.clear_widgets()

        for msg in mensagens:
            chat_history.add_widget(
                MDLabel(
                    text=f"Utilizador: {msg['mensagem_utilizador']}\nMimhean: {msg['resposta_ia']}",
                    size_hint_y=None,
                    height=30,
                    text_color=(1, 1, 1, 1),
                    halign="left"
                )
            )

    def exibir_conversa(self, id_conversa):
        """Exibe as mensagens de uma conversa específica na tela de chat."""
        self.conversa_atual = id_conversa
        mensagens = carregar_mensagens(id_conversa)  # Carrega as mensagens do banco de dados

        chat_screen = self.root.get_screen("chat")
        chat_screen.ids.chat_history.clear_widgets()  # Limpa o histórico de chat

        for msg in mensagens:
            chat_screen.display_message("Utilizador", msg["mensagem_utilizador"])  # Exibe a mensagem do usuário
            chat_screen.display_message("IA", msg["resposta_ia"])  # Exibe a resposta do bot


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

    def exibir_conversa(self, id_conversa):
        """Exibe as mensagens de uma conversa específica na tela de chat."""
        self.conversa_atual = id_conversa
        mensagens = carregar_mensagens(id_conversa)  # Carrega as mensagens do banco de dados

        chat_screen = self.root.get_screen("chat")
        chat_screen.ids.chat_history.clear_widgets()  # Limpa o histórico de chat

        for msg in mensagens:
            chat_screen.display_message("Utilizador", msg["mensagem_utilizador"])  # Exibe a mensagem do usuário
            chat_screen.display_message("IA", msg["resposta_ia"])  # Exibe a resposta do bot

    def carregar_conversa(self, id_conversa):
        """Carrega mensagens da conversa selecionada."""        
        mensagens = carregar_mensagens(id_conversa)

        chat_screen = self.root.get_screen("chat")
        chat_screen.carregar_conversa(id_conversa)
        self.conversa_atual = id_conversa
 
        chat_history = chat_screen.ids.chat_history
        chat_history.clear_widgets()

        for msg in mensagens:
            chat_history.add_widget(
                MDLabel(
                    text=f"Utilizador: {msg['mensagem_utilizador']}\nMimhean: {msg['resposta_ia']}",
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

        if not self.conversa_atual:
            self.conversa_atual = criar_conversa(self.utilizador_atual, "Nova Conversa")

        chat_screen.display_message("Utilizador", user_input)

        response = self.get_ai_response(user_input)
        chat_screen.display_message("IA", response)

        self.salvar_mensagem(self.utilizador_atual, self.conversa_atual, user_input, response)
        carregar_conversas(self.utilizador_atual) 
        chat_screen.ids.user_input.text = ""

    def salvar_mensagem(self, id_utilizador, id_conversa, mensagem, resposta):
        """Salva a interação na base de dados.""" 
              
        salvar_mensagem(id_utilizador, id_conversa, mensagem, resposta)

    def salvar_titulo(self, id_conversa, novo_titulo):
        """Salva o novo titulo na base de dados."""        
        salvar_titulo(id_conversa, novo_titulo)

    def get_ai_response(self, user_input):
        try:
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4,
                messages=[{"role": "user", "content": user_input}]
            )
            return response
        except Exception as e:
            toast(f"Erro ao gerar resposta: {str(e)}")
            return "Desculpe, ocorreu um erro ao processar sua mensagem."
    
    def nova_conversa(self):
        """Cria uma nova conversa e atualiza o menu."""
        app = MDApp.get_running_app()
        if not app.utilizador_atual:
            toast("Nenhum utilizador logado")
            return

        titulo = "Nova Conversa"
        id_nova_conversa = criar_conversa(app.utilizador_atual, titulo)

        # Atualiza a conversa atual
        self.conversa_atual = id_nova_conversa

        chat_screen = self.root.get_screen("chat")
        chat_screen.carregar_conversas()
        self.carregar_conversa(id_nova_conversa)

    def logout(self):
        """Desconecta o utilizador e retorna à tela de login."""        
        self.root.current = "login"
        self.root.transition.direction = "right"
        toast("Logout realizado com sucesso!")   
        self.utilizador_atual = None
        self.conversa_atual = None

if __name__ == '__main__':
    Mimhean().run()