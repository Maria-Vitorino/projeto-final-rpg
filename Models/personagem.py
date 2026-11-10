from abc import ABC, abstractmethod


class Personagem(ABC):

    def __init__(self, nome, x, y, velocidade=0.0):
        self._nome = nome
        self._x = float(x)
        self._y = float(y)
        self._velocidade = float(velocidade)

    @property
    def nome(self):
        return self._nome

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def posicao(self):
        return self._x, self._y

    def mover(self, dx, dy, tempo, limites):
        esquerda, topo, direita, baixo = limites

        self._x = min(max(self._x + dx * self._velocidade * tempo, esquerda), direita)
        self._y = min(max(self._y + dy * self._velocidade * tempo, topo), baixo)

    @abstractmethod
    def interagir(self):
        """Cada tipo de personagem define como ocorre sua interação."""
        raise NotImplementedError