from .personagem import Personagem


class Jogador(Personagem):

    def __init__(self, nome, id_personagem, x, y, velocidade=220.0):
        super().__init__(nome, x, y, velocidade)

        self._id_personagem = id_personagem
        self._andando = False
        self._olhando_direita = True

    @property
    def id_personagem(self):
        return self._id_personagem

    @property
    def andando(self):
        return self._andando

    @property
    def olhando_direita(self):
        return self._olhando_direita

    def definir_movimento(self, dx, dy, tempo, limites):

        if dx != 0 or dy != 0:
            self._andando = True
        else:
            self._andando = False

        if dx != 0:
            if dx > 0:
                self._olhando_direita = True
            else:
                self._olhando_direita = False

        if dx != 0 and dy != 0:
            dx = dx * 0.70710678
            dy = dy * 0.70710678

        self.mover(dx, dy, tempo, limites)

    def interagir(self):
        return f"{self.nome} está pronto para explorar a era."