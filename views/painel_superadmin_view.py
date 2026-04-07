import tkinter as tk
from models.entidades import Usuario


class PainelSuperAdmin(tk.Toplevel):
    def __init__(self, master, usuario: Usuario, callback_fechar):
        super().__init__(master)
        self.title("Biblioteca - Administração Mestra")
        self.geometry("450x350")
        self.resizable(False, False)

        self.usuario = usuario
        self.callback_fechar = callback_fechar
        self.protocol("WM_DELETE_WINDOW", self.fechar)

        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.winfo_screenheight() // 2) - (350 // 2)
        self.geometry(f"+{x}+{y}")

        lbl_boas_vindas = tk.Label(
            self,
            text=f"👑 Controle do Acervo\n\nDiretor(a) {self.usuario.username}!",
            font=("Segoe UI", 16, "bold"),
            fg="#800080"
        )
        lbl_boas_vindas.pack(pady=20)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(pady=10)

        tk.Button(
            frame_botoes,
            text="Gerenciar Acervo e Livros",
            width=30,
            font=("Segoe UI", 10),
            bg="#f3e6ff",
            relief=tk.FLAT
        ).pack(pady=5)

        tk.Button(
            frame_botoes,
            text="Relatório de Multas e Devoluções",
            width=30,
            font=("Segoe UI", 10),
            bg="#f3e6ff",
            relief=tk.FLAT
        ).pack(pady=5)

        tk.Button(
            frame_botoes,
            text="Gerenciar Contas de Leitores",
            width=30,
            font=("Segoe UI", 10),
            bg="#f3e6ff",
            relief=tk.FLAT
        ).pack(pady=5)

        btn_sair = tk.Button(
            self,
            text="Sair do Modo Admin",
            command=self.fechar,
            width=30,
            font=("Segoe UI", 10, "bold"),
            bg="#dc3545",
            fg="white",
            relief=tk.FLAT
        )
        btn_sair.pack(pady=20)

    def fechar(self):
        self.destroy()
        self.callback_fechar()