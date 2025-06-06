class Control_Tipo:
    def __init__(self, conn):
        self.conn = conn

    def criar_tabela(self):
        """Cria a tabela tipos no banco (se não existir)"""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tipos (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                preco REAL NOT NULL
            )
        """)
        self.conn.commit()

    def adicionar_tipo(self, tipo_id: int, nome: str, preco: float):
        """Adiciona um novo tipo de quarto"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO tipos (id, nome, preco) VALUES (?, ?, ?)",
            (tipo_id, nome, preco)
        )
        self.conn.commit()

    def remover_tipo(self, tipo_id: int):
        """Remove um tipo pelo ID"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM tipos WHERE id = ?", (tipo_id,))
        self.conn.commit()

    def listar_tipos(self):
        """Lista todos os tipos cadastrados"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tipos")
        rows = cursor.fetchall()
        return [{"id": row[0], "nome": row[1], "preco": row[2]} for row in rows]
