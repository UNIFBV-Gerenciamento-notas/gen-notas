import os
import sqlite3

def conectar_bd():
    try:
        pasta_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_banco = os.path.join(pasta_atual, 'alunos.db')
        conexao = sqlite3.connect(caminho_banco)
        return conexao, conexao.cursor()
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None, None

def criar_banco():
    try:
        pasta_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_banco = os.path.join(pasta_atual, 'alunos.db')
        conexao = sqlite3.connect(caminho_banco)
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                nota1 REAL NOT NULL,
                nota2 REAL NOT NULL,
                media REAL NOT NULL
            );
        """)

        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao criar banco: {e}")
    finally:
        conexao.close()

def inserir_aluno(nome, nota1, nota2):
    try:
        media = (nota1 + nota2) / 2
        conexao, cursor = conectar_bd()
        if not conexao:
            return

        cursor.execute("""
            INSERT INTO alunos (nome, nota1, nota2, media)
            VALUES (?, ?, ?, ?)
        """, (nome, nota1, nota2, media))

        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inserir aluno: {e}")
    finally:
        if conexao:
            conexao.close()

def listar_alunos():
    try:
        conexao, cursor = conectar_bd()
        if not conexao:
            return []

        cursor.execute("SELECT * FROM alunos")
        resultados = cursor.fetchall()
        return resultados
    except sqlite3.Error as e:
        print(f"Erro ao listar alunos: {e}")
        return []
    finally:
        if conexao:
            conexao.close()

def buscar_por_id(id_aluno):
    try:
        conexao, cursor = conectar_bd()
        if not conexao:
            return None

        cursor.execute("SELECT * FROM alunos WHERE id = ?", (id_aluno,))
        resultado = cursor.fetchone()
        return resultado
    except sqlite3.Error as e:
        print(f"Erro ao buscar aluno por ID: {e}")
        return None
    finally:
        if conexao:
            conexao.close()

def buscar_por_nome(nome):
    try:
        conexao, cursor = conectar_bd()
        if not conexao:
            return []

        cursor.execute("SELECT * FROM alunos WHERE nome = ?", (nome,))
        resultados = cursor.fetchall()
        return resultados
    except sqlite3.Error as e:
        print(f"Erro ao buscar alunos por nome: {e}")
        return []
    finally:
        if conexao:
            conexao.close()

def atualizar_notas(id_aluno, nova_nota1, nova_nota2):
    try:
        media = (nova_nota1 + nova_nota2) / 2
        conexao, cursor = conectar_bd()
        if not conexao:
            return

        cursor.execute("""
            UPDATE alunos
            SET nota1 = ?, nota2 = ?, media = ?
            WHERE id = ?
        """, (nova_nota1, nova_nota2, media, id_aluno))

        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao atualizar notas: {e}")
    finally:
        if conexao:
            conexao.close()

def remover_aluno(id_aluno):
    try:
        conexao, cursor = conectar_bd()
        if not conexao:
            return

        cursor.execute("DELETE FROM alunos WHERE id = ?", (id_aluno,))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao remover aluno: {e}")
    finally:
        if conexao:
            conexao.close()