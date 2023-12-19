from enum import Enum
from player import Player;
from termo import Termo;

class party_state(Enum):
    """
    Enum que representa o estado da party.

    - WAITING_TO_START: Estado inicial, quando a party ainda não começou.
    - GAME_IN_PROGRESS: Estado quando a party está em andamento.
    - GAME_FINISHED: Estado quando a party terminou.
    """
    WAITING_TO_START = 1
    GAME_IN_PROGRESS = 2
    GAME_FINISHED = 3

class Party:
    """
    Classe que representa uma party de players do jogo Termo.

    Métodos:
        add_player(player: Player): Adiciona um player à party.
        remove_player(player: Player): Remove um player da party.
        start_game(): Inicia o jogo da party.
    """
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
        """
        Adiciona um player à party.
        
        Args:
            player (Player): O player a ser adicionado.

        Returns:
            None

        """
        # Caso o jogo esteja em andamento, não é possivel adicionar
        if(self.__party_state == party_state.GAME_IN_PROGRESS):
            # Tratar com código de retorno
            return
        
        player.game = self.__game
        self.__players.append(player)

    def remove_player(self, player: Player):
        """
        Remove um player da party.

        Args:
            player (Player): O player a ser removido.

        Returns:
            None
        """
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
        """
        Inicia o jogo da Party.

        Args:
            A própria Party.

        Returns:
            None
        
        """
        if(self.__game.game_not_started()):
            self.__game.start_game()
        
        self.__party_state = party_state.GAME_IN_PROGRESS

        # Tratar com retorno de sucesso
        return