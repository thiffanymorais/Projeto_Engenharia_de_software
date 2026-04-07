import tkinter as tk
from tkinter import messagebox


class CatalogoView(tk.Toplevel):
    def __init__(self, master, usuario, recomendacoes, catalogo_completo, facade):
        super().__init__(master)
        self.usuario = usuario
        self.recomendacoes = recomendacoes
        self.catalogo_completo = catalogo_completo
        self.facade = facade

        self.title("Biblioteca - Acervo de Livros")
        self.geometry("920x620")
        self.resizable(False, False)

        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (920 // 2)
        y = (self.winfo_screenheight() // 2) - (620 // 2)
        self.geometry(f"920x620+{x}+{y}")

        self.cor_principal = "#0052cc" if usuario.obter_tipo() == "Aluno" else "#28a745"
        self.cor_fundo = "#f5f8ff" if usuario.obter_tipo() == "Aluno" else "#f4fff6"
        self.cor_card = "#eaf2ff" if usuario.obter_tipo() == "Aluno" else "#e9f9ee"
        self.cor_borda = "#b7d0ff" if usuario.obter_tipo() == "Aluno" else "#b8e6c5"

        self.configure(bg=self.cor_fundo)

        self._criar_header()
        self._criar_conteudo()

    def _criar_header(self):
        header = tk.Frame(self, bg=self.cor_principal, height=90)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        titulo = tk.Label(
            header,
            text="📚 Acervo da Biblioteca",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg=self.cor_principal
        )
        titulo.pack(pady=(16, 2))

        subtitulo = tk.Label(
            header,
            text=f"Bem-vindo(a), {self.usuario.username} • Perfil: {self.usuario.obter_tipo()}",
            font=("Segoe UI", 10),
            fg="white",
            bg=self.cor_principal
        )
        subtitulo.pack()

    def _criar_conteudo(self):
        container = tk.Frame(self, bg=self.cor_fundo, padx=18, pady=16)
        container.pack(fill=tk.BOTH, expand=True)

        btn_fechar = tk.Button(
            container,
            text="Fechar Acervo",
            command=self.destroy,
            width=18,
            font=("Segoe UI", 10, "bold"),
            bg="#dc3545",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2"
        )
        btn_fechar.pack(anchor="e", pady=(0, 10))

        canvas = tk.Canvas(
            container,
            bg=self.cor_fundo,
            highlightthickness=0
        )
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.cor_fundo)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._criar_secao_titulo(scroll_frame, "Sugestões para você")
        self._criar_grade_livros(scroll_frame, self.recomendacoes)

        self._criar_secao_titulo(scroll_frame, "Catálogo completo")
        self._criar_grade_livros(scroll_frame, self.catalogo_completo)

        self._ativar_scroll_mouse(canvas)

    def _criar_secao_titulo(self, parent, texto):
        secao = tk.Frame(parent, bg=self.cor_fundo)
        secao.pack(fill=tk.X, pady=(8, 12))

        linha = tk.Frame(secao, bg=self.cor_principal, height=3)
        linha.pack(fill=tk.X, pady=(0, 8))

        titulo = tk.Label(
            secao,
            text=texto,
            font=("Segoe UI", 15, "bold"),
            fg=self.cor_principal,
            bg=self.cor_fundo
        )
        titulo.pack(anchor="w")

    def _criar_grade_livros(self, parent, livros):
        grid_frame = tk.Frame(parent, bg=self.cor_fundo)
        grid_frame.pack(fill=tk.X, pady=(0, 22))

        colunas = 2
        largura_card = 410

        for i, livro in enumerate(livros):
            linha = i // colunas
            coluna = i % colunas

            card = tk.Frame(
                grid_frame,
                bg="white",
                width=largura_card,
                height=152,
                highlightbackground=self.cor_borda,
                highlightthickness=2,
                bd=0
            )
            card.grid(row=linha, column=coluna, padx=8, pady=8, sticky="n")
            card.grid_propagate(False)

            faixa = tk.Frame(card, bg=self.cor_card, width=14)
            faixa.pack(side=tk.LEFT, fill=tk.Y)

            conteudo = tk.Frame(card, bg="white", padx=12, pady=10)
            conteudo.pack(fill=tk.BOTH, expand=True)

            rotulo = tk.Label(
                conteudo,
                text="Livro recomendado" if livro in self.recomendacoes else "Disponível no catálogo",
                font=("Segoe UI", 8, "bold"),
                fg=self.cor_principal,
                bg="white"
            )
            rotulo.pack(anchor="w")

            status = self.facade.obter_status_livro(self.usuario, livro)
            status_texto, status_cor = self._formatar_status(status)
            status_lbl = tk.Label(
                conteudo,
                text=f"Status: {status_texto}",
                font=("Segoe UI", 8, "bold"),
                fg=status_cor,
                bg="white"
            )
            status_lbl.pack(anchor="w", pady=(3, 0))

            titulo = tk.Label(
                conteudo,
                text=livro,
                font=("Segoe UI", 11, "bold"),
                fg="#1f1f1f",
                bg="white",
                wraplength=350,
                justify="left"
            )
            titulo.pack(anchor="w", pady=(4, 0))

            descricao = tk.Label(
                conteudo,
                text="Biblioteca Acadêmica • Acervo disponível",
                font=("Segoe UI", 9),
                fg="#666666",
                bg="white"
            )
            descricao.pack(anchor="w", pady=(4, 0))

            btn_alugar = tk.Button(
                conteudo,
                text="Alugar este livro",
                font=("Segoe UI", 9, "bold"),
                bg=self.cor_principal,
                fg="white",
                relief=tk.FLAT,
                cursor="hand2",
                command=lambda livro_escolhido=livro: self._alugar_livro(livro_escolhido)
            )
            btn_alugar.pack(anchor="e", pady=(8, 4))

            btn_reservar = tk.Button(
                conteudo,
                text="Reservar livro",
                font=("Segoe UI", 9, "bold"),
                bg="#6c757d",
                fg="white",
                relief=tk.FLAT,
                cursor="hand2",
                command=lambda livro_escolhido=livro: self._reservar_livro(livro_escolhido)
            )
            btn_reservar.pack(anchor="e")

            if status == "disponivel":
                btn_reservar.configure(state=tk.DISABLED, bg="#b8bec5", cursor="arrow")
            elif status == "alugado_por_voce":
                btn_alugar.configure(state=tk.DISABLED, bg="#b8bec5", cursor="arrow")
                btn_reservar.configure(state=tk.DISABLED, bg="#b8bec5", cursor="arrow")
            elif status == "alugado":
                btn_alugar.configure(state=tk.DISABLED, bg="#b8bec5", cursor="arrow")
            elif status == "reservado_por_voce":
                btn_alugar.configure(state=tk.DISABLED, bg="#b8bec5", cursor="arrow")
                btn_reservar.configure(state=tk.DISABLED, bg="#b8bec5", cursor="arrow")

        for c in range(colunas):
            grid_frame.grid_columnconfigure(c, weight=1)

    def _ativar_scroll_mouse(self, canvas):
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def _alugar_livro(self, livro):
        sucesso, mensagem = self.facade.registrar_emprestimo(self.usuario, livro)
        if sucesso:
            messagebox.showinfo("Empréstimo registrado", f"{mensagem}\n\nLivro: {livro}")
            self.destroy()
            CatalogoView(self.master, self.usuario, self.recomendacoes, self.catalogo_completo, self.facade)
        else:
            messagebox.showwarning("Não foi possível alugar", mensagem)

    def _reservar_livro(self, livro):
        sucesso, mensagem = self.facade.reservar_livro(self.usuario, livro)
        if sucesso:
            messagebox.showinfo("Reserva registrada", f"{mensagem}\n\nLivro: {livro}")
            self.destroy()
            CatalogoView(self.master, self.usuario, self.recomendacoes, self.catalogo_completo, self.facade)
        else:
            messagebox.showwarning("Não foi possível reservar", mensagem)

    def _formatar_status(self, status):
        mapa = {
            "disponivel": ("Disponível", "#198754"),
            "alugado_por_voce": ("Alugado por você", "#0d6efd"),
            "alugado": ("Alugado", "#dc3545"),
            "reservado_por_voce": ("Reservado por você", "#6f42c1"),
            "desconhecido": ("Indisponível", "#6c757d"),
        }
        return mapa.get(status, ("Indisponível", "#6c757d"))