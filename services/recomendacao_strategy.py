from abc import ABC, abstractmethod


class RecomendacaoStrategy(ABC):
    @abstractmethod
    def recomendar_livros(self):
        pass


class RecomendacaoAlunoStrategy(RecomendacaoStrategy):
    def recomendar_livros(self):
        return [
            "Introdução à Programação",
            "Lógica de Programação",
            "Estruturas de Dados",
            "Python para Iniciantes",
            "Algoritmos e Pensamento Computacional",
            "Banco de Dados Básico",
            "Redes de Computadores - Fundamentos",
            "Matemática Discreta Aplicada",
            "Programação Orientada a Objetos",
            "Desenvolvimento Web com HTML e CSS",
            "JavaScript Essencial",
            "Versionamento com Git e GitHub",
            "Engenharia de Software para Estudantes",
            "Análise e Projeto de Sistemas",
            "Segurança da Informação - Conceitos Básicos",
            "Introdução à Inteligência Artificial",
            "Computação em Nuvem para Universitários",
            "UX e UI para Sistemas Acadêmicos",
            "Resolução de Problemas com Algoritmos",
            "Fundamentos de Sistemas Operacionais"
        ]


class RecomendacaoProfessorStrategy(RecomendacaoStrategy):
    def recomendar_livros(self):
        return [
            "Padrões de Projeto",
            "Arquitetura de Software Limpa",
            "Engenharia de Software Moderna",
            "Domain-Driven Design",
            "Clean Code",
            "Refatoração de Software",
            "Sistemas Distribuídos",
            "Computação de Alto Desempenho",
            "Mineração de Dados e Analytics",
            "Machine Learning Aplicado",
            "Deep Learning para Pesquisa",
            "Métodos Formais em Engenharia de Software",
            "Banco de Dados Avançado",
            "Big Data e Processamento Massivo",
            "Cibersegurança em Ambientes Corporativos",
            "Gerência de Projetos de Software",
            "Qualidade e Testes de Software",
            "Arquitetura de Microsserviços",
            "Pesquisa Científica em Computação",
            "Tópicos Avançados em Inteligência Artificial"
        ]