from .termo import Termo

class Player:
    """
    Classe que representa um jogador do jogo.
    """
    def __init__(self, client: str, con: str):
        self.__client = client
        self.__con = con
        self.__total_score = 0
        self.__game = None

    @property
    def client(self) -> str:
        return self.__client

    @property
    def con(self) -> str:
        return self.__con

    @property
    def game(self) -> Termo:
        return self.__game

    @game.setter
    def game(self, game: Termo):
        self.__game = game

    @property
    def total_score(self) -> int:
        return self.__total_score


    def add_score(self, remaining_attempts:int, time_in_seconds:int) -> None:
        """
        Adiciona a pontuação do jogador com base no número de tentativas restantes 
        e no tempo em segundos.

        Parâmetros:
        remaining_attempts (int): O número de tentativas restantes.
        time_in_seconds (int): O tempo em segundos.

        Retorna:
        None
        """
        score = remaining_attempts + remaining_attempts / (time_in_seconds % 10)
        self.__total_score += score


    def reset_score(self) -> None:
        """
        Reseta a pontuação do jogador.

        Returns:
        None
        """
        self.__total_score = 0


    def __str__(self) -> str:
        """
        Retorna uma string que representa o objeto.

        Returns:
        str: Uma string que representa o objeto.
        """
        return f"Jogador: {self.__client} - Conexão: {self.__con} - Pontuação: {self.__total_score}"
