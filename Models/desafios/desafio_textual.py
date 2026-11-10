from .desafio import Desafio


class DesafioTextual(Desafio):

    def validar_resposta(self, resposta):
        return self.pergunta.verificar_resposta(resposta)