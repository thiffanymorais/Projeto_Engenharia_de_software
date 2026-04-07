from models.entidades import Usuario
from views.painel_aluno_view import PainelAluno
from views.painel_professor_view import PainelProfessor
from views.painel_superadmin_view import PainelSuperAdmin


class ViewFactory:
    @staticmethod
    def criar_painel(tipo_usuario: str, master, usuario: Usuario, callback_fechar, facade):
        if tipo_usuario == "Aluno":
            return PainelAluno(master, usuario, callback_fechar, facade)
        elif tipo_usuario == "Professor":
            return PainelProfessor(master, usuario, callback_fechar, facade)
        elif tipo_usuario == "SuperAdmin":
            return PainelSuperAdmin(master, usuario, callback_fechar)
        else:
            raise ValueError(f"Painel não encontrado para o tipo: {tipo_usuario}")