class SessaoJogo:

    MAX_VIDAS = 3

    def __init__(self):
        self.reiniciar()

    def reiniciar(self):
        self._indice_era = 0
        self._vidas = self.MAX_VIDAS
        self._pontuacao = 0
        self._npcs_concluidos = set()

    @property
    def indice_era(self):
        return self._indice_era

    @property
    def vidas(self):
        return self._vidas

    @property
    def pontuacao(self):
        return self._pontuacao

    @property
    def npcs_concluidos(self):
        return frozenset(self._npcs_concluidos)

    @property
    def quantidade_concluida(self):
        return len(self._npcs_concluidos)

    @property
    def era_concluida(self):
        return self.quantidade_concluida >= 3

    def perder_vida(self):
        if self._vidas > 0:
            self._vidas -= 1

        return self._vidas == 0

    def concluir_npc(self, id_npc, pontos):

        if id_npc not in self._npcs_concluidos:
            self._npcs_concluidos.add(id_npc)
            self._pontuacao += max(0, int(pontos))

            return True

        return False

    def proxima_era(self):
        self._indice_era += 1
        self._vidas = self.MAX_VIDAS
        self._npcs_concluidos.clear()

    def restaurar(self, indice_era, vidas, pontuacao, npcs_concluidos=()):

        self._indice_era = max(0, int(indice_era))
        self._vidas = max(1, min(int(vidas), self.MAX_VIDAS))
        self._pontuacao = max(0, int(pontuacao))

        self._npcs_concluidos = {
            str(item) for item in npcs_concluidos
        }

    def voltar_ao_inicio(self):

        pontuacao_total = self._pontuacao

        self.reiniciar()

        # A nova jornada começa sem pontuação ou encontros anteriores.
        return pontuacao_total