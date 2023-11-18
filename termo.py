import nltk
import unidecode 
from nltk.corpus import floresta

from pilhaSequencial import PilhaSequencial
from AVLtree import AVLTree

class Termo:
    @staticmethod
    def __carregarPalavras() -> list[str]:
        nltk.download('floresta')

        def __sem_acentos(palavra):
            return all(letra.isalpha() and letra == unidecode.unidecode(letra) for letra in palavra)

        palavras = floresta.words()
        palavras_filtradas = [palavra.lower() for palavra in palavras if len(palavra) == 6 and __sem_acentos(palavra)]
        return palavras_filtradas
        
    palavras = AVLTree()
    palavras.add_elements(__carregarPalavras())


    def __init__(self, qtdTentativas:int=5) -> None:
        self.__palavra = ""
        self.__dictPalavra = {}
        self.__qtdTentativasRestantes = qtdTentativas

        self.iniciarJogo()

    def iniciarJogo(self, qtdTentativas:int=5):
        self.__palavra = self.__escolherPalavraAleatoria()
        self.__dictPalavra = self.__criarDictPalavra(self.__palavra)
        self.__qtdTentativasRestantes = qtdTentativas
        self.__pilhaPalavras = PilhaSequencial(qtdTentativas)
        
    @property
    def palavra(self):
        return self.__palavra
    
    @property
    def dictPalavra(self):
        return self.__dictPalavra
    
    @property
    def qtdTentativasRestantes(self):
        return self.__qtdTentativasRestantes
    
    def getPalavras(self):
        return Termo.palavras.inOrder(Termo.palavras.root)
    
    # Fazer
    def __str__(self) -> str:
        return f'{self.__jogador} x {self.__jogador2}'
    
    def __escolherPalavraAleatoria(self):
        palavra = Termo.palavras.get_random()
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
        if palavra == self.__palavra:
            return 'acertou'
        
        elif self.__pilhaPalavras.verifica_elemento(palavra):
            return 'Palavra repetida'
        
        elif len(palavra) != len(self.__palavra):
            return 'Tamanho incorreto'
        
        elif Termo.palavras.is_present(palavra):
            return 'Palavra inexistente'
        
        saida = ''
        for index,letra in enumerate(palavra):
            if letra in self.__dictPalavra and index in self.__dictPalavra[letra]:
                saida += '\033[92m' + letra + '\033[0m' #verde
            elif letra in self.__dictPalavra and index not in self.__dictPalavra[letra]:
                saida += '\033[93m' + letra + '\033[0m' #amarelo
            else:
                saida += '\033[90m' + letra + '\033[0m' #cinza escuro
        self.__qtdTentativasRestantes -= 1
        self.__pilhaPalavras.empilha(palavra)
        return saida    
                
            

if __name__ == '__main__':
    jogo = Termo()
    print(jogo.palavra)
    print(jogo.dictPalavra)
    print(jogo.checkPalavra('casual'))
    print(jogo.checkPalavra('banana'))
    print(jogo.checkPalavra('desejo'))
    # print(jogo.getPalavras())