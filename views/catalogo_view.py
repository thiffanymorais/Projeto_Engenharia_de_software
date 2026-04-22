import tkinter as tk
from tkinter import messagebox


class CatalogoView(tk.Toplevel):
    def __init__(self, master, usuario, recomendacoes, novidades, catalogo_completo, facade):
        super().__init__(master)
        self.usuario = usuario
        self.recomendacoes = list(dict.fromkeys(recomendacoes))
        self.novidades = list(dict.fromkeys(novidades))
        self.catalogo_completo = list(dict.fromkeys(catalogo_completo))
        self.facade = facade
        self.aba_atual = "pedp"
        self.busca_var = tk.StringVar()
        self.filtro_status_var = tk.StringVar(value="todos")

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
        self.cor_aba_inativa = "#dfe8f7" if usuario.obter_tipo() == "Aluno" else "#dff3e4"

        self.configure(bg=self.cor_fundo)

        self._criar_header()
        self._criar_conteudo()
        self._atualizar_conteudo()

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

        self._criar_abas(container)
        self._criar_filtros(container)

        self.canvas = tk.Canvas(
            container,
            bg=self.cor_fundo,
            highlightthickness=0
        )
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

        self._ativar_scroll_mouse(self.canvas)

    def _criar_abas(self, parent):
        self.frame_abas = tk.Frame(parent, bg=self.cor_fundo)
        self.frame_abas.pack(fill=tk.X, pady=(0, 12))

        self.btn_pedp = self._criar_botao_aba("PEDP", "pedp")
        self.btn_novidades = self._criar_botao_aba("Novidades", "novidades")
        self.btn_todos = self._criar_botao_aba("Todos", "todos")

    def _criar_botao_aba(self, texto, chave):
        btn = tk.Button(
            self.frame_abas,
            text=texto,
            width=18,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda aba=chave: self._trocar_aba(aba)
        )
        btn.pack(side=tk.LEFT, padx=(0, 8))
        return btn

    def _criar_filtros(self, parent):
        self.frame_filtros = tk.Frame(parent, bg="white", highlightbackground=self.cor_borda, highlightthickness=1)

        interno = tk.Frame(self.frame_filtros, bg="white", padx=12, pady=10)
        interno.pack(fill=tk.X)

        tk.Label(
            interno,
            text="Buscar:",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#333333"
        ).grid(row=0, column=0, sticky="w", padx=(0, 8))

        entrada = tk.Entry(
            interno,
            textvariable=self.busca_var,
            width=32,
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=self.cor_borda,
            highlightcolor=self.cor_principal
        )
        entrada.grid(row=0, column=1, sticky="w", padx=(0, 16))
        self.busca_var.trace_add("write", lambda *_: self._atualizar_conteudo())

        tk.Label(
            interno,
            text="Status:",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#333333"
        ).grid(row=0, column=2, sticky="w", padx=(0, 8))

        filtro = tk.OptionMenu(
            interno,
            self.filtro_status_var,
            "todos",
            "disponivel",
            "alugado",
            "alugado_por_voce",
            "reservado_por_voce",
            command=lambda *_: self._atualizar_conteudo()
        )
        filtro.config(font=("Segoe UI", 9), relief=tk.FLAT, bg=self.cor_card, activebackground=self.cor_card)
        filtro.grid(row=0, column=3, sticky="w")

    def _trocar_aba(self, aba):
        self.aba_atual = aba
        self._atualizar_conteudo()

    def _atualizar_conteudo(self):
        self._atualizar_visual_abas()

        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if self.aba_atual == "todos":
            self.frame_filtros.pack(fill=tk.X, pady=(0, 12), before=self.canvas)
            livros = self._filtrar_livros(self.catalogo_completo)
            self._criar_secao_titulo(self.scroll_frame, f"Todos os livros • {len(livros)} resultado(s)")
            self._criar_grade_livros(self.scroll_frame, livros)
        elif self.aba_atual == "novidades":
            self.frame_filtros.pack_forget()
            self._criar_secao_titulo(self.scroll_frame, "Novidades")
            self._criar_grade_livros(self.scroll_frame, self.novidades)
        else:
            self.frame_filtros.pack_forget()
            self._criar_secao_titulo(self.scroll_frame, "PEDP • Livros de recomendação")
            self._criar_grade_livros(self.scroll_frame, self.recomendacoes)

        self.canvas.yview_moveto(0)

    def _atualizar_visual_abas(self):
        mapa = {
            "pedp": self.btn_pedp,
            "novidades": self.btn_novidades,
            "todos": self.btn_todos
        }
        for chave, btn in mapa.items():
            ativo = chave == self.aba_atual
            btn.configure(
                bg=self.cor_principal if ativo else self.cor_aba_inativa,
                fg="white" if ativo else self.cor_principal
            )

    def _filtrar_livros(self, livros):
        termo = self.busca_var.get().strip().lower()
        filtro_status = self.filtro_status_var.get()
        resultado = []

        for livro in livros:
            if termo and termo not in livro.lower():
                continue

            status = self.facade.obter_status_livro(self.usuario, livro)
            if filtro_status != "todos" and status != filtro_status:
                continue

            resultado.append(livro)

        return resultado

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

        if not livros:
            tk.Label(
                grid_frame,
                text="Nenhum livro encontrado.",
                font=("Segoe UI", 11, "italic"),
                fg="#6c757d",
                bg=self.cor_fundo
            ).pack(pady=22)
            return

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
                bd=0,
                cursor="hand2"
            )
            card.grid(row=linha, column=coluna, padx=8, pady=8, sticky="n")
            card.grid_propagate(False)

            faixa = tk.Frame(card, bg=self.cor_card, width=14)
            faixa.pack(side=tk.LEFT, fill=tk.Y)

            conteudo = tk.Frame(card, bg="white", padx=12, pady=10)
            conteudo.pack(fill=tk.BOTH, expand=True)

            rotulo = tk.Label(
                conteudo,
                text=self._obter_rotulo_livro(livro),
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
                text="Clique no card para abrir este acervo",
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

            self._vincular_clique(card, livro)
            self._vincular_clique(faixa, livro)
            self._vincular_clique(conteudo, livro)
            self._vincular_clique(rotulo, livro)
            self._vincular_clique(status_lbl, livro)
            self._vincular_clique(titulo, livro)
            self._vincular_clique(descricao, livro)

        for c in range(colunas):
            grid_frame.grid_columnconfigure(c, weight=1)

    def _vincular_clique(self, widget, livro):
        widget.bind("<Button-1>", lambda event, livro_escolhido=livro: self._abrir_detalhes_livro(livro_escolhido))

    def _obter_rotulo_livro(self, livro):
        if livro in self.recomendacoes:
            return "Livro recomendado"
        if livro in self.novidades:
            return "Novo no acervo"
        return "Disponível no catálogo"

    def _abrir_detalhes_livro(self, livro):
        detalhes = tk.Toplevel(self)
        detalhes.title("Detalhes do livro")
        detalhes.geometry("480x260")
        detalhes.resizable(False, False)
        detalhes.configure(bg="white")
        detalhes.transient(self)
        detalhes.grab_set()

        status = self.facade.obter_status_livro(self.usuario, livro)
        status_texto, status_cor = self._formatar_status(status)

        corpo = tk.Frame(detalhes, bg="white", padx=20, pady=20)
        corpo.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            corpo,
            text=livro,
            font=("Segoe UI", 14, "bold"),
            fg="#1f1f1f",
            bg="white",
            wraplength=420,
            justify="left"
        ).pack(anchor="w")

        tk.Label(
            corpo,
            text=self._obter_rotulo_livro(livro),
            font=("Segoe UI", 10, "bold"),
            fg=self.cor_principal,
            bg="white"
        ).pack(anchor="w", pady=(10, 4))

        tk.Label(
            corpo,
            text=f"Status: {status_texto}",
            font=("Segoe UI", 10, "bold"),
            fg=status_cor,
            bg="white"
        ).pack(anchor="w", pady=(0, 14))

        tk.Label(
            corpo,
            text="Este livro está disponível no acervo da biblioteca. Você pode alugá-lo ou reservá-lo conforme a disponibilidade atual.",
            font=("Segoe UI", 10),
            fg="#555555",
            bg="white",
            wraplength=420,
            justify="left"
        ).pack(anchor="w")

        acoes = tk.Frame(corpo, bg="white")
        acoes.pack(anchor="e", pady=(24, 0))

        tk.Button(
            acoes,
            text="Fechar",
            font=("Segoe UI", 9, "bold"),
            bg="#dee2e6",
            fg="#333333",
            relief=tk.FLAT,
            cursor="hand2",
            command=detalhes.destroy
        ).pack(side=tk.RIGHT)

    def _ativar_scroll_mouse(self, canvas):
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def _alugar_livro(self, livro):
        sucesso, mensagem = self.facade.registrar_emprestimo(self.usuario, livro)
        if sucesso:
            messagebox.showinfo("Empréstimo registrado", f"{mensagem}\n\nLivro: {livro}")
            self.destroy()
            CatalogoView(self.master, self.usuario, self.recomendacoes, self.novidades, self.catalogo_completo, self.facade)
        else:
            messagebox.showwarning("Não foi possível alugar", mensagem)

    def _reservar_livro(self, livro):
        sucesso, mensagem = self.facade.reservar_livro(self.usuario, livro)
        if sucesso:
            messagebox.showinfo("Reserva registrada", f"{mensagem}\n\nLivro: {livro}")
            self.destroy()
            CatalogoView(self.master, self.usuario, self.recomendacoes, self.novidades, self.catalogo_completo, self.facade)
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
