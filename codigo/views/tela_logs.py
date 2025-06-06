import tkinter as tk
import json
from models.logs_json import LoggerJSON
from tkinter import ttk

class TelaLogs:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.root.title("Relatório de Atividades")
        self.root.geometry("750x450")
        self.root.configure(bg='#FAF1E4')
        self.logger = LoggerJSON()

        # Estilo ttk customizado
        style = ttk.Style(self.root)
        style.theme_use('clam')  # tema mais moderno para Treeview
        style.configure("Treeview",
                        background="#FFFFFF",
                        foreground="#333333",
                        rowheight=25,
                        fieldbackground="#FAF1E4",
                        font=('Segoe UI', 10))
        style.map('Treeview', background=[('selected', '#8FBF9F')], foreground=[('selected', 'black')])

        # Título
        titulo = tk.Label(self.root, text="Relatório de Atividades", font=("Segoe UI", 18, "bold"), bg="#FAF1E4", fg="#3A7765")
        titulo.pack(pady=(20, 10))

        # Frame para a tabela e scrollbar
        frame_tabela = tk.Frame(self.root, bg='#FAF1E4')
        frame_tabela.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)

        # Colunas
        colunas = ("data", "usuario", "acao", "tela", "tipo")
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show='headings')

        # Configuração das colunas e títulos
        nomes_colunas = {
            "data": "Data / Hora",
            "usuario": "Usuário",
            "acao": "Ação",
            "tela": "Tela",
            "tipo": "Tipo"
        }
        for col in colunas:
            self.tree.heading(col, text=nomes_colunas[col])
            # Ajusta largura de cada coluna de forma proporcional
            if col == "acao":
                self.tree.column(col, width=220, anchor=tk.W)
            elif col == "data":
                self.tree.column(col, width=140, anchor=tk.CENTER)
            else:
                self.tree.column(col, width=110, anchor=tk.CENTER)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Botão de voltar com hover e cores melhores
        btn_voltar = tk.Button(self.root, text="Voltar ao Menu", bg="#3A7765", fg="white",
                              font=("Segoe UI", 12, "bold"), relief=tk.FLAT, command=self.voltar_menu, cursor="hand2")
        btn_voltar.pack(pady=(10, 25), ipadx=15, ipady=7)

        self.carregar_logs()

    def carregar_logs(self):
        try:
            with open("logs.json", "r", encoding="utf-8") as f:
                logs = json.load(f)
                # Limpa tabela antes de carregar
                for item in self.tree.get_children():
                    self.tree.delete(item)

                for log in logs:
                    self.tree.insert('', tk.END, values=(log["data"], log["usuario"], log["acao"], log["tela"], log["tipo"]))
        except FileNotFoundError:
            self.logger.registrar("Sistema", "Erro ao carregar o arquivo JSON", "tela_logs.py", "ERROR")

    def voltar_menu(self):
        self.app.voltar_menu()
