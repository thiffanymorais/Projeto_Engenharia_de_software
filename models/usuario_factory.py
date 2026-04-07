from models.entidades import Usuario, Aluno, Professor, SuperAdmin


class UsuarioFactory:
    @staticmethod
    def criar_usuario(tipo_usuario: str, username: str) -> Usuario:
        if tipo_usuario == "Aluno":
            return Aluno(username)
        elif tipo_usuario == "Professor":
            return Professor(username)
        elif tipo_usuario == "SuperAdmin":
            return SuperAdmin(username)
        else:
            raise ValueError(f"Tipo de usuário desconhecido: {tipo_usuario}")