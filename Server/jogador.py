from .termo import Termo

class Jogador:
    """
    Classe que representa um jogador do jogo.
    """
    def __init__(self, cliente: str, con: str):
        self.__cliente = cliente
        self.__con = con
        self.__pontuacaoTotal = 0
        self.__pontuacaoNaRodada = 0
        self.__jogo = None
        
    @property
    def cliente(self) -> str:
        return self.__cliente
    
    @cliente.setter
    def cliente(self, cliente: str):
        self.__cliente = cliente
        
    @property
    def con(self) -> str:
        return self.__con
    
    @con.setter
    def con(self, con: str):
        self.__con = con
        
    @property
    def pontuacao(self) -> int:
        return self.__pontuacaoNaRodada
    
    @pontuacao.setter
    def pontuacao(self, pontuacao: int):
        self.__pontuacaoNaRodada = pontuacao
            
    @property
    def jogadorAtivo(self) -> bool:
        return self.__jogadorAtivo
    
    @jogadorAtivo.setter
    def jogadorAtivo(self, jogadorAtivo: bool):
        self.__jogadorAtivo = jogadorAtivo
        
    @property
    def jogadorVencedor(self) -> bool:
        return self.__jogadorVencedor
    
    @jogadorVencedor.setter
    def jogadorVencedor(self, jogadorVencedor: bool):
        self.__jogadorVencedor = jogadorVencedor
        
    @property
    def jogo(self) -> Termo:
        return self.__jogo
    
    @jogo.setter
    def jogo(self, jogo: Termo):
        self.__jogo = jogo

    def addPontuacao(self):
        self.__pontuacaoNaRodada += 1