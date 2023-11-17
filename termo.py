from random import randint
from os import path
from json import load

class Termo:
    def __init__(self,jogador1,jogador2) -> None:
        self.__jogador1 = jogador1
        self.__jogador2 = jogador2
        self.__palavraJogador1 = self.__escolherPalavraAleatoria()
        self.__palavraJogador2 = self.__escolherPalavraAleatoria()
        while self.__palavraJogador2 == self.__palavraJogador1:
            self.__palavraJogador2 = self.__escolherPalavraAleatoria()
        self.__dictPalavra1 = self.__criarDictPalavra(self.__palavraJogador1)
        self.__dictPalavra2 = self.__criarDictPalavra(self.__palavraJogador2)
        self.__pontuacaoJogador1 = 0
        self.__pontuacaoJogador2 = 0

    @property
    def jogador1(self):
        return self.__jogador1
    
    @property
    def jogador2(self):
        return self.__jogador2
    
    @jogador1.setter
    def jogador1(self, jogador):
        self.__jogador1 = jogador

    @jogador2.setter
    def jogador2(self, jogador):
        self.__jogador2 = jogador

    @property
    def palavraJogador1(self):
        return self.__palavraJogador1
    
    @property
    def palavraJogador2(self):
        return self.__palavraJogador2
    
    @property
    def dictPalavra1(self):
        return self.__dictPalavra1
    
    @property
    def dictPalavra2(self):
        return self.__dictPalavra2
    
    @property
    def pontuacaoJogador1(self):
        return self.__pontuacaoJogador1
    
    @property
    def pontuacaoJogador2(self):
        return self.__pontuacaoJogador2
    
    def __str__(self) -> str:
        return f'{self.__jogador1} x {self.__jogador2}'
    
    def __escolherPalavraAleatoria(self):
        with open(path.join(path.dirname(__file__),'palavras.json'),'r') as arquivo:
            palavras = load(arquivo)
            palavra = palavras[randint(0,len(palavras)-1)]
        return palavra
    
    def __criarDictPalavra(self, palavra):
        dict_palavra = {}
        for i, letra in enumerate(palavra):
            if letra not in dict_palavra:
                dict_palavra[letra] = [i]
            else:
                dict_palavra[letra].append(i)
        return dict_palavra