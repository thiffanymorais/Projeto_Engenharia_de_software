from abc import ABC, abstractmethod


class Usuario(ABC):
    def __init__(self, username):
        self.username = username

    @abstractmethod
    def obter_tipo(self):
        pass


class Aluno(Usuario):
    def obter_tipo(self):
        return "Aluno"


class Professor(Usuario):
    def obter_tipo(self):
        return "Professor"


class SuperAdmin(Usuario):
    def obter_tipo(self):
        return "SuperAdmin"