from Estruturas.pilhaSequencial import PilhaSequencial
from Estruturas.AVLtree import AVLTree
from typing import List, Dict, Union
import time 
import sys

class Termo:
    @staticmethod
    def __carregarPalavras() -> List[str]:
        with open('.txt/bancoDePalavras.txt', 'r') as arquivo:
            palavras = [palavra.strip() for palavra in arquivo.readlines()]
            palavras = [palavra.replace('\x00', '') for palavra in palavras]
            return palavras

    @staticmethod
    def __carregarPalavrasTermo() -> List[str]:
        with open('.txt/listaPalavrasTermo.txt', 'r') as arquivo:
            palavras = [palavra.strip() for palavra in arquivo.readlines()]
            return palavras

    bancoPalavras: AVLTree = AVLTree()
    bancoPalavras.add_elements(__carregarPalavras())
    palavrasTermo: AVLTree = AVLTree()
    palavrasTermo.add_elements(__carregarPalavrasTermo())

    def __init__(self, qtdTentativas: int = 5) -> None:
        self.__palavra: str = ""
        self.__dictPalavra: Dict[str, List[int]] = {}
        self.__qtdTentativasRestantes: int = qtdTentativas
        self.__pilhaPalavras: PilhaSequencial = PilhaSequencial(qtdTentativas)

        self.iniciarJogo(qtdTentativas)

    def iniciarJogo(self, qtdTentativas: int = 5) -> None:
        self.__palavra = self.__escolherPalavraAleatoria()
        self.__dictPalavra = self.__criarDictPalavra(self.__palavra)
        self.__qtdTentativasRestantes = qtdTentativas
        self.__pilhaPalavras = PilhaSequencial(qtdTentativas)

    @property
    def palavra(self) -> str:
        return self.__palavra

    @property
    def dictPalavra(self) -> Dict[str, List[int]]:
        return self.__dictPalavra

    @property
    def qtdTentativasRestantes(self) -> int:
        return self.__qtdTentativasRestantes

    def getPalavras(self) -> List[str]:
        return Termo.palavras.inOrder(Termo.palavras.root)

    def __str__(self) -> str:
        return f'{self.__jogador} x {self.__jogador2}'

    def __escolherPalavraAleatoria(self) -> str:
        palavra = Termo.palavrasTermo.get_random()
        return palavra

    def __criarDictPalavra(self, palavra: str) -> Dict[str, List[int]]:
        dict_palavra = {}
        for i, letra in enumerate(palavra):
            if letra not in dict_palavra:
                dict_palavra[letra] = [i]
            else:
                dict_palavra[letra].append(i)
        return dict_palavra

    def checkPalavra(self, palavra: str) -> Union[str, None]:
        
        if palavra == self.__palavra:
            return 'acertou'
        
        elif self.__pilhaPalavras.verifica_elemento(palavra):
            return 'Palavra repetida'
        
        elif len(palavra) != len(self.__palavra):
            return 'Tamanho incorreto'
        
        elif not Termo.bancoPalavras.is_present(palavra):
            return 'Palavra inexistente'
        
        saida = ''
        for index, letra in enumerate(palavra):
            if letra in self.__dictPalavra and index in self.__dictPalavra[letra]:
                saida += '\033[92m' + letra + '\033[0m' #verde
            elif letra in self.__dictPalavra and index not in self.__dictPalavra[letra]:
                saida += '\033[93m' + letra + '\033[0m' #amarelo
            else:
                saida += '\033[90m' + letra + '\033[0m' #cinza escuro
        
        self.__qtdTentativasRestantes -= 1
        self.__pilhaPalavras.empilha(palavra)
        
        if self.__verificaDerrota():
            return self.__animacao_palavra_secreta()
        else:
            return saida
    

    def __verificaDerrota(self):
        return self.__qtdTentativasRestantes == 0

    # é necessário fazer a lógica do print da animação no cliente ou no servidor (possivelmente no cliente)
    def __animacao_palavra_secreta(self):
        palavra_transformada = ['_' for _ in self.__palavra]
        animacao = []
        
        animacao.append('Você perdeu! A palavra era: ')
        
        for i in range(len(self.__palavra)):
            palavra_transformada[i] = self.__palavra[i]
            animacao.append(''.join(palavra_transformada))
        
        return animacao

if __name__ == '__main__':
    jogo = Termo(qtdTentativas=1)
    print(jogo.palavra)
    print(jogo.dictPalavra)
    entrado = input()
    print(jogo.checkPalavra(entrado))

    

