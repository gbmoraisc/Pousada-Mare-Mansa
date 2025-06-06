import sqlite3

class Control_Quarto:
    def __init__(self, conn):
        self.conn = conn

    def criar_tabela(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quartos (
                numero_quarto INTEGER PRIMARY KEY,
                disponibilidade INTEGER NOT NULL,
                capacidade INTEGER NOT NULL,
                tipo_id INTEGER NOT NULL
            )
        ''')
        self.conn.commit()

    def adicionar_quarto(self, numero_quarto: int, disponivel: bool, capacidade: int, tipo_id: int):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO quartos (numero_quarto, disponibilidade, capacidade, tipo_id) VALUES (?, ?, ?, ?)",
            (numero_quarto, int(disponivel), capacidade, tipo_id)
        )
        self.conn.commit()

    def remover_quarto(self, numero_quarto: int):
        """Remove um quarto pelo número"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM quartos WHERE numero_quarto = ?", (numero_quarto,))
        self.conn.commit()

    def listar_quartos(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT numero_quarto, disponibilidade, capacidade, tipo_id FROM quartos")
        resultado = cursor.fetchall()
        quartos = [{"numero": row[0], "disponibilidade": row[1], "capacidade": row[2], "tipo_id": row[3]} for row in resultado]
        quartos_disponiveis = [q for q in quartos if q["disponibilidade"] == 1]
        return quartos_disponiveis

    def atualizar_status_quarto(self, disponivel: bool, numero_quarto: int):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE quartos SET disponibilidade = ? WHERE numero_quarto = ?",
            (int(disponivel), numero_quarto)
        )
        self.conn.commit()
    
    def buscar_quarto_por_numero(self, id_quarto: int):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT numero_quarto, disponibilidade, capacidade, tipo_id FROM quartos WHERE numero_quarto = ?", 
            (id_quarto,) 
        )
        row = cursor.fetchone()
        if row:
            return {
                "numero": row[0],
                "disponibilidade": row[1],
                "capacidade": row[2],
                "tipo_id": row[3]
            }
        else:
            return None
