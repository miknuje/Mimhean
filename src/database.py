import mysql.connector
import hashlib
import uuid
from google.oauth2 import id_token
from google.auth.transport import requests

# Configuração da conexão ao MySQL
def conectar(usar_bd=True):
    if usar_bd:
        return mysql.connector.connect(
            host="localhost",  # Alterar se necessário
            user="root",       # Utilizador padrão do MySQL
            password="",       # Alterar se tiver senha configurada
            database="mimhean_db"  # Nome da base de dados
        )
    else:
        return mysql.connector.connect(
            host="localhost",  # Alterar se necessário
            user="root",       # Utilizador padrão do MySQL
            password=""        # Alterar se tiver senha configurada
        )

# Função para criar a base de dados e tabelas
def inicializar_bd():
    try:
        # Conecta sem especificar o banco de dados
        conexao = conectar(usar_bd=False)
        cursor = conexao.cursor()

        # Criação da base de dados
        cursor.execute("CREATE DATABASE IF NOT EXISTS mimhean_db")

        # Agora conecta ao banco criado para criar as tabelas
        cursor.close()
        conexao.close()
        conexao = conectar()
        cursor = conexao.cursor()

        # Tabela para roteiros
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS roteiros (
                id INT AUTO_INCREMENT PRIMARY KEY,
                titulo VARCHAR(255) NOT NULL,
                texto TEXT NOT NULL,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabela para utilizadores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS utilizadores (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                pass VARCHAR(255) NOT NULL,
                google_id VARCHAR(255),
                reset_token VARCHAR(255),
                preferencia_interacao ENUM('texto', 'voz') DEFAULT 'texto'
            )
        ''')

        conexao.commit()
        print("Base de dados inicializada com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

def registar_utilizador(nome, email, senha):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # Gerar hash da senha
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()

        query = "INSERT INTO utilizadores (nome, email, pass) VALUES (%s, %s, %s)"
        valores = (nome, email, senha_hash)
        cursor.execute(query, valores)
        conexao.commit()

        print("Utilizador registado com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro ao registar utilizador: {err}")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

def login_utilizador(email, senha):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # Gerar hash da senha para comparação
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()

        query = "SELECT id, nome FROM utilizadores WHERE email = %s AND pass = %s"
        cursor.execute(query, (email, senha_hash))
        resultado = cursor.fetchone()

        if resultado:
            print(f"Bem-vindo, {resultado[1]}!")
            return resultado  # Retorna o ID e nome do utilizador
        else:
            print("Credenciais inválidas.")
            return None
    except mysql.connector.Error as err:
        print(f"Erro ao fazer login: {err}")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

def gerar_token_reset(email):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # Gerar token único
        token = str(uuid.uuid4())

        query = "UPDATE utilizadores SET reset_token = %s WHERE email = %s"
        cursor.execute(query, (token, email))
        conexao.commit()

        if cursor.rowcount > 0:
            print(f"Token de reset gerado: {token}")
            return token  # Retorne o token para enviar por e-mail
        else:
            print("E-mail não encontrado.")
            return None
    except mysql.connector.Error as err:
        print(f"Erro ao gerar token: {err}")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

def redefinir_senha(token, nova_senha):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # Gerar hash da nova senha
        nova_senha_hash = hashlib.sha256(nova_senha.encode()).hexdigest()

        query = "UPDATE utilizadores SET pass = %s, reset_token = NULL WHERE reset_token = %s"
        cursor.execute(query, (nova_senha_hash, token))
        conexao.commit()

        if cursor.rowcount > 0:
            print("Senha redefinida com sucesso!")
            return True
        else:
            print("Token inválido.")
            return False
    except mysql.connector.Error as err:
        print(f"Erro ao redefinir senha: {err}")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

GOOGLE_CLIENT_ID = "seu_client_id_do_google"

def login_google(google_token):
    try:
        # Verificar o token recebido do cliente
        idinfo = id_token.verify_oauth2_token(google_token, requests.Request(), GOOGLE_CLIENT_ID)

        if 'email' in idinfo:
            email = idinfo['email']

            conexao = conectar()
            cursor = conexao.cursor()

            # Verificar se o utilizador já existe
            cursor.execute("SELECT id, nome FROM utilizadores WHERE email = %s", (email,))
            resultado = cursor.fetchone()

            if resultado:
                print(f"Bem-vindo de volta, {resultado[1]}!")
                return resultado  # Login bem-sucedido
            else:
                # Registrar novo utilizador com Google
                query = "INSERT INTO utilizadores (nome, email, google_id) VALUES (%s, %s, %s)"
                valores = (idinfo['name'], email, idinfo['sub'])
                cursor.execute(query, valores)
                conexao.commit()
                print(f"Novo utilizador criado: {idinfo['name']}")
                return cursor.lastrowid  # ID do novo utilizador
    except ValueError as err:
        print(f"Erro ao validar token do Google: {err}")
        return None
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

# Função para salvar um novo roteiro
def salvar_roteiro(titulo, texto):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        query = "INSERT INTO roteiros (titulo, texto) VALUES (%s, %s)"
        valores = (titulo, texto)
        cursor.execute(query, valores)
        conexao.commit()

        print("Roteiro salvo com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro ao salvar roteiro: {err}")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

# Função para obter todos os roteiros
def obter_roteiros():
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        query = "SELECT id, titulo, texto, data_criacao FROM roteiros ORDER BY data_criacao DESC"
        cursor.execute(query)
        resultados = cursor.fetchall()

        roteiros = []
        for id, titulo, texto, data_criacao in resultados:
            roteiros.append({
                "id": id,
                "titulo": titulo,
                "texto": texto,
                "data_criacao": data_criacao
            })

        return roteiros
    except mysql.connector.Error as err:
        print(f"Erro ao obter roteiros: {err}")
        return []
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

# Testando a inicialização da base de dados
if __name__ == '__main__':
    inicializar_bd()
