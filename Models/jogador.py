from .personagem import Personagem


class Jogador(Personagem):
    """Representa o personagem controlado pela pessoa que está jogando."""

    PERSONAGENS_DISPONIVEIS = (
        "kassandra",
        "nikos",
        "lyra",
        "alexandros",
    )

    def __init__(self, nome, id_personagem, x, y, velocidade=220.0):
        super().__init__(nome, x, y, velocidade)

        self.id_personagem = id_personagem
        self._andando = False
        self._olhando_direita = True

    @property
    def nome(self):
        """Retorna o nome validado do jogador."""
        return super().nome

    @nome.setter
    def nome(self, novo_nome):
        """Aceita nomes de pessoas, sem números, vazios ou o nome bloqueado."""
        if not isinstance(novo_nome, str) or not novo_nome.strip():
            raise ValueError("O nome do jogador não pode ficar vazio.")

        nome_limpo = " ".join(novo_nome.split())
        nome_normalizado = nome_limpo.casefold()

        if nome_normalizado == "kanye west":
            raise ValueError("Esse nome não está disponível. Escolha outro. 😄")

        caracteres_permitidos = {" ", "-", "'", "’"}
        if not all(caractere.isalpha() or caractere in caracteres_permitidos
                   for caractere in nome_limpo):
            raise ValueError("Use apenas letras para o nome do jogador.")

        self._nome = nome_limpo

    @property
    def id_personagem(self):
        """Retorna o identificador visual do personagem escolhido."""
        return self._id_personagem

    @id_personagem.setter
    def id_personagem(self, novo_id):
        """Aceita somente identificadores de personagens cadastrados no jogo."""
        if novo_id not in self.PERSONAGENS_DISPONIVEIS:
            raise ValueError(
                f"Personagem inválido. Escolha um destes: {', '.join(self.PERSONAGENS_DISPONIVEIS)}."
            )
        self._id_personagem = novo_id

    @property
    def andando(self):
        """Indica se o jogador está se movimentando."""
        return self._andando

    @property
    def olhando_direita(self):
        """Indica se o personagem está virado para a direita."""
        return self._olhando_direita

    def definir_movimento(self, dx, dy, tempo, limites):
        """Atualiza animação, direção e posição conforme os comandos recebidos."""
        self._andando = dx != 0 or dy != 0

        if dx != 0:
            self._olhando_direita = dx > 0

        if dx != 0 and dy != 0:
            dx *= 0.70710678
            dy *= 0.70710678

        self.mover(dx, dy, tempo, limites)

    def interagir(self):
        """Retorna a mensagem de interação do jogador."""
        return f"{self.nome} está pronto para explorar a era."
