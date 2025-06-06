import tkinter as tk
import datetime
from tkinter import ttk, messagebox
from views.form_agendamento import FormsAgendamento
from controllers.control_agendamento import Control_Agendamento
from controllers.control_quarto import Control_Quarto
from controllers.control_cliente import Control_Cliente
from models.logs_json import LoggerJSON

class TelaAgendamento:
    def __init__(self, root, app, conn):
        self.root = root
        self.app = app
        self.conn = conn

        self.logger = LoggerJSON()
        self.ctr_agendamento = Control_Agendamento(self.conn)
        self.ctr_quarto = Control_Quarto(self.conn)
        self.ctr_cliente = Control_Cliente(self.conn)

        self.root.title("Agendamentos - Pousada Maré Mansa")
        self.root.geometry("900x500")
        self.root.configure(bg='#FCEBD5')

        self.dados = []
        self.criar_interface()
        self.carregar_dados()

    def criar_interface(self):
        # Topo com título
        topo = tk.Frame(self.root, bg='#397A7B', height=60)
        topo.pack(side=tk.TOP, fill=tk.X)
        titulo = tk.Label(topo, text="Agendamentos", bg='#397A7B', fg='white', font=("Helvetica", 18, "bold"))
        titulo.pack(pady=10)

        # Área de pesquisa
        frame_pesquisa = tk.Frame(self.root, bg='#FCEBD5')
        frame_pesquisa.pack(pady=10)

        tk.Label(frame_pesquisa, text="Pesquisar:", bg='#FCEBD5').pack(side=tk.LEFT)
        self.entrada_pesquisa = tk.Entry(frame_pesquisa)
        self.entrada_pesquisa.pack(side=tk.LEFT, padx=5)
        tk.Button(frame_pesquisa, text="Buscar", command=self.buscar_agendamento).pack(side=tk.LEFT)

        # Tabela de agendamentos
        colunas = ("id", "nome", "cpf_cliente", "email", "data_entrada", "data_saida", "quarto_id", "tipo", "preco")
        self.tabela = ttk.Treeview(self.root, columns=colunas, show="headings", height=15)

        nomes_colunas = {
            "id": "ID","nome": "Nome","cpf_cliente": "CPF","email": "Email",
            "data_entrada": "Entrada","data_saida": "Saída",
            "quarto_id": "Quarto","tipo": "Tipo","preco": "Preço (R$)"
        }

        for col in colunas:
            self.tabela.heading(col, text=nomes_colunas[col])
            self.tabela.column(col, anchor=tk.CENTER, width=100)

        self.tabela.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Botões de ação
        frame_botoes = tk.Frame(self.root, bg='#FCEBD5')
        frame_botoes.pack(pady=10)

        tk.Button(frame_botoes, text="Criar", command=self.criar_agendamento).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_botoes, text="Editar", command=self.editar_agendamento).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_botoes, text="Deletar", command=self.deletar_agendamento).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_botoes, text="Atualizar", command=self.carregar_dados).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_botoes, text="Voltar ao Menu", bg="#D9B08C", command=self.voltar_menu).pack(side=tk.LEFT, padx=10)

    def carregar_dados(self):
        self.dados = self.ctr_agendamento.listar_agendamentos()
        self.atualizar_tabela(self.dados)

    def atualizar_tabela(self, dados):
        for i in self.tabela.get_children():
            self.tabela.delete(i)
        for ag in dados:
            # Formatando as datas
            try:
                data_entrada_fmt = datetime.datetime.strptime(ag['data_entrada'][:10], "%Y-%m-%d").strftime("%d-%m-%Y")
            except Exception:
                data_entrada_fmt = ag['data_entrada']

            try:
                data_saida_fmt = datetime.datetime.strptime(ag['data_saida'][:10], "%Y-%m-%d").strftime("%d-%m-%Y")
            except Exception:
                data_saida_fmt = ag['data_saida']

            self.tabela.insert('', tk.END, values=(
                ag['id'],
                ag['nome'],
                ag.get('cpf_cliente', ''),
                ag['email'],
                data_entrada_fmt,
                data_saida_fmt,
                ag['quarto_id'],
                ag.get('tipo', ''),
                f"{ag.get('preco', 0.0):.2f}"
            ))

    def buscar_agendamento(self):
        termo = self.entrada_pesquisa.get().lower()
        filtrados = [ag for ag in self.dados if termo in ag['nome'].lower()]
        self.atualizar_tabela(filtrados)

    def criar_agendamento(self):
        def ao_salvar():
            self.carregar_dados()
        FormsAgendamento(self.root, self.conn, callback_sucesso=ao_salvar)

    def editar_agendamento(self):
        item = self.tabela.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um agendamento para editar.")
            self.logger.registrar("Sistema", "Erro ao editar um agendamento inexistente", "tela_agendamento.py", "WARN")
            return

        item_id = item[0]
        item_index = self.tabela.index(item_id)
        dados_agendamento = self.dados[item_index]

        dados_form = (
            dados_agendamento['id'],
            dados_agendamento['nome'],
            dados_agendamento['data_entrada'],
            dados_agendamento['data_saida'],
            dados_agendamento['cpf_cliente'],
            dados_agendamento['email'],
            dados_agendamento['quarto_id']
        )

        id_quarto_antigo = dados_agendamento["quarto_id"]

        def ao_salvar():
            self.carregar_dados()

        FormsAgendamento(
            self.root,
            self.conn,
            dados_iniciais=dados_form,
            quarto_antigo=id_quarto_antigo,
            callback_sucesso=ao_salvar
        )

        
    def deletar_agendamento(self):
        item = self.tabela.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um agendamento para deletar.")
            self.logger.registrar("Sistema", "Erro ao excluir um agendamento inexistente", "tela_agendamento.py", "WARN")
            return

        item_id = item[0]
        item_index = self.tabela.index(item_id)
        agendamento = self.dados[item_index]
        
        id_quarto = agendamento.get('quarto_id')
        id_agendamento = agendamento.get('id')

        if id_agendamento is None:
            messagebox.showerror("Erro", "ID do agendamento não encontrado.")
            return
        
        if id_quarto is None:
            messagebox.showerror("Erro", "ID do quarto não encontrado.")
            return

        confirm = messagebox.askyesno("Confirmação", "Tem certeza que deseja deletar este agendamento e o cliente associado?")
        if confirm:
            try:
                self.ctr_quarto.atualizar_status_quarto(True, int(id_quarto))
                self.ctr_agendamento.remover_agendamento(id_agendamento)
                messagebox.showinfo("Sucesso", "Agendamento deletado com sucesso!")
                self.logger.registrar("Sistema", f"Agendamento (ID: {id_agendamento}) excluído com sucesso", "tela_agendamento.py", "INFO")
                self.carregar_dados()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao deletar: {e}")

    def voltar_menu(self):
        self.app.abrir_tela_menu()