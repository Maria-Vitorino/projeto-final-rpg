from .desafio import Desafio


class DesafioQuestionario(Desafio):

    def validar_resposta(self, resposta):
        return self.pergunta.verificar_resposta(resposta)