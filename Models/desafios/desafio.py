from abc import ABC, abstractmethod
from .pergunta import Pergunta


class Desafio(ABC):

    def __init__(self, pergunta: Pergunta):
        self._pergunta = pergunta

    @property
    def pergunta(self):
        return self._pergunta

    @abstractmethod
    def validar_resposta(self, resposta):
        pass