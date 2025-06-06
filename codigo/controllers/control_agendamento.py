from datetime import date
from typing import List, Dict
import sqlite3

class Control_Agendamento:
    def __init__(self, conn):
        self.conn = conn

    def criar_tabela(self) -> None:
        """Cria a tabela agendamentos no banco (se não existir)"""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agendamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_entrada TEXT NOT NULL,
                data_saida TEXT NOT NULL,
                cliente_cpf TEXT NOT NULL,
                numero_quarto INTEGER NOT NULL,
                FOREIGN KEY (cliente_cpf) REFERENCES clientes(cpf),
                FOREIGN KEY (numero_quarto) REFERENCES quartos(numero_quarto)
            );
        """)
        self.conn.commit()

    def adicionar_agendamento(self, data_entrada: date, data_saida: date, cpf: str, numero_quarto: int) -> int:
        """Adiciona um novo agendamento e retorna o id criado"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO agendamentos (data_entrada, data_saida, cliente_cpf, numero_quarto) VALUES (?, ?, ?, ?)",
            (data_entrada, data_saida, cpf, numero_quarto)
        )
        self.conn.commit()
        return cursor.lastrowid

    def remover_agendamento(self, agendamento_id: int) -> None:
        """Remove um agendamento pelo ID"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM agendamentos WHERE id = ?", (agendamento_id,))
        self.conn.commit()

    def listar_agendamentos(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT a.id,c.nome AS cliente_nome, c.cpf AS cliente_cpf, c.email AS cliente_email, 
            a.data_entrada, a.data_saida, a.numero_quarto, t.nome AS tipo_quarto, t.preco AS preco_quarto
            FROM agendamentos a JOIN clientes c ON a.cliente_cpf = c.cpf JOIN quartos q ON a.numero_quarto = q.numero_quarto
            JOIN tipos t ON q.tipo_id = t.id
        """)

        resultados = cursor.fetchall()

        # Nome das colunas em ordem
        colunas = ["id", "nome", "cpf_cliente", "email", "data_entrada", "data_saida", "quarto_id", "tipo", "preco"]

        # Transforma em lista de dicionários
        return [dict(zip(colunas, linha)) for linha in resultados]

    def carregar_dados(self) -> List[Dict]:
        """Carrega dados formatados para a interface"""
        agendamentos = self.listar_agendamentos()
        dados_formatados = []
        for ag in agendamentos:
            dados_formatados.append({
                "id": ag["id"],
                "nome": ag["cliente_nome"],
                "data": f"{ag['data_entrada']} a {ag['data_saida']}",
                "quarto": f"{ag['numero_quarto']} - {ag['tipo_quarto']}"
            })
        return dados_formatados

    def atualizar_agendamento(self, id_agendamento: int, data_entrada: date, data_saida: date, cpf: str, numero_quarto: int) -> None:
        """Atualiza os dados do agendamento pelo ID"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE agendamentos
            SET data_entrada = ?, data_saida = ?, cliente_cpf = ?, numero_quarto = ?
            WHERE id = ?
        """, (data_entrada, data_saida, cpf, numero_quarto, id_agendamento))
        self.conn.commit()

    def verificar_disponibilidade(self, numero_quarto: int, data_entrada: date, data_saida: date, ignorar_id: int) -> bool:
        cursor = self.conn.cursor()
        query = """
            SELECT COUNT(*) FROM agendamentos 
            WHERE numero_quarto = ?
            AND data_saida > ?
            AND data_entrada < ?
        """
        params = [numero_quarto, data_entrada, data_saida]
        if ignorar_id:
            query += " AND id != ?"
            params.append(ignorar_id)

        cursor.execute(query, params)
        return cursor.fetchone()[0] == 0
