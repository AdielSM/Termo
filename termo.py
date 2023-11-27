from typing import List, Dict, Union
from enum import Enum

from Estruturas import AVLtree, PilhaSequencial

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
    
    @staticmethod
    def __carregarPalavras():
        if not Termo.bancoPalavras:  # Verifica se as palavras já foram carregadas
            with open('.txt/bancoDePalavras.txt', 'r') as arquivo:
                palavras = [palavra.strip().replace('\x00', '') for palavra in arquivo.readlines()]
                Termo.bancoPalavras.add_elements(palavras)
                Termo.palavras = palavras  # Armazena as palavras na variável de classe

    def __init__(self, qtdTentativas: int = 5) -> None:
        Termo.__carregarPalavras()  # Carrega as palavras, se ainda não foram carregadas

        self.__qtdTentativasRestantes: int = qtdTentativas
        self.__pilhaPalavras: PilhaSequencial = PilhaSequencial(qtdTentativas)
        self.__estadoDoJogo = Estado.Sem_jogo

        self.iniciarJogo(qtdTentativas)

    def iniciarJogo(self, qtdTentativas) -> None:
        self.__palavra = self.__escolherPalavraAleatoria()
        self.__dictPalavra = self.__criarDictPalavra(self.__palavra)
        self.__qtdTentativasRestantes = qtdTentativas
        self.__pilhaPalavras = PilhaSequencial(qtdTentativas)
        self.__estadoDoJogo = Estado.Jogo_com_tentativa
        

    @property
    def palavra(self) -> str:
        return self.__palavra

    @property
    def dictPalavra(self) -> Dict[str, List[int]]:
        return self.__dictPalavra.copy()

    @property
    def qtdTentativasRestantes(self) -> int:
        return self.__qtdTentativasRestantes

    def getPalavrasTermo(self) -> List[str]:
        return Termo.palavrasTermo.inOrder()

    def __str__(self) -> str:
        return f'{self.__jogador} x {self.__jogador2}'

    def jogoNaoIniciado(self) -> bool:
        return self.__estadoDoJogo == Estado.Sem_jogo

    def __escolherPalavraAleatoria(self) -> str:
        palavra = Termo.bancoPalavras.get_random()
        return palavra

    def __criarDictPalavra(self, palavra: str) -> Dict[str, List[int]]:
        dict_palavra = {}
        for i, letra in enumerate(palavra):
            if letra not in dict_palavra:
                dict_palavra[letra] = [i]
            else:
                dict_palavra[letra].append(i)
        return dict_palavra

    def checkWord(self, palavra: str) -> Union[str, None]:
        # Só avança com tentativa
        if not self.__estadoDoJogo == Estado.Jogo_com_tentativa: pass

        if palavra == self.__palavra:
            self.__estadoDoJogo = Estado.Vitoria
            return "Palavra Correta."
        
        # A ser tratado no cliente
        elif self.__pilhaPalavras.verifica_elemento(palavra):
            return 'Palavra Repetida'
        
        elif len(palavra) != len(self.__palavra):
            return 'Tamanho Incorreto'
        
        elif not Termo.bancoPalavras.is_present(palavra):
            return 'Palavra Inexistente'
        
        feedback = []
        for index, letra in enumerate(palavra):
            if letra in self.__dictPalavra and index in self.__dictPalavra[letra]:
                feedback.append('green')
            elif letra in self.__dictPalavra and index not in self.__dictPalavra[letra]:
                feedback.append('yellow')
            else:
                feedback.append('gray')

        self.__qtdTentativasRestantes -= 1
        self.__pilhaPalavras.empilha(palavra)

        if self.__qtdTentativasRestantes == 0:
            self.__estadoDoJogo = Estado.Jogo_sem_tentativa
        
        return feedback
        

    # é necessário fazer a lógica do print da animação no cliente ou no servidor (possivelmente no cliente)
    def animacao_palavra_secreta(self):
        palavra_transformada = ['_' for _ in self.__palavra]
        animacao = []
        
        animacao.append('Você perdeu! A palavra era:')
        
        for i in range(len(self.__palavra)):
            palavra_transformada[i] = self.__palavra[i]
            animacao.append(''.join(palavra_transformada))
        
        return animacao


