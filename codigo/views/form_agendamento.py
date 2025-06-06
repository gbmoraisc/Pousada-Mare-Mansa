import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date,datetime

from controllers.control_cliente import Control_Cliente
from controllers.control_tipo import Control_Tipo
from controllers.control_quarto import Control_Quarto
from controllers.control_agendamento import Control_Agendamento
from models.logs_json import LoggerJSON

class FormsAgendamento:
    def __init__(self, parent, conn, dados_iniciais=None, quarto_antigo=None, callback_sucesso=None):
        self.parent = parent
        self.conn = conn
        self.dados_iniciais = dados_iniciais
        self.quarto_antigo = quarto_antigo  # novo atributo
        self.callback_sucesso = callback_sucesso
        
        self.logger = LoggerJSON()
        self.ctr_cliente = Control_Cliente(self.conn)
        self.ctr_quarto = Control_Quarto(self.conn)
        self.ctr_tipo = Control_Tipo(self.conn)
        self.ctr_agendamento = Control_Agendamento(self.conn)

        self.janela = tk.Toplevel(self.parent)
        self.janela.title("Agendamento")
        self.janela.geometry("350x300")
        self.janela.configure(bg="#FCEBD5")
        self.janela.grab_set()

        self._criar_widgets()
        if self.dados_iniciais:
            self._preencher_dados()

    def _criar_widgets(self):
        tk.Label(self.janela, text="CPF:", bg="#FCEBD5").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_cpf = tk.Entry(self.janela)
        self.entry_cpf.grid(row=0, column=1, padx=5, pady=5)
        self.entry_cpf.bind("<FocusOut>", self._buscar_cliente)

        tk.Label(self.janela, text="Nome:", bg="#FCEBD5").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_nome = tk.Entry(self.janela)
        self.entry_nome.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.janela, text="E-mail:", bg="#FCEBD5").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_email = tk.Entry(self.janela)
        self.entry_email.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.janela, text="Entrada:", bg="#FCEBD5").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_check_in = DateEntry(self.janela, date_pattern="dd/mm/yyyy")
        self.entry_check_in.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.janela, text="Saída:", bg="#FCEBD5").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.entry_check_out = DateEntry(self.janela, date_pattern="dd/mm/yyyy")
        self.entry_check_out.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self.janela, text="Quarto:", bg="#FCEBD5").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        quartos = self.ctr_quarto.listar_quartos() or []
        quartos_disponiveis = [str(q["numero"]) for q in quartos if q.get("disponibilidade", True)]
        self.entry_quarto = ttk.Combobox(self.janela, values=quartos_disponiveis, state="readonly")
        self.entry_quarto.grid(row=5, column=1, padx=5, pady=5)

        tk.Button(self.janela, text="Salvar", command=self._salvar).grid(row=6, column=0, padx=5, pady=10, sticky="e")
        tk.Button(self.janela, text="Cancelar", command=self.janela.destroy).grid(row=6, column=1, padx=5, pady=10, sticky="w")

    def _preencher_dados(self):
        id_ag, nome, entrada, saida, cpf, email, numero_quarto = self.dados_iniciais  # type: ignore
        self.entry_cpf.insert(0, cpf)
        self.entry_nome.insert(0, nome)
        self.entry_email.insert(0, email)
        
        # Aqui o ajuste:
        try:
            data_entrada = datetime.strptime(entrada, "%d/%m/%Y")
        except ValueError:
            data_entrada = datetime.strptime(entrada, "%Y-%m-%d")
        self.entry_check_in.set_date(data_entrada)
        
        try:
            data_saida = datetime.strptime(saida, "%d/%m/%Y")
        except ValueError:
            data_saida = datetime.strptime(saida, "%Y-%m-%d")
        self.entry_check_out.set_date(data_saida)
        
        self.entry_quarto.set(str(numero_quarto))

    def _buscar_cliente(self, event=None):
        cpf = self.entry_cpf.get().strip()
        if cpf:
            cliente = self.ctr_cliente.buscar_cliente_por_cpf(cpf)
            if cliente:
                self.entry_nome.delete(0, tk.END)
                self.entry_email.delete(0, tk.END)
                self.entry_nome.insert(0, cliente['nome'])
                self.entry_email.insert(0, cliente['email'])
            else:
                messagebox.showinfo("Aviso", "Cliente não encontrado.")

    def _salvar(self):
        cpf = self.entry_cpf.get().strip()
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        numero_quarto_str = self.entry_quarto.get().strip()

        if not (cpf and nome and email and numero_quarto_str):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        try:
            numero_quarto = int(numero_quarto_str)
            data_atual = date.today()
            data_entrada = datetime.strptime(self.entry_check_in.get(), "%d/%m/%Y").date()
            data_saida = datetime.strptime(self.entry_check_out.get(), "%d/%m/%Y").date()

            if data_saida <= data_entrada:
                messagebox.showerror("Erro", "A data de saída deve ser após a data de entrada.")
                return

            if data_entrada < data_atual:
                messagebox.showerror("Erro", "A data de entrada já passou!")
                return

            if data_saida < data_atual:
                messagebox.showerror("Erro", "A data de saída já passou!")
                return

            quarto = self.ctr_quarto.buscar_quarto_por_numero(numero_quarto)
            if not quarto:
                messagebox.showerror("Erro", "Quarto não encontrado.")
                return

            # Se estiver cadastrando (sem dados iniciais), verifica disponibilidade
            if not self.dados_iniciais and not quarto['disponibilidade']:
                messagebox.showerror("Erro", "Quarto não está disponível.")
                return

            cliente_existente = self.ctr_cliente.buscar_cliente_por_cpf(cpf)
            if not cliente_existente:
                self.ctr_cliente.adicionar_cliente(cpf, nome, email)

            if self.dados_iniciais:
                id_agendamento = self.dados_iniciais[0]
                self.ctr_agendamento.atualizar_agendamento(
                    id_agendamento, data_entrada, data_saida, cpf, numero_quarto
                )
                # Atualiza status quartos se mudou o quarto
                if self.quarto_antigo and self.quarto_antigo != numero_quarto:
                    self.ctr_quarto.atualizar_status_quarto(True, self.quarto_antigo)  # libera antigo
                    self.ctr_quarto.atualizar_status_quarto(False, numero_quarto)      # bloqueia novo
            else:
                self.ctr_agendamento.adicionar_agendamento(
                    data_entrada, data_saida, cpf, numero_quarto
                )
                self.ctr_quarto.atualizar_status_quarto(False, numero_quarto)  # bloqueia quarto novo

            messagebox.showinfo("Sucesso", "Agendamento salvo com sucesso!")

            if self.callback_sucesso:
                self.callback_sucesso()
            self.janela.destroy()

        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
