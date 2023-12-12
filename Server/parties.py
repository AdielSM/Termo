from enum import Enum
from player import Player;
from termo import Termo;

class party_state(Enum):
    WAITING_TO_START = 1
    GAME_IN_PROGRESS = 2
    GAME_FINISHED = 3

class Party:
    def __init__(self, id: int, host_player: Player, game: Termo):
        self.__id = id
        self.__host_player = host_player
        self.__players = [host_player]
        self.__qtd_players = 1
        self.__game = Termo(unlimited_attempts=True)
        self.__party_state = party_state.WAITING_TO_START

    @property
    def id(self):
        return self.__id

    def add_player(self, player: Player):
        # Caso o jogo esteja em andamento, não é possivel adicionar
        if(self.__party_state == party_state.GAME_IN_PROGRESS):
            # Tratar com código de retorno
            return
        
        player.game = self.__game
        self.__players.append(player)

    def remove_player(self, player: Player):
        if(player in self.__players):
            is_host_player = player == self.__host_player
            if(is_host_player and self.__qtd_players > 1):
                self.__host_player = self.__players[1]
                # Retornar algo pra indicar troca de host?
            elif(is_host_player and self.__qtd_players == 1):
                self.__del__()
                # Tem que tratar essa party retirando-a e retornando como código

            self.__players.remove(player)
            # Retornar código de sucesso

    def start_game(self):
        if(self.__game.game_not_started()):
            self.__game.start_game()
        
        self.__party_state = party_state.GAME_IN_PROGRESS

        # Tratar com retorno de sucesso
        return