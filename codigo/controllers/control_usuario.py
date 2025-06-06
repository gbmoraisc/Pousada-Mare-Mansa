import sqlite3
from models.usuario import Usuario

class Control_Usuario:
    def __init__(self, conn):
        self.conn = conn

    def criar_tabela(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    senha TEXT NOT NULL
                );
            """)
            self.conn.commit()
            print("✅ Tabela 'usuarios' verificada/criada com sucesso.")
        except sqlite3.Error as erro:
            print(f"❌ Erro ao criar Tabela usuarios: {erro}")

    def adicionar_usuario(self, nome: str, email: str, senha: str):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?);",
            (nome, email, senha)
        )
        self.conn.commit()

    def remover_usuario(self, id: int):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = ?;", (id,))
        self.conn.commit()

    def autenticar(self, nome: str, senha: str):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE nome = ? AND senha = ?;', (nome, senha))
        row = cursor.fetchone()
        if row:
            return Usuario(*row)
        return None

    def listar_usuarios(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM usuarios")
        rows = cursor.fetchall()
        return [{"id": row[0], "nome": row[1], "email": row[2]} for row in rows]
