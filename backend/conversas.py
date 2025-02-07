from backend.db import *

def criar_conversa(self, id_utilizador, titulo):
    """Cria uma nova conversa e retorna seu ID."""
    db = connect_db()
    cursor = db.cursor()
    sql = "INSERT INTO conversas (id_utilizador, titulo) VALUES (%s, %s)"
    cursor.execute(sql, (id_utilizador, titulo))
    db.commit()
    conversa_id = cursor.lastrowid
    cursor.close()
    db.close()
    return conversa_id

def salvar_mensagem(self, id_utilizador, id_conversa, mensagem, resposta):
    """Salva a interação no base de dados."""
    db = connect_db()
    cursor = db.cursor()
    sql = """
    INSERT INTO interacoes (id_utilizador, id_conversa, mensagem_utilizador, resposta_ia) 
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (id_utilizador, id_conversa, mensagem, resposta))
    db.commit()
    cursor.close()
    db.close()

def carregar_conversas(self, id_utilizador):
    """Recupera todas as conversas do utilizador."""
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    sql = "SELECT id_conversa, titulo, data_criacao FROM conversas WHERE id_utilizador = %s ORDER BY data_criacao DESC"
    cursor.execute(sql, (id_utilizador,))
    conversas = cursor.fetchall()
    cursor.close()
    db.close()
    return conversas

def carregar_mensagens(self, id_conversa):
    """Recupera todas as mensagens de uma conversa específica."""
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    sql = "SELECT mensagem_utilizador, resposta_ia, data_interacao FROM interacoes WHERE id_conversa = %s ORDER BY data_interacao"
    cursor.execute(sql, (id_conversa,))
    mensagens = cursor.fetchall()
    cursor.close()
    db.close()
    return mensagens
