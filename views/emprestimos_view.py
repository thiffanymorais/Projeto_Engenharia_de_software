import tkinter as tk
from tkinter import messagebox


class EmprestimosView(tk.Toplevel):
    def __init__(self, master, usuario, facade):
        super().__init__(master)
        self.usuario = usuario
        self.facade = facade

        self.title("Biblioteca - Empréstimos e Reservas")
        self.geometry("860x560")
        self.resizable(False, False)

        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (860 // 2)
        y = (self.winfo_screenheight() // 2) - (560 // 2)
        self.geometry(f"860x560+{x}+{y}")

        self.cor_principal = "#0052cc" if usuario.obter_tipo() == "Aluno" else "#28a745"
        self.cor_fundo = "#f5f8ff" if usuario.obter_tipo() == "Aluno" else "#f4fff6"
        self.cor_borda = "#b7d0ff" if usuario.obter_tipo() == "Aluno" else "#b8e6c5"

        self.configure(bg=self.cor_fundo)
        self._criar_layout()
        self._carregar_dados()

    def _criar_layout(self):
        header = tk.Frame(self, bg=self.cor_principal, height=84)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Gerenciamento de Empréstimos",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg=self.cor_principal
        ).pack(pady=(16, 4))

        tk.Label(
            header,
            text=f"{self.usuario.username} • {self.usuario.obter_tipo()}",
            font=("Segoe UI", 10),
            fg="white",
            bg=self.cor_principal
        ).pack()

        container = tk.Frame(self, bg=self.cor_fundo, padx=18, pady=14)
        container.pack(fill=tk.BOTH, expand=True)

        topo = tk.Frame(container, bg=self.cor_fundo)
        topo.pack(fill=tk.X, pady=(0, 10))

        tk.Button(
            topo,
            text="Atualizar Lista",
            command=self._carregar_dados,
            font=("Segoe UI", 10, "bold"),
            bg=self.cor_principal,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            width=16
        ).pack(side=tk.LEFT)

        tk.Button(
            topo,
            text="Fechar",
            command=self.destroy,
            font=("Segoe UI", 10, "bold"),
            bg="#dc3545",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            width=12
        ).pack(side=tk.RIGHT)

        self.canvas = tk.Canvas(container, bg=self.cor_fundo, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg=self.cor_fundo)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _carregar_dados(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self._criar_titulo_secao("Meus Empréstimos Abertos")
        emprestimos = self.facade.listar_emprestimos_abertos(self.usuario)
        if not emprestimos:
            tk.Label(
                self.scroll_frame,
                text="Nenhum livro alugado no momento.",
                font=("Segoe UI", 12, "bold"),
                fg="#444444",
                bg=self.cor_fundo
            ).pack(pady=30)
        else:
            for emprestimo_id, livro, data_emprestimo, data_prevista, dias_extensao in emprestimos:
                self._criar_card_emprestimo(
                    emprestimo_id,
                    livro,
                    data_emprestimo,
                    data_prevista or "-",
                    dias_extensao
                )

        self._criar_titulo_secao("Minhas Reservas Ativas")
        reservas_ativas = self.facade.listar_reservas_ativas(self.usuario)
        if not reservas_ativas:
            tk.Label(
                self.scroll_frame,
                text="Nenhuma reserva ativa no momento.",
                font=("Segoe UI", 10, "bold"),
                fg="#444444",
                bg=self.cor_fundo
            ).pack(anchor="w", pady=(2, 12), padx=6)
        else:
            for reserva_id, livro, data_reserva in reservas_ativas:
                self._criar_card_reserva_ativa(reserva_id, livro, data_reserva)

        self._criar_titulo_secao("Reservas Canceladas (últimas 10)")
        reservas_canceladas = self.facade.listar_reservas_canceladas(self.usuario)
        if not reservas_canceladas:
            tk.Label(
                self.scroll_frame,
                text="Nenhuma reserva cancelada.",
                font=("Segoe UI", 10, "bold"),
                fg="#444444",
                bg=self.cor_fundo
            ).pack(anchor="w", pady=(2, 12), padx=6)
        else:
            for livro, data_reserva, data_cancelamento in reservas_canceladas:
                self._criar_card_reserva_cancelada(livro, data_reserva, data_cancelamento or "-")

    def _criar_titulo_secao(self, texto):
        frame = tk.Frame(self.scroll_frame, bg=self.cor_fundo)
        frame.pack(fill=tk.X, pady=(8, 6))
        tk.Label(
            frame,
            text=texto,
            font=("Segoe UI", 12, "bold"),
            fg=self.cor_principal,
            bg=self.cor_fundo
        ).pack(anchor="w", padx=4)

    def _criar_card_emprestimo(self, emprestimo_id, livro, data_emprestimo, data_prevista, dias_extensao):
        card = tk.Frame(
            self.scroll_frame,
            bg="white",
            highlightbackground=self.cor_borda,
            highlightthickness=2,
            bd=0
        )
        card.pack(fill=tk.X, pady=7, padx=4)

        texto = tk.Frame(card, bg="white", padx=14, pady=12)
        texto.pack(fill=tk.X)

        tk.Label(
            texto,
            text=livro,
            font=("Segoe UI", 11, "bold"),
            fg="#1f1f1f",
            bg="white",
            anchor="w",
            justify="left",
            wraplength=620
        ).pack(anchor="w")

        tk.Label(
            texto,
            text=f"Alugado em: {data_emprestimo}   |   Devolução prevista: {data_prevista}",
            font=("Segoe UI", 9),
            fg="#666666",
            bg="white"
        ).pack(anchor="w", pady=(5, 0))

        tk.Label(
            texto,
            text=f"Dias de extensão usados: {dias_extensao}/15",
            font=("Segoe UI", 9, "bold"),
            fg=self.cor_principal,
            bg="white"
        ).pack(anchor="w", pady=(4, 0))

        acoes = tk.Frame(texto, bg="white")
        acoes.pack(anchor="e", pady=(10, 0))

        tk.Button(
            acoes,
            text="Estender +15 dias",
            command=lambda eid=emprestimo_id: self._estender(eid),
            font=("Segoe UI", 9, "bold"),
            bg=self.cor_principal,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            width=18
        ).pack(side=tk.RIGHT)

    def _estender(self, emprestimo_id):
        sucesso, mensagem = self.facade.estender_emprestimo(self.usuario, emprestimo_id)
        if sucesso:
            messagebox.showinfo("Concluído", mensagem)
            self._carregar_dados()
        else:
            messagebox.showwarning("Atenção", mensagem)

    def _criar_card_reserva_ativa(self, reserva_id, livro, data_reserva):
        card = tk.Frame(
            self.scroll_frame,
            bg="white",
            highlightbackground=self.cor_borda,
            highlightthickness=2,
            bd=0
        )
        card.pack(fill=tk.X, pady=6, padx=4)

        texto = tk.Frame(card, bg="white", padx=14, pady=10)
        texto.pack(fill=tk.X)

        tk.Label(
            texto,
            text=livro,
            font=("Segoe UI", 11, "bold"),
            fg="#1f1f1f",
            bg="white"
        ).pack(anchor="w")

        tk.Label(
            texto,
            text=f"Data da reserva: {data_reserva}",
            font=("Segoe UI", 9),
            fg="#666666",
            bg="white"
        ).pack(anchor="w", pady=(4, 0))

        tk.Button(
            texto,
            text="Cancelar reserva",
            command=lambda rid=reserva_id: self._cancelar_reserva(rid),
            font=("Segoe UI", 9, "bold"),
            bg="#dc3545",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            width=18
        ).pack(anchor="e", pady=(8, 0))

    def _criar_card_reserva_cancelada(self, livro, data_reserva, data_cancelamento):
        card = tk.Frame(
            self.scroll_frame,
            bg="white",
            highlightbackground="#d3d3d3",
            highlightthickness=1,
            bd=0
        )
        card.pack(fill=tk.X, pady=5, padx=4)

        texto = tk.Frame(card, bg="white", padx=14, pady=8)
        texto.pack(fill=tk.X)

        tk.Label(
            texto,
            text=livro,
            font=("Segoe UI", 10, "bold"),
            fg="#3d3d3d",
            bg="white"
        ).pack(anchor="w")

        tk.Label(
            texto,
            text=f"Reservado em: {data_reserva}   |   Cancelado em: {data_cancelamento}",
            font=("Segoe UI", 9),
            fg="#666666",
            bg="white"
        ).pack(anchor="w", pady=(3, 0))

    def _cancelar_reserva(self, reserva_id):
        if not messagebox.askyesno("Confirmar", "Deseja cancelar esta reserva?"):
            return

        sucesso, mensagem = self.facade.cancelar_reserva(self.usuario, reserva_id)
        if sucesso:
            messagebox.showinfo("Concluído", mensagem)
            self._carregar_dados()
        else:
            messagebox.showwarning("Atenção", mensagem)
