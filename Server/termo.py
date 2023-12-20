from typing import List, Dict, Union
from enum import Enum

from utils import LinkedStack, summary_protocol
from .words_loader import load_words
from .termo_words_loader import load_termo_words
from .AVLtree import AVLtree

class TermoStatus(Enum):
    """
    Enumeração que representa os possíveis estados do jogo.
    
    - NO_GAME: Estado inicial, quando não há jogo em andamento.
    - GAME_WITH_TRY: Estado quando há um jogo em andamento e o jogador fez pelo menos uma tentativa.
    - GAME_WITHOUT_TRY: Estado quando há um jogo em andamento e o jogador ainda não fez nenhuma tentativa.
    - DEFEAT: Estado quando o jogador perdeu o jogo.
    - VICTORY: Estado quando o jogador venceu o jogo.
    """
    NO_GAME = 1
    GAME_WITH_TRY = 2
    GAME_WITHOUT_TRY = 3
    DEFEAT = 4
    VICTORY = 5

class Termo:
    """
    Classe que representa o jogo termo.

    Atributos:
        word_bank (AVLtree): Árvore AVL que armazena o banco de palavras.
        termo_word_bank (AVLtree): Árvore AVL que armazena o banco de palavras específico do jogo termo.
        protocol (summary_protocol): Objeto que contém o protocolo do jogo termo.

    Métodos:
        start_game(attempts_number: int = 5, unlimited_attempts:bool = False): Inicia o jogo com o número especificado de tentativas.
        get_termo_words(): Retorna a lista de palavras específicas do jogo termo.
        game_not_started(): Verifica se o jogo não foi iniciado.
        check_word(word: str): Verifica se a palavra fornecida é válida de acordo com as regras do jogo.
        __choose_random_word(): Escolhe uma palavra aleatória do banco de palavras específico do jogo termo.
        __create_word_dict(letters: str): Cria um dicionário onde as chaves são as letras da palavra e os valores são as posições onde as letras aparecem na palavra.
        __generate_feedback(word: str): Gera o feedback para uma palavra com base na palavra do jogo.
    """

    word_bank: AVLtree = AVLtree()
    termo_word_bank: AVLtree = AVLtree()
    protocol = summary_protocol()

    words = load_words()  # Carrega as palavras do wordRepository
    word_bank.add_elements(words)
    del words

    termo_words = load_termo_words()  # Carrega as palavras do wordRepository
    termo_word_bank.add_elements(termo_words)
    del termo_words

    def __init__(self, attempts_number: int = 5, unlimited_attempts:bool = False) -> None:
        """
        Inicializa uma instância da classe termo.

        Args:
            attempts_number (int): O número de tentativas disponíveis.
            unlimited_attempts (bool): Indica se o jogo terá tentativas ilimitadas.

        Returns:
            None
        """
        self.__game_status: TermoStatus = TermoStatus.NO_GAME

        self.start_game(attempts_number, unlimited_attempts)

    def start_game(self, attempts_number: int = 5, unlimited_attempts: bool = False) -> None:
        """
        Inicia o jogo com o número especificado de tentativas.

        Args:
            attempts_number (int): O número de tentativas disponíveis.
            unlimited_attempts (bool): Indica se o jogo terá tentativas ilimitadas.

        Returns:
            None
        """
        self.__secret_word: str = self.__choose_random_word()
        self.__dict_secret_word: Dict[str, List[int]] = self.__create_word_dict(self.__secret_word)
        self.__unlimited_attempts = unlimited_attempts
        self.__remaining_attempts: int = attempts_number if not unlimited_attempts else -1
        self.__words_stack: LinkedStack = LinkedStack()
        self.__game_status = TermoStatus.GAME_WITH_TRY


    @property
    def game_status(self) -> TermoStatus:
        """
        Retorna o estado do jogo.

        Args:
            None

        Returns:
            TermoStatus: O estado do jogo.
        """
        return self.__game_status


    @property
    def secret_word(self) -> str:
        """
        Retorna a palavra do jogo.

        Args:
            None

        Returns:
            str: A palavra do jogo.
        """
        return self.__secret_word

    @property
    def remaining_attempts(self) -> int:
        """
        Retorna o número de tentativas restantes.

        Args:
            None

        Returns:
            int: O número de tentativas restantes.
        """
        return self.__remaining_attempts

    def get_termo_words(self) -> List[str]:
        """
        Retorna a lista de palavras específicas do jogo termo.

        Args:
            None

        Returns:
            List[str]: A lista de palavras específicas do jogo termo.
        """
        return Termo.termo_word_bank.in_order()

    def game_not_started(self) -> bool:
        """
        Verifica se o jogo não foi iniciado.

        Args:
            None

        Returns:
            bool: True se o jogo não foi iniciado, False caso contrário.
        """
        return self.__game_status == TermoStatus.NO_GAME

    def __choose_random_word(self) -> str:
        """
        Escolhe uma palavra aleatória do banco de palavras específico do jogo termo.

        Args:
            None

        Returns:
            str: A palavra escolhida aleatoriamente.
        """
        word: str = Termo.termo_word_bank.get_random()
        return word

    def __create_word_dict(self, letters: str) -> Dict[str, List[int]]:
        """
        Cria um dicionário onde as chaves são as letras da palavra e os valores são as posições 
        onde as letras aparecem na palavra.

        Args:
            letters (str): A palavra para criar o dicionário.

        Returns:
            Dict[str, List[int]]: O dicionário onde as chaves são as letras da palavra e os valores 
            são as posições onde as letras aparecem na palavra.
        """
        word_dict: Dict[str, List[int]] = {}
        for i, letter in enumerate(letters):
            if letter not in word_dict:
                word_dict[letter] = [i]
            else:
                word_dict[letter].append(i)
        return word_dict

    def check_word(self, word: str) -> Union[int, List[int]]:
        """
        Verifica se a palavra fornecida é válida de acordo com as regras do jogo.

        Args:
            word (str): A palavra a ser verificada.

        Returns:
            Union[int, List[int]]: O feedback da palavra ou um código de erro.

        Raises:
            ValueError: Se o jogo não estiver no estado de tentativa.

        """
        # Verifica se o estado do jogo permite uma tentativa
        if self.__game_status != TermoStatus.GAME_WITH_TRY:
            raise ValueError("O jogo não está no estado de tentativa")

        # Verifica se a palavra é igual à palavra do jogo
        if word == self.__secret_word:
            self.__game_status = TermoStatus.VICTORY
            return Termo.protocol["PALAVRA_CORRETA"]

        # Verifica se a palavra tem o mesmo tamanho que a palavra do jogo
        elif len(word) != len(self.__secret_word):
            return Termo.protocol["TAMANHO_INCORRETO"]

        # Verifica se a palavra está presente no banco de palavras
        elif not (Termo.word_bank.is_present(word) or Termo.termo_word_bank.is_present(word)):
            return Termo.protocol["PALAVRA_INEXISTENTE"]

        # Verifica se a palavra já foi tentada antes
        if self.__words_stack.search(word):
            return Termo.protocol["PALAVRA_REPETIDA"]

        # Gera o feedback para a palavra
        feedback = self.__generate_feedback(word)

        if not self.__unlimited_attempts:
            self.__remaining_attempts -= 1
        self.__words_stack.stack_up(word)

        # Verifica se o jogo ainda tem tentativas restantes
        if self.__remaining_attempts == 0 and not self.__unlimited_attempts:
            self.__game_status = TermoStatus.GAME_WITHOUT_TRY

        return feedback

    def __generate_feedback(self, word: str) -> List[int]:
        """
        Gera o feedback para uma palavra com base na palavra do jogo.

        Args:
            word (str): A palavra a ser verificada.

        Returns:
            List[int]: O feedback da palavra.
        """
        feedback: List[int] = []
        for index, letter in enumerate(word):
            if letter in self.__dict_secret_word and index in self.__dict_secret_word[letter]:
                feedback.append(2)
            elif letter in self.__dict_secret_word and index not in self.__dict_secret_word[letter]:
                feedback.append(1)
            else:
                feedback.append(0)
        return feedback
