from .personagem_nao_jogavel import PersonagemNaoJogavel


class NPCDesafio(PersonagemNaoJogavel):

    def interagir(self):
        return f"{self.nome} tem um desafio para você."