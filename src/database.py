import mysql.connector

# Configuração da conexão ao MySQL
def conectar():
    return mysql.connector.connect(
        host="localhost",  # Alterar se necessário
        user="root",       # Usuário padrão do MySQL
        password="",       # Alterar se tiver senha configurada
        database="mimhean_db"  # Certifique-se de usar o nome correto da base de dados
    )

# Função para criar a base de dados e tabelas
def inicializar_bd():
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # Criação da base de dados
        cursor.execute("CREATE DATABASE IF NOT EXISTS mimhean_db")
        cursor.execute("USE mimhean_db")

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
                preferencia_interacao ENUM('texto', 'voz') DEFAULT 'texto'
            )
        ''')

        conexao.commit()
        print("Base de dados inicializada com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")
    finally:
        if conexao.is_connected():
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
        if conexao.is_connected():
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
        if conexao.is_connected():
            cursor.close()
            conexao.close()

# Testando a inicialização da base de dados
if __name__ == '__main__':
    inicializar_bd()
