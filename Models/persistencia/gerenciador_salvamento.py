#Gerencia o salvamento e o carregamento do perfil e do progresso.

import json
from Controllers.caminhos import ARQUIVO_SALVAMENTO


class GerenciadorSalvamento:

    def __init__(self, caminho=ARQUIVO_SALVAMENTO):
        self.caminho = caminho

    def salvar(self, dados):
        conteudo = json.dumps(
            dados,
            ensure_ascii=False,
            indent=2
        )

        self.caminho.write_text(conteudo, encoding="utf-8")

    def carregar(self):

        if not self.caminho.exists():
            return None

        try:
            conteudo = self.caminho.read_text(encoding="utf-8")
            return json.loads(conteudo)

        except (OSError, json.JSONDecodeError):
            return None

    def existe(self):
        return self.caminho.exists()
