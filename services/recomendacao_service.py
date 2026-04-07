from models.entidades import Aluno, Professor
from services.recomendacao_strategy import (
    RecomendacaoAlunoStrategy,
    RecomendacaoProfessorStrategy
)


class RecomendacaoService:
    def __init__(self):
        self._estrategia_aluno = RecomendacaoAlunoStrategy()
        self._estrategia_professor = RecomendacaoProfessorStrategy()

    def obter_recomendacoes(self, usuario):
        if isinstance(usuario, Aluno):
            return self._estrategia_aluno.recomendar_livros()
        elif isinstance(usuario, Professor):
            return self._estrategia_professor.recomendar_livros()
        return []

    def obter_catalogo_completo(self):
        catalogo = []
        catalogo.extend(self._estrategia_aluno.recomendar_livros())
        catalogo.extend(self._estrategia_professor.recomendar_livros())
        return catalogo