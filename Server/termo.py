from typing import List, Dict, Union
from enum import Enum

from .AVLtree import AVLtree
from utils import PilhaSequencial, sumario_protocolo
from .palavrasRepositorio import carregarPalavras, carregarPalavrasTermo

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
    bancoPalavrasTermo: AVLtree = AVLtree()
    protocolo = sumario_protocolo()
    
    palavras = carregarPalavras()  # Carrega as palavras do palavrasRepositorio
    bancoPalavras.add_elements(palavras)
    del palavras
    
    palavrasTermo = carregarPalavrasTermo()  # Carrega as palavras do palavrasRepositorio
    bancoPalavrasTermo.add_elements(palavrasTermo)
    del palavrasTermo
    
    def __init__(self, qtdTentativas: int = 5) -> None:
        self.__estadoDoJogo: Estado = Estado.Sem_jogo

        self.iniciarJogo(qtdTentativas)

    def iniciarJogo(self, qtdTentativas: int = 5) -> None:
        """
        Inicia o jogo com a quantidade de tentativas especificada.

        Args:
            qtdTentativas (int): A quantidade de tentativas disponíveis.

        Returns:
            None
        """
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
        palavra: str = Termo.bancoPalavrasTermo.get_random()
        return palavra

    def __criarDictPalavra(self, palavra: str) -> Dict[str, List[int]]:
        """
        Cria um dicionário onde as chaves são as letras da palavra e os valores são as posições em que as letras aparecem na palavra.

        Args:
            palavra (str): A palavra para criar o dicionário.

        Returns:
            Dict[str, List[int]]: O dicionário onde as chaves são as letras da palavra e os valores são as posições em que as letras aparecem na palavra.
        """
        dict_palavra: Dict[str, List[int]] = {}
        for i, letra in enumerate(palavra):
            if letra not in dict_palavra:
                dict_palavra[letra] = [i]
            else:
                dict_palavra[letra].append(i)
        return dict_palavra

    def checkWord(self, palavra: str) -> Union[int, List[int]]:
        """
        Verifica se a palavra fornecida é válida de acordo com as regras do jogo.

        Args:
            palavra (str): A palavra a ser verificada.

        Returns:
            Union[int, List[int]]: O feedback da palavra ou um código de erro.

        Raises:
            ValueError: Se o jogo não estiver no estado de tentativa.

        """
        # Verifica se o estado do jogo permite uma tentativa
        if self.__estadoDoJogo != Estado.Jogo_com_tentativa:
            raise ValueError("O jogo não está no estado de tentativa")

        # Verifica se a palavra é igual à palavra do jogo
        if palavra == self.__palavra:
            self.__estadoDoJogo = Estado.Vitoria
            return Termo.protocolo["PALAVRA_CORRETA"]

        # Verifica se a palavra tem o mesmo tamanho que a palavra do jogo
        elif len(palavra) != len(self.__palavra):
            return Termo.protocolo["TAMANHO_INCORRETO"]

        # Verifica se a palavra está presente no banco de palavras
        elif not Termo.bancoPalavras.is_present(palavra) and not Termo.bancoPalavrasTermo.is_present(palavra):
            return Termo.protocolo["PALAVRA_INEXISTENTE"]

        # Verifica se a palavra já foi tentada antes
        elif self.__pilhaPalavras.verifica_elemento(palavra):
            return Termo.protocolo["PALAVRA_REPETIDA"]

        # Gera o feedback para a palavra
        feedback = self.__generateFeedback(palavra)

        self.__qtdTentativasRestantes -= 1
        self.__pilhaPalavras.empilha(palavra)

        # Verifica se o jogo ainda tem tentativas restantes
        if self.__qtdTentativasRestantes == 0:
            self.__estadoDoJogo = Estado.Jogo_sem_tentativa

        return feedback

    def __generateFeedback(self, palavra: str) -> List[int]:
        """Gera o feedback para uma palavra com base na palavra do jogo."""
        feedback: List[int] = []
        for index, letra in enumerate(palavra):
            if letra in self.__dictPalavra and index in self.__dictPalavra[letra]:
                feedback.append(2)
            elif letra in self.__dictPalavra and index not in self.__dictPalavra[letra]:
                feedback.append(1)
            else:
                feedback.append(0)
        return feedback
    