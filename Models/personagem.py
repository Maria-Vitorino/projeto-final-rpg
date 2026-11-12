from abc import ABC, abstractmethod
import math


class Personagem(ABC):
    """Classe-base que reúne os dados e comportamentos comuns dos personagens."""

    def __init__(self, nome, x, y, velocidade=0.0):
        self.nome = nome
        self._x = float(x)
        self._y = float(y)
        self.velocidade = velocidade

    @property
    def nome(self):
        """Retorna o nome do personagem."""
        return self._nome

    @nome.setter
    def nome(self, novo_nome):
        """Define o nome, impedindo valores vazios ou que não sejam texto."""
        if not isinstance(novo_nome, str) or not novo_nome.strip():
            raise ValueError("O nome não pode ser vazio.")

        # A classe-base também representa NPCs, cujos nomes podem conter números.
        # Regras específicas para nomes de jogadores ficam na classe Jogador.
        self._nome = " ".join(novo_nome.split())

    @property
    def velocidade(self):
        """Retorna a velocidade de movimentação do personagem."""
        return self._velocidade

    @velocidade.setter
    def velocidade(self, nova_velocidade):
        """Define uma velocidade numérica, finita e não negativa."""
        if isinstance(nova_velocidade, bool):
            raise ValueError("A velocidade deve ser um número válido e não negativo.")
        try:
            velocidade = float(nova_velocidade)
        except (TypeError, ValueError):
            raise ValueError("A velocidade deve ser um número válido e não negativo.") from None

        if not math.isfinite(velocidade) or velocidade < 0:
            raise ValueError("A velocidade deve ser um número válido e não negativo.")

        self._velocidade = velocidade

    @property
    def x(self):
        """Retorna a posição horizontal do personagem."""
        return self._x

    @property
    def y(self):
        """Retorna a posição vertical do personagem."""
        return self._y

    @property
    def posicao(self):
        """Retorna as coordenadas horizontal e vertical."""
        return self._x, self._y

    def mover(self, dx, dy, tempo, limites):
        """Atualiza a posição respeitando a velocidade e os limites do mapa."""
        esquerda, topo, direita, baixo = limites

        self._x = min(max(self._x + dx * self._velocidade * tempo, esquerda), direita)
        self._y = min(max(self._y + dy * self._velocidade * tempo, topo), baixo)

    @abstractmethod
    def interagir(self):
        """Define o comportamento de interação nas classes concretas."""
        raise NotImplementedError
