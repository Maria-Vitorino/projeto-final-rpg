from dataclasses import dataclass
from .validadores import FabricaValidadores


@dataclass(frozen=True)
class Pergunta:

    dados: dict

    @property
    def id_pergunta(self):
        return self.dados["id"]

    @property
    def nome(self):
        return self.dados.get("npc_nome", "Habitante da época")

    @property
    def enunciado(self):
        return self.dados.get("enigma", "")

    @property
    def explicacao(self):
        return self.dados.get("explicacao", "")

    @property
    def pontos(self):
        return int(self.dados.get("pontos", 100))

    @property
    def opcoes(self):
        return self.dados.get("opcoes", [])

    def verificar_resposta(self, resposta):
        validador = FabricaValidadores.criar(
            self.dados.get("tipo_validacao", "texto")
        )

        return validador.validar(self.dados, resposta)