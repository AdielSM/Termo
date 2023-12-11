from .termo import Termo
from time import time

from typing import Optional

class Player:
    """
    Classe que representa um jogador do jogo.
    """
    def __init__(self, client: str, con: str, user_name: str) -> None:
        self.__client = client
        self.__con = con
        self.__user_name = user_name
        self.__total_score = 0
        self.__rounds_scores = {}
        self.__current_round = 1
        self.__round_start_time = None
        self.__game = None

    @property
    def user_name(self) -> str:
        return self.__user_name

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

    @property
    def rounds_scores(self) -> dict:
        return self.__rounds_scores

    @property
    def round_start_time(self) -> Optional[float]:
        return self.__round_start_time


    def reset_round_start_time(self) -> None:
        """
        Reseta o tempo de início da rodada para None.
        """
        self.__round_start_time = None


    def turn_start(self) -> None:
        """
        Inicia o turno do jogador.

        Returns:
        None
        """
        self.__round_start_time = time()

    def add_score(self, remaining_attempts:int) -> None:
        """
        Adiciona a pontuação do jogador com base no número de tentativas restantes 
        e no tempo em segundos que a rodada durou.

        Parâmetros:
        remaining_attempts (int): O número de tentativas restantes.

        Retorna:
        None
        """

        if remaining_attempts != 0:    
            end_time_round = time()
            time_in_seconds = end_time_round - self.__round_start_time

            score = remaining_attempts + remaining_attempts / ( time_in_seconds % 10)

            self.__total_score += round(score, 2)
            self.__rounds_scores["Rodada " + str(self.__current_round)] = round(score, 2)

            self.__current_round += 1
            self.__round_start_time = None

        else:
            self.__rounds_scores["Rodada " + str(self.__current_round)] = 0
            self.__current_round += 1
            self.__round_start_time = None



    def restart(self):
        """
        Reinicia o jogador, limpando os scores das rodadas anteriores,
        reiniciando a rodada atual e iniciando um novo jogo.
        """
        self.__rounds_scores = {}
        self.__current_round = 1
        self.__game = Termo()
        self.turn_start()


    def __str__(self) -> str:
        """
        Retorna uma string que representa o objeto.

        Returns:
        str: Uma string que representa o objeto.
        """
        return f"Jogador: {self.__user_name} - Conexão: {self.__con} - Pontuação Total: {self.__total_score}"
