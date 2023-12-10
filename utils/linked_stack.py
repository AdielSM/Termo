class StackException(Exception):
    """Classe de exceção lançada quando é identificada uma violação de acesso aos elementos da pilha."""
    def __init__(self, msg):
        """Construtor padrão da classe, que recebe uma mensagem para ser incorporada na exceção."""
        super().__init__(msg)


class Node:
    def __init__(self, data: any):
        self.__data = data
        self.__next = None

    @property
    def data(self) -> any:
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

    @property
    def next(self) -> 'Node':
        return self.__next

    @next.setter
    def next(self, next: 'Node'):
        self.__next = next

    def has_next(self) -> 'Node':
        return self.__next is not None

    def __str__(self):
        return str(self.__data)


class LinkedStack:
    """
    Classe que implementa a estrutura de dados "Pilha" usando a técnica de lista encadeada simples.

    Atributos:
        head (Node): ponteiro para o nó do topo da pilha
        size (int): número de elementos na pilha
    """

    def __init__(self):
        """Construtor padrão da classe Pilha sem argumentos.
        Ao instanciar um objeto do tipo Pilha, ele começará sem elementos.
        """
        self.__head = None
        self.__size = 0

    def is_empty(self) -> bool:
        """Método que verifica se a pilha está vazia.

        Returns:
            bool: True se a pilha estiver vazia, False caso contrário
        """
        return self.__head is None

    def __len__(self) -> int:
        """Método para obter o número de elementos na pilha.

        Returns:
            int: um número inteiro representando o número de elementos na pilha
        """
        return self.__size

    def element(self, position: int) -> any:
        """Método que recupera o valor armazenado em um elemento específico da pilha.

        Args:
            position (int): o elemento para obter o valor.
            A ordem dos elementos é da base para o topo da pilha.

        Returns:
            any: o valor armazenado na posição especificada.

        Raises:
            StackException: Exceção lançada quando uma posição inválida é fornecida pelo usuário.
                Posições inválidas se referem a:
                (a) números negativos
                (b) zero
                (c) número natural correspondente a um elemento que excede o número de elementos na pilha.
        """
        try:
            assert not self.is_empty(), 'A pilha está vazia'
            assert position > 0 and position <= len(self), f'A posição {position} não é válida para uma pilha de tamanho {self.__size}'

            cursor = self.__head
            counter = 1
            steps = len(self) - position
            while cursor is not None and counter <= steps:
                counter += 1
                cursor = cursor.next

            return cursor.data

        except TypeError:
            raise StackException('Digite um número inteiro referente ao elemento desejado')
        except AssertionError as ae:
            raise StackException(ae.__str__())
        except:
            raise

    def search(self, key: any) -> int:
        """Método que recupera a posição ordenada, dentro da pilha, onde a
            chave passada como argumento está localizada. Caso haja mais
            de uma ocorrência da chave, apenas a primeira ocorrência será Returnsda.

        Args:
            key: um item de dados para procurar na pilha

        Returns:
            int: um número inteiro representando a posição, na pilha, onde a "chave" foi encontrada.
                A posição é contada a partir da base da pilha, em direção ao topo

        Raises:
            StackException: Exceção lançada quando a chave não está presente na pilha.
        """
        cursor = self.__head
        counter = 1

        while cursor is not None:
            if cursor.data == key:
                return (len(self) - counter) + 1
            cursor = cursor.next
            counter += 1

        return None

    def top(self) -> any:
        """Método que Returns o elemento localizado no topo, sem removê-lo.

        Returns:
            any: o conteúdo correspondente ao elemento do topo

        Raises:
            StackException: Exceção lançada ao tentar acessar o topo de uma pilha vazia
        """
        if not self.is_empty():
            return self.__head.data
        raise StackException('A pilha está vazia')

    def stack_up(self, value: any):
        """Método que adiciona um novo elemento ao topo da pilha.

        Args:
            value (any): o conteúdo a ser inserido no topo da pilha.
        """
        new_node = Node(value)
        new_node.next = self.__head
        self.__head = new_node
        self.__size += 1

    def unstack(self) -> any:
        """Método que remove um elemento do topo da pilha e Returns
            o conteúdo correspondente desse elemento removido.

        Returns:
            any: o conteúdo removido do topo da pilha

        Raises:
            StackException: Exceção lançada ao tentar remover de uma pilha vazia
        """
        if not self.is_empty():
            data = self.__head.data
            self.__head = self.__head.next
            self.__size -= 1
            return data
        raise StackException('A pilha está vazia')

    def __str__(self):
        """Método que Returns uma string contendo os elementos da pilha
            separados por vírgulas e envolvidos em colchetes. A ordem de exibição é
            da base para o topo da pilha.
        """
        cursor = self.__head
        first = True
        s = ''
        while cursor is not None:
            if first:
                s += f'{cursor.data}'
                first = False
            else:
                s += f', {cursor.data}'
            cursor = cursor.next
        return s

    def clear(self):
        """
        Método que limpa a pilha encadeada, removendo a cabeça e redefinindo o tamanho
        """
        self.__head = None
        self.__size = 0
