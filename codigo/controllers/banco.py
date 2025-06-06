import os
import sqlite3

from .control_tipo import Control_Tipo
from .control_quarto import Control_Quarto
from .control_cliente import Control_Cliente
from .control_agendamento import Control_Agendamento
from .control_usuario import Control_Usuario
from models.logs_json import LoggerJSON

class Banco:
    def __init__(self, nome_banco='pousada.db'):
        self.logger = LoggerJSON()
        self.conn = None
        self.nome_banco = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", nome_banco)

    def conectar(self):
        try:
            self.conn = sqlite3.connect(self.nome_banco)
            self.logger.registrar("Sistema", "Conexão estabelecida com sucesso.", "banco.py", "INFO")
        except sqlite3.Error as erro:
            self.logger.registrar("Sistema", "Erro ao conectar com o banco de dados", "banco.py", "ERROR")
            print(f"❌ Erro ao conectar ao banco: {erro}")
            raise

    def desconectar(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.logger.registrar("Sistema", "Conexão encerrada.", "banco.py", "INFO")

    def criar_tabelas(self):
        if self.conn:
            self.control_usuario = Control_Usuario(self.conn)
            self.control_usuario.criar_tabela()

            self.control_tipo = Control_Tipo(self.conn)
            self.control_tipo.criar_tabela()

            self.control_quarto = Control_Quarto(self.conn)
            self.control_quarto.criar_tabela()

            self.control_cliente = Control_Cliente(self.conn)
            self.control_cliente.criar_tabela()

            self.control_agendamento = Control_Agendamento(self.conn)
            self.control_agendamento.criar_tabela()

            if not self.control_tipo.listar_tipos():
                self.logger.registrar("Sistema", "Inserindo tipos de quartos iniciais..", "banco.py", "INFO")
                self.control_tipo.adicionar_tipo(1, "Quarto Solteiro", 100.00)
                self.control_tipo.adicionar_tipo(2, "Quarto Casal", 150.00)
                self.control_tipo.adicionar_tipo(3, "Suíte", 250.00)

            if not self.control_quarto.listar_quartos():
                # Andar 1 - quartos 101 a 106 (solteiro)
                for numero in range(101, 107):
                    self.control_quarto.adicionar_quarto(numero, True, 2, 1)

                # Andar 2 - quartos 201 a 206 (casal)
                for numero in range(201, 207):
                    self.control_quarto.adicionar_quarto(numero, True, 4, 2)

                # Andar 3 - quartos 301 a 306 (suíte)
                for numero in range(301, 307):
                    self.control_quarto.adicionar_quarto(numero, True, 6, 3)

                    self.logger.registrar("Sistema", "Dados iniciais de quartos inseridos.", "banco.py", "INFO")
        else:
            self.logger.registrar("Sistema", "Conexão não estabelecida.", "banco.py", "INFO")
