from backend.db import *

from backend.db import connect_db

def criar_conversa(id_utilizador, titulo):
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

def salvar_mensagem(id_utilizador, id_conversa, mensagem, resposta):
    """Salva a interação na base de dados."""
    db = connect_db()
    cursor = db.cursor()
    if id_conversa is None:
        # Criar uma nova conversa se não houver uma ativa
        cursor.execute("INSERT INTO conversas (id_utilizador, titulo) VALUES (%s, %s)", (id_utilizador, "Nova Conversa"))
        db.commit()
        id_conversa = cursor.lastrowid
    sql = """
    INSERT INTO interacoes (id_utilizador, id_conversa, mensagem_utilizador, resposta_ia) 
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (id_utilizador, id_conversa, mensagem, resposta))
    db.commit()
    cursor.close()
    db.close()

def carregar_conversas(id_utilizador):
    cnx = connect_db()
    cursor = cnx.cursor(dictionary=True)
    query = "SELECT id_conversa, titulo FROM conversas WHERE id_utilizador = %s"
    cursor.execute(query, (id_utilizador,))
    conversas = cursor.fetchall()
    cursor.close()
    cnx.close()
    return conversas

def carregar_mensagens(id_conversa):
    """Recupera todas as mensagens de uma conversa específica."""
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    sql = "SELECT mensagem_utilizador, resposta_ia, data_interacao FROM interacoes WHERE id_conversa = %s ORDER BY data_interacao"
    cursor.execute(sql, (id_conversa,))
    mensagens = cursor.fetchall()
    cursor.close()
    db.close()
    return mensagens

def salvar_titulo(id_conversa, novo_titulo):
    """Salva o novo título da conversa na base de dados."""
    db = connect_db()
    cursor = db.cursor()
    sql = "UPDATE conversas SET titulo = %s WHERE id_conversa = %s"
    cursor.execute(sql, (novo_titulo, id_conversa))
    db.commit()
    cursor.close()
    db.close()

def excluir_conversa(id_conversa):
    """Exclui uma conversa na base de dados."""
    db = connect_db()
    cursor = db.cursor()
    sql = "DELETE FROM conversas WHERE id_conversa = %s"
    cursor.execute(sql, (id_conversa,))
    db.commit()
    cursor.close()
    db.close()