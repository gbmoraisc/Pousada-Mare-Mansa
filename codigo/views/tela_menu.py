import tkinter as tk

class TelaMenu:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.root.title("Menu Principal - Pousada Maré Mansa")
        self.root.geometry("600x400")
        self.root.configure(bg="#FAF1E4")

        # Cabeçalho
        topo = tk.Frame(self.root, bg="#397A7B", height=60)
        topo.pack(fill=tk.X)
        tk.Label(topo, text="Menu Principal", font=("Helvetica", 20, "bold"), bg="#397A7B", fg="white").pack(pady=15)

        # Corpo
        corpo = tk.Frame(self.root, bg="#FAF1E4")
        corpo.pack(expand=True)

        estilo_botao = {
            "font": ("Helvetica", 14),
            "width": 25,
            "bg": "#397A7B",
            "fg": "white",
            "activebackground": "#2E5F50",
            "activeforeground": "white",
            "bd": 0,
            "highlightthickness": 0,
            "cursor": "hand2",
            "relief": tk.FLAT,
            "pady": 10
        }

        tk.Button(corpo, text="📅 Gerenciar Agendamentos", command=self.app.abrir_agendamentos, **estilo_botao).pack(pady=10)
        tk.Button(corpo, text="📊 Visualizar Relatório", command=self.app.abrir_logs, **estilo_botao).pack(pady=10)
        tk.Button(corpo, text="❌ Sair", command=self.app.sair, **estilo_botao).pack(pady=10)
        
        # Rodapé
        rodape = tk.Frame(self.root, bg="#397A7B", height=40)
        rodape.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(rodape, text="Pousada Maré Mansa © 2025", bg="#397A7B", fg="white", font=("Helvetica", 10)).pack(pady=10)