from .personagem import Personagem


class PersonagemNaoJogavel(Personagem):

    def __init__(self, id_npc, nome, x, y):
        super().__init__(nome, x, y, 0)

        self._id_npc = id_npc
        self._concluido = False

    @property
    def id_npc(self):
        return self._id_npc

    @property
    def concluido(self):
        return self._concluido

    def marcar_concluido(self):
        self._concluido = True

    def interagir(self):
        return f"Você se aproximou de {self.nome}."