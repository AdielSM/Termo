from typing import List, Dict, Union
from enum import Enum

from .AVLtree import AVLtree
from utils import PilhaSequencial
from .palavrasRepository import carregarPalavras

class Estado(Enum):
    Sem_jogo = 1
    Jogo_com_tentativa = 2
    Jogo_sem_tentativa = 3
    # Para quando não houver limite de tentativas, implementação futura
    Jogo_ilimitado = 4
    Derrota = 5
    Vitoria = 6

class Termo:
    bancoPalavras: AVLtree = AVLtree()
    
    palavras = carregarPalavras()  # Carrega as palavras do palavrasRepository
    bancoPalavras.add_elements(palavras)
    del palavras

    def __init__(self, qtdTentativas: int = 5) -> None:
        self.__qtdTentativasRestantes: int = qtdTentativas
        self.__pilhaPalavras: PilhaSequencial = PilhaSequencial(qtdTentativas)
        self.__estadoDoJogo: Estado = Estado.Sem_jogo

        self.iniciarJogo(qtdTentativas)

    def iniciarJogo(self, qtdTentativas: int) -> None:
        self.__palavra: str = self.__escolherPalavraAleatoria()
        self.__dictPalavra: Dict[str, List[int]] = self.__criarDictPalavra(self.__palavra)
        self.__qtdTentativasRestantes: int = qtdTentativas
        self.__pilhaPalavras: PilhaSequencial = PilhaSequencial(qtdTentativas)
        self.__estadoDoJogo: Estado = Estado.Jogo_com_tentativa
        
    @property
    def palavra(self) -> str:
        return self.__palavra

    @property
    def qtdTentativasRestantes(self) -> int:
        return self.__qtdTentativasRestantes

    def getPalavrasTermo(self) -> List[str]:
        return Termo.palavrasTermo.inOrder()

    def jogoNaoIniciado(self) -> bool:
        return self.__estadoDoJogo == Estado.Sem_jogo

    def __escolherPalavraAleatoria(self) -> str:
        palavra: str = Termo.bancoPalavras.get_random()
        return palavra

    def __criarDictPalavra(self, palavra: str) -> Dict[str, List[int]]:
        dict_palavra: Dict[str, List[int]] = {}
        for i, letra in enumerate(palavra):
            if letra not in dict_palavra:
                dict_palavra[letra] = [i]
            else:
                dict_palavra[letra].append(i)
        return dict_palavra

    def checkWord(self, palavra: str) -> int | List[int]:
        # Só avança com tentativa
        if not self.__estadoDoJogo == Estado.Jogo_com_tentativa: pass

        if palavra == self.__palavra:
            self.__estadoDoJogo = Estado.Vitoria
            return 202
        
        elif len(palavra) != len(self.__palavra):
            return 403
        
        elif not Termo.bancoPalavras.is_present(palavra):
            return 404
        
        elif self.__pilhaPalavras.verifica_elemento(palavra):
            return 405
        
        feedback: List[int] = []
        for index, letra in enumerate(palavra):
            if letra in self.__dictPalavra and index in self.__dictPalavra[letra]:
                feedback.append(2)
            elif letra in self.__dictPalavra and index not in self.__dictPalavra[letra]:
                feedback.append(1)
            else:
                feedback.append(0)

        self.__qtdTentativasRestantes -= 1
        self.__pilhaPalavras.empilha(palavra)

        if self.__qtdTentativasRestantes == 0:
            self.__estadoDoJogo = Estado.Jogo_sem_tentativa
        
        return feedback
        
    
