from models.entidades import Aluno, Professor
from services.recomendacao_strategy import (
    RecomendacaoAlunoStrategy,
    RecomendacaoProfessorStrategy
)


class RecomendacaoService:
    def __init__(self):
        self._estrategia_aluno = RecomendacaoAlunoStrategy()
        self._estrategia_professor = RecomendacaoProfessorStrategy()
        self._novidades = [
            "IA Generativa na Prática",
            "DevOps e Integração Contínua",
            "Engenharia de Prompt e Aplicações com IA",
            "Arquitetura Orientada a Eventos",
            "Observabilidade em Sistemas Distribuídos",
            "Automação de Testes com Python"
        ]

    def obter_recomendacoes(self, usuario):
        if isinstance(usuario, Aluno):
            return self._estrategia_aluno.recomendar_livros()
        elif isinstance(usuario, Professor):
            return self._estrategia_professor.recomendar_livros()
        return []

    def obter_novidades(self):
        return self._novidades.copy()

    def obter_catalogo_completo(self):
        catalogo = []
        catalogo.extend(self._estrategia_aluno.recomendar_livros())
        catalogo.extend(self._estrategia_professor.recomendar_livros())
        catalogo.extend(self._novidades)
        return list(dict.fromkeys(catalogo))
