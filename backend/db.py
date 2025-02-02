import mysql.connector
from mysql.connector import errorcode
from kivymd.toast import toast

# Configurações de conexão com o MySQL
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
# Script SQL para criação da Base de dados e tabelas
TABLES = {}

TABLES['dados_treinamento'] = (
"""
CREATE TABLE dados_treinamento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    input_utilizador TEXT NOT NULL,
    resposta_esperada TEXT NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
)

TABLES['utilizadores'] = (
    """
    CREATE TABLE IF NOT EXISTS utilizadores (
        id_utilizador INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        senha VARCHAR(255) NOT NULL,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB;
    """
)

TABLES['metricas_modelo'] = (
"""
CREATE TABLE metricas_modelo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_modelo VARCHAR(255) NOT NULL,
    acuracia FLOAT NOT NULL,
    perda FLOAT NOT NULL,
    data_treinamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
)

TABLES['logs_predicoes'] = (
"""
CREATE TABLE logs_predicoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_utilizador INT NOT NULL,
    input_utilizador TEXT NOT NULL,
    resposta_ia TEXT NOT NULL,
    probabilidade FLOAT,
    data_interacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_utilizador) REFERENCES utilizadores (id_utilizador) ON DELETE CASCADE
);
"""
)

TABLES['configuracoes_modelo'] = (
"""
CREATE TABLE configuracoes_modelo (
    id_config INT AUTO_INCREMENT PRIMARY KEY,
    nome_modelo VARCHAR(255) NOT NULL,
    hiperparametros JSON NOT NULL, 
    data_alteracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
"""
)

TABLES['roteiros'] = (
    """
    CREATE TABLE IF NOT EXISTS roteiros (
        id_roteiro INT AUTO_INCREMENT PRIMARY KEY,
        id_utilizador INT NOT NULL,
        titulo VARCHAR(255) NOT NULL,
        conteudo TEXT NOT NULL,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ultima_modificacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (id_utilizador) REFERENCES utilizadores (id_utilizador) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """
)

TABLES['interacoes'] = (
    """
    CREATE TABLE IF NOT EXISTS interacoes (
        id_interacao INT AUTO_INCREMENT PRIMARY KEY,
        id_utilizador INT NOT NULL,
        mensagem_utilizador TEXT NOT NULL,
        resposta_ia TEXT NOT NULL,
        data_interacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_utilizador) REFERENCES utilizadores (id_utilizador) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """
)

TABLES['tarefas_automatizadas'] = (
    """
    CREATE TABLE IF NOT EXISTS tarefas_automatizadas (
        id_tarefa INT AUTO_INCREMENT PRIMARY KEY,
        id_utilizador INT NOT NULL,
        descricao_tarefa VARCHAR(255) NOT NULL,
        comando VARCHAR(255) NOT NULL,
        status ENUM('pendente', 'concluída') DEFAULT 'pendente',
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_utilizador) REFERENCES utilizadores (id_utilizador) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """
)

TABLES['configuracoes'] = (
    """
    CREATE TABLE IF NOT EXISTS configuracoes (
        id_configuracao INT AUTO_INCREMENT PRIMARY KEY,
        id_utilizador INT NOT NULL,
        tipo_configuracao VARCHAR(100) NOT NULL,
        valor TEXT NOT NULL,
        data_alteracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (id_utilizador) REFERENCES utilizadores (id_utilizador) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """
)

TABLES['conversas'] = (
"""
CREATE TABLE IF NOT EXISTS conversas (
    id_conversa INT AUTO_INCREMENT PRIMARY KEY,
    id_utilizador INT NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_utilizador) REFERENCES utilizadores (id_utilizador) ON DELETE CASCADE
);
"""
)

def create_database(cursor):
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS projeto_ia DEFAULT CHARACTER SET 'utf8mb4'")
        print("Base de dados 'projeto_ia' criado ou já existente.")
    except mysql.connector.Error as err:
        print(f"Erro ao criar o Base de dados: {err}")
        exit(1)

def create_tables(cursor):
    for table_name, table_sql in TABLES.items():
        try:
            print(f"Criando tabela {table_name}...")
            cursor.execute(table_sql)
            print(f"Tabela {table_name} criada com sucesso.")
        except mysql.connector.Error as err:
            print(f"Erro ao criar tabela {table_name}: {err}")

def update_tables(cursor):
    string = """
    ALTER TABLE interacoes ADD COLUMN id_conversa INT;
    ALTER TABLE interacoes ADD FOREIGN KEY (id_conversa) REFERENCES conversas (id_conversa) ON DELETE CASCADE;
    """
    try:
        cursor.execute(string)
    except mysql.connector.Error as err:
            print(f"Erro ao alterar tabela interacoes: {err}")

def main():
    try:
        # Conectar ao servidor MySQL
        cnx = mysql.connector.connect(user=config['user'], password=config['password'], host=config['host'])
        cursor = cnx.cursor()

        # Criar Base de dados se não existir
        create_database(cursor)

        # Selecionar o Base de dados
        cnx.database = config['database']
        
        # Criar tabelas
        create_tables(cursor)
        update_tables(cursor)

        # Fechar conexões
        cursor.close()
        cnx.close()
        print("Processo concluído com sucesso!")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro de acesso: Verifique seu utilizador e senha.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Base de dados não encontrado.")
        else:
            print(err)

if __name__ == "__main__":
    main()
