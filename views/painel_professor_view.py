import tkinter as tk
from models.entidades import Usuario
from views.catalogo_view import CatalogoView
from views.emprestimos_view import EmprestimosView


class PainelProfessor(tk.Toplevel):
    def __init__(self, master, usuario: Usuario, callback_fechar, facade):
        super().__init__(master)
        self.title("Biblioteca - Espaço do Professor")
        self.geometry("450x300")
        self.resizable(False, False)

        self.usuario = usuario
        self.callback_fechar = callback_fechar
        self.facade = facade
        self.protocol("WM_DELETE_WINDOW", self.fechar)

        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.winfo_screenheight() // 2) - (300 // 2)
        self.geometry(f"450x300+{x}+{y}")

        lbl_boas_vindas = tk.Label(
            self,
            text=f"Espaço do Pesquisador\n\nProf(a). {self.usuario.username}",
            font=("Segoe UI", 16, "bold"),
            fg="#28a745"
        )
        lbl_boas_vindas.pack(pady=20)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(pady=10)

        tk.Button(
            frame_botoes,
            text="Catálogo Completo",
            width=30,
            font=("Segoe UI", 10),
            bg="#e6ffe6",
            relief=tk.FLAT,
            command=self.abrir_acervo
        ).pack(pady=5)

        tk.Button(
            frame_botoes,
            text="Meus Empréstimos Abertos",
            width=30,
            font=("Segoe UI", 10),
            bg="#e6ffe6",
            relief=tk.FLAT,
            command=self.mostrar_emprestimos_abertos
        ).pack(pady=5)

        tk.Button(
            self,
            text="Sair (Fazer Logout)",
            command=self.fechar,
            width=30,
            font=("Segoe UI", 10, "bold"),
            bg="#dc3545",
            fg="white",
            relief=tk.FLAT
        ).pack(pady=20)

    def abrir_acervo(self):
        recomendacoes = self.facade.obter_recomendacoes(self.usuario)
        novidades = self.facade.obter_novidades()
        catalogo_completo = self.facade.obter_catalogo_completo()
        CatalogoView(self, self.usuario, recomendacoes, novidades, catalogo_completo, self.facade)

    def mostrar_emprestimos_abertos(self):
        EmprestimosView(self, self.usuario, self.facade)

    def fechar(self):
        self.destroy()
        self.callback_fechar()