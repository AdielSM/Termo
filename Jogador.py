class Jogador:
    def __init__(self, cliente: str, con: str):
        self.__cliente = cliente
        self.__con = con
        self.__pontuacao = 0
        self.__jogadorAtivo = False
        self.__jogadorVencedor = False
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
        return self.__pontuacao
    
    @pontuacao.setter
    def pontuacao(self, pontuacao: int):
        self.__pontuacao = pontuacao
            
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
    def jogo(self) -> str:
        return self.__jogo
    
    @jogo.setter
    def jogo(self, jogo: str):
        self.__jogo = jogo

    def addPontuacao(self):
        self.__pontuacao += 1