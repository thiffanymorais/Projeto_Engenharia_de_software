import tkinter as tk
from tkinter import messagebox
from database.sqlite_db import Database
from services.biblioteca_facade import BibliotecaFacade


class LoginApp:
    def __init__(self, root):
        self.db = Database()
        self.facade = BibliotecaFacade(self.db)

        self.root = root
        self.root.title("Biblioteca Acadêmica")
        self.root.geometry("400x370")
        self.root.resizable(False, False)

        self.root.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)

        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.lbl_titulo = tk.Label(
            self.frame,
            text="📚 Sistema da Biblioteca",
            font=("Segoe UI", 16, "bold")
        )
        self.lbl_titulo.pack(pady=(0, 20))

        self.lbl_user = tk.Label(
            self.frame,
            text="Nome de Leitor (Usuário):",
            font=("Segoe UI", 10)
        )
        self.lbl_user.pack(anchor="w")

        self.ent_user = tk.Entry(self.frame, width=35, font=("Segoe UI", 10))
        self.ent_user.pack(pady=(0, 10))

        self.lbl_senha = tk.Label(
            self.frame,
            text="Acesso (Senha):",
            font=("Segoe UI", 10)
        )
        self.lbl_senha.pack(anchor="w")

        self.ent_senha = tk.Entry(
            self.frame,
            width=35,
            font=("Segoe UI", 10),
            show="*"
        )
        self.ent_senha.pack(pady=(0, 10))

        self.lbl_tipo = tk.Label(
            self.frame,
            text="Perfil (Apenas no Cadastro Novo):",
            font=("Segoe UI", 10)
        )
        self.lbl_tipo.pack(anchor="w")

        self.tipo_var = tk.StringVar(value="Aluno")

        self.frame_radios = tk.Frame(self.frame)
        self.frame_radios.pack(anchor="w", pady=(0, 15))

        self.rb_aluno = tk.Radiobutton(
            self.frame_radios,
            text="Aluno",
            variable=self.tipo_var,
            value="Aluno",
            font=("Segoe UI", 10)
        )
        self.rb_aluno.pack(side=tk.LEFT, padx=(0, 10))

        self.rb_professor = tk.Radiobutton(
            self.frame_radios,
            text="Professor",
            variable=self.tipo_var,
            value="Professor",
            font=("Segoe UI", 10)
        )
        self.rb_professor.pack(side=tk.LEFT)

        self.frame_botoes = tk.Frame(self.frame)
        self.frame_botoes.pack(fill=tk.X, pady=(10, 0))

        self.btn_entrar = tk.Button(
            self.frame_botoes,
            text="Acessar Acervo",
            command=self.realizar_login,
            width=15,
            bg="#0052cc",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT
        )
        self.btn_entrar.pack(side=tk.LEFT, padx=(5, 5), expand=True)

        self.btn_cadastrar = tk.Button(
            self.frame_botoes,
            text="Novo Cadastro",
            command=self.realizar_cadastro,
            width=15,
            bg="#28a745",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT
        )
        self.btn_cadastrar.pack(side=tk.RIGHT, padx=(5, 5), expand=True)

    def realizar_cadastro(self):
        username = self.ent_user.get().strip()
        senha = self.ent_senha.get().strip()
        tipo_selecionado = self.tipo_var.get()

        if not username or not senha:
            messagebox.showwarning(
                "Aviso",
                "Por favor, preencha o nome de usuário e a senha para se cadastrar."
            )
            return

        sucesso, mensagem = self.db.cadastrar_usuario(username, senha, tipo_selecionado)

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
        else:
            messagebox.showerror("Erro de Cadastro", mensagem)

    def realizar_login(self):
        username = self.ent_user.get().strip()
        senha = self.ent_senha.get().strip()

        if not username or not senha:
            messagebox.showwarning("Aviso", "Por favor, preencha o login e a senha.")
            return

        usuario = self.facade.autenticar_usuario(username, senha)

        if not usuario:
            messagebox.showerror(
                "Acesso Negado",
                "Nome de leitor ou senha inválidos. Tente novamente."
            )
            return

        try:
            self.root.withdraw()
            self.facade.abrir_painel(
                self.root,
                usuario,
                self.mostrar_login
            )
        except ValueError as e:
            messagebox.showerror("Erro de Sistema", str(e))
            self.mostrar_login()

    def mostrar_login(self):
        self.ent_user.delete(0, tk.END)
        self.ent_senha.delete(0, tk.END)
        self.root.deiconify()

    def fechar_aplicacao(self):
        self.db.fechar_conexao()
        self.root.destroy()