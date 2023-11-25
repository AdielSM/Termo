from enum import Enum

class Resposta_CHECK_WORD(Enum):
    ACERTOU = {
        'status': "+ACERTOU",
        'msg_status': "Parabéns, você acertou!"
    }
    PALAVRA_REPETIDA = {
        'status': "-ERROU",
        'msg_status': 'Palavra repetida'
    }
    TAMANHO_INCORRETO = {
        'status': "-ERROU",
        'msg_status': 'Tamanho incorreto'
    }
    PALAVRA_INEXISTENTE = {
        'status': "-ERROU",
        'msg_status': 'Palavra inexistente'
    }