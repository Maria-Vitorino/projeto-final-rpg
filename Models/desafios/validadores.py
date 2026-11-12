from abc import ABC, abstractmethod
import unicodedata


def normalizar_texto(texto):
    texto = str(texto).strip().lower()
    texto = unicodedata.normalize("NFKD", texto)

    resultado = ""

    for caractere in texto:
        if not unicodedata.combining(caractere) and not unicodedata.category(caractere).startswith("P"):
            resultado += caractere

    return resultado


class ValidadorResposta(ABC):

    @abstractmethod
    def validar(self, pergunta, resposta):
        pass


class ValidadorNumerico(ValidadorResposta):

    def validar(self, pergunta, resposta):
        try:
            resposta = float(resposta.strip().replace(",", ".").replace("%", ""))
            correta = float(pergunta["resposta_numerica"])
            tolerancia = float(pergunta.get("tolerancia", 0.01))

            diferenca = abs(resposta - correta)

            return diferenca <= tolerancia

        except (ValueError, TypeError, KeyError):
            return False


class ValidadorTexto(ValidadorResposta):

    def validar(self, pergunta, resposta):
        resposta = normalizar_texto(resposta)
        criterios = pergunta.get("criterios_resposta", [])

        if resposta == "" or criterios == []:
            return False

        for grupo in criterios:
            encontrou = False

            for termo in grupo:
                termo = normalizar_texto(termo)

                if termo in resposta:
                    encontrou = True
                    break

            if not encontrou:
                return False

        return True


class ValidadorAlternativas(ValidadorResposta):

    def validar(self, pergunta, resposta):
        resposta = normalizar_texto(resposta)
        alternativas = pergunta.get("respostas_aceitas", [])

        for alternativa in alternativas:
            if resposta == normalizar_texto(alternativa):
                return True

        return False


class FabricaValidadores:

    @staticmethod
    def criar(tipo):

        if tipo == "numero":
            return ValidadorNumerico()

        elif tipo == "texto":
            return ValidadorTexto()

        elif tipo == "alternativas":
            return ValidadorAlternativas()

        else:
            return ValidadorTexto()
