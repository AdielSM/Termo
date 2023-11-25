from typing import List, Dict, Union
from enum import Enum

from Estruturas.pilhaSequencial import PilhaSequencial
from Estruturas.AVLtree import AVLTree

class Estado(Enum):
    Sem_jogo = 1
    Jogo_com_tentativa = 2
    Jogo_sem_tentativa = 3
    # Para quando não houver limite de tentativas, implementação futura
    Jogo_ilimitado = 4
    Derrota = 5
    Vitoria = 6

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

    # Palavras para validação
    bancoPalavras: AVLTree = AVLTree()
    bancoPalavras.add_elements(__carregarPalavras())

    # Palavras para sorteio
    palavrasTermo: AVLTree = AVLTree()
    palavrasTermo.add_elements(__carregarPalavrasTermo())

    def __init__(self, qtdTentativas: int = 5) -> None:
        self.__palavra: str = ""
        self.__dictPalavra: Dict[str, List[int]] = {}
        self.__qtdTentativasRestantes: int = qtdTentativas

        # Corrigir pilha pro lado do cliente, aqui está no servidor
        self.__pilhaPalavras: PilhaSequencial = PilhaSequencial(qtdTentativas)
        self.__estadoDoJogo = Estado.Sem_jogo

        self.iniciarJogo(qtdTentativas)

    def iniciarJogo(self, qtdTentativas: int = 5) -> None:
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
        return self.__dictPalavra

    @property
    def qtdTentativasRestantes(self) -> int:
        return self.__qtdTentativasRestantes

    def getPalavrasTermo(self) -> List[str]:
        return Termo.palavrasTermo.inOrder()

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
        # Só avança com tentativa
        if not self.__estadoDoJogo == Estado.Jogo_com_tentativa: pass

        if palavra == self.__palavra:
            self.__estadoDoJogo = Estado.Vitoria
            return 'acertou'
        
        # A ser tratado no cliente
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

        # if self.__verificaDerrota():
        if self.__qtdTentativasRestantes == 0:
            self.__estadoDoJogo = Estado.Jogo_sem_tentativa
            return self.__animacao_palavra_secreta()
        return saida
        
    def __verificaDerrota(self):
        return self.__qtdTentativasRestantes == 0

    # é necessário fazer a lógica do print da animação no cliente ou no servidor (possivelmente no cliente)
    def __animacao_palavra_secreta(self):
        palavra_transformada = ['_' for _ in self.__palavra]
        animacao = []
        
        animacao.append('Você perdeu! A palavra era:')
        
        for i in range(len(self.__palavra)):
            palavra_transformada[i] = self.__palavra[i]
            animacao.append(''.join(palavra_transformada))
        
        return ' '.join(animacao)

#* Para testes internos
# if __name__ == '__main__':
#     jogo = Termo()
#     print(jogo.palavra)
#     print(jogo.dictPalavra)
#     print(jogo.checkPalavra('wertyu'))
#     print(jogo.checkPalavra('banana'))
#     print(jogo.checkPalavra('desejo'))
#     # jogo.getPalavras()