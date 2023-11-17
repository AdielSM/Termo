from random import randint
from os import path
from json import load

class Termo:
    @staticmethod
    def __carregarPalavras()->list[str]:
        with open(path.join(path.dirname(__file__),'palavras.json'),'r') as arquivo:
            palavras = load(arquivo)
        return palavras

    palavras = __carregarPalavras()

    def __init__(self, qtdTentativas:int=5) -> None:
        self.__palavra = ""
        self.__dictPalavra = {}
        self.__qtdTentativasRestantes = qtdTentativas

        self.iniciarJogo()

    def iniciarJogo(self, qtdTentativas:int=5):
        self.__palavra = self.__escolherPalavraAleatoria()
        self.__dictPalavra = self.__criarDictPalavra(self.__palavra)
        self.__qtdTentativasRestantes = qtdTentativas

    @property
    def palavra(self):
        return self.__palavra
    
    @property
    def dictPalavra(self):
        return self.__dictPalavra
    
    @property
    def qtdTentativasRestantes(self):
        return self.__qtdTentativasRestantes
    
    # Fazer
    def __str__(self) -> str:
        return f'{self.__jogador} x {self.__jogador2}'
    
    def __escolherPalavraAleatoria(self):
        palavra = Termo.palavras[randint(0,len(Termo.palavras)-1)]
        # with open(path.join(path.dirname(__file__),'palavras.json'),'r') as arquivo:
            # palavras = load(arquivo)
            # palavra = palavras
        return palavra
    
    def __criarDictPalavra(self, palavra:str):
        dict_palavra = {}
        for i, letra in enumerate(palavra):
            if letra not in dict_palavra:
                dict_palavra[letra] = [i]
            else:
                dict_palavra[letra].append(i)
        return dict_palavra
    
    def checkPalavra(self, palavra:str):
        saida = ''
        
        for index,letra in enumerate(palavra):
            if letra in self.__dictPalavra and index in self.__dictPalavra[letra]:
                saida += '\033[92m' + letra + '\033[0m' #verde
            elif letra in self.__dictPalavra and index not in self.__dictPalavra[letra]:
                saida += '\033[93m' + letra + '\033[0m' #amarelo
            else:
                saida += '\033[90m' + letra + '\033[0m' #cinza escuro
        return saida    
                
            

if __name__ == '__main__':
    jogo = Termo()
    print(jogo.palavra)
    print(jogo.dictPalavra)
    print(jogo.checkPalavra('casual'))
    print(jogo.checkPalavra('banana'))
    print(jogo.checkPalavra('desejo'))