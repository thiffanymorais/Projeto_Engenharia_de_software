from models.usuario_factory import UsuarioFactory
from services.recomendacao_service import RecomendacaoService
from views.view_factory import ViewFactory


class BibliotecaFacade:
    def __init__(self, db):
        self.db = db
        self.recomendacao_service = RecomendacaoService()

    def autenticar_usuario(self, username: str, senha: str):
        dados_usuario = self.db.buscar_usuario(username, senha)

        if not dados_usuario:
            return None

        nome_encontrado, tipo_encontrado = dados_usuario
        usuario = UsuarioFactory.criar_usuario(tipo_encontrado, nome_encontrado)
        return usuario

    def obter_recomendacoes(self, usuario):
        return self.recomendacao_service.obter_recomendacoes(usuario)

    def obter_catalogo_completo(self):
        return self.recomendacao_service.obter_catalogo_completo()

    def abrir_painel(self, master, usuario, callback_fechar):
        return ViewFactory.criar_painel(
            usuario.obter_tipo(),
            master,
            usuario,
            callback_fechar,
            self
        )

    def registrar_emprestimo(self, usuario, livro: str):
        return self.db.registrar_emprestimo(usuario.username, livro)

    def listar_emprestimos_abertos(self, usuario):
        return self.db.listar_emprestimos_abertos(usuario.username)

    def estender_emprestimo(self, usuario, emprestimo_id: int):
        return self.db.estender_emprestimo(usuario.username, emprestimo_id)

    def reservar_livro(self, usuario, livro: str):
        return self.db.reservar_livro(usuario.username, livro)

    def obter_status_livro(self, usuario, livro: str):
        return self.db.obter_status_livro(usuario.username, livro)

    def listar_reservas_ativas(self, usuario):
        return self.db.listar_reservas_ativas(usuario.username)

    def listar_reservas_canceladas(self, usuario):
        return self.db.listar_reservas_canceladas(usuario.username)

    def cancelar_reserva(self, usuario, reserva_id: int):
        return self.db.cancelar_reserva(usuario.username, reserva_id)