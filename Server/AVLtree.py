from random import randint
from typing import List, Optional

class Node:    
    def __init__(self, key: any):
        self.key: any = key
        self.height: int = 1
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

class AVLtree:
    
    """
    Uma classe que representa uma estrutura de dados de árvore AVL.

    Métodos:
        insert(root: Optional[Node], key: any) -> Node: Insere uma nova chave na árvore AVL.
        pre_order(): Imprime os elementos da árvore AVL em uma travessia pré-ordem.
        in_order(): Imprime os elementos da árvore AVL em uma travessia em ordem.
        post_order(): Imprime os elementos da árvore AVL em uma travessia pós-ordem.
        is_present(key: any) -> bool: Verifica se uma determinada chave está presente na árvore AVL.
        search(key: any) -> Optional[Node]: Procura por uma determinada chave na árvore AVL e retorna o nó correspondente.
        add_elements(lst: List[any]) -> None: Adiciona uma lista de elementos à árvore AVL.
        turn_list() -> List[any]: Retorna uma lista de todos os elementos na árvore AVL.
        get_random() -> any: Retorna um elemento aleatório da árvore AVL.
    """
    def __init__(self):
        self.__root: Optional[Node] = None
        self.__list: List[any] = []


    def __len__(self) -> int:
        """
        Retorna o número de elementos na árvore AVL.

        Returns: 
            int: O número de elementos na árvore AVL.
        """
        return len(self.__list)


    def __get_height(self, node: Optional[Node]) -> int:
        """
        Retorna a altura do nó fornecido.

        Args:
            node (Node): O nó para o qual a altura será calculada.

        Returns:
            int: A altura do nó. Se o nó for None, retorna 0.
        """
        if not node:
            return 0
        return node.height


    def __get_balance(self, node: Optional[Node]) -> int:
        """
        Retorna o fator de balanceamento do nó.

        O fator de balanceamento é calculado subtraindo a altura da subárvore esquerda
        pela altura da subárvore direita.

        Args:
            node (Optional[Node]): O nó para o qual o fator de balanceamento será calculado.

        Returns:
            int: O fator de balanceamento do nó.
        """
        if not node:
            return 0
        return self.__get_height(node.left) - self.__get_height(node.right)


    def __right_rotate(self, y: Node) -> Node:
        """
        Realiza uma rotação para a direita na árvore AVL.

        Parâmetros:
        - y: O nó a ser rotacionado para a direita.

        Retorna:
        - O novo nó raiz após a rotação.

        """
        x: Node = y.left
        T2: Optional[Node] = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(self.__get_height(y.left), self.__get_height(y.right))
        x.height = 1 + max(self.__get_height(x.left), self.__get_height(x.right))

        return x


    def __left_rotate(self, x: Node) -> Node:
        """
        Realiza uma rotação para a esquerda em torno do nó x na árvore AVL.

        Args:
            x (Node): O nó em torno do qual a rotação será realizada.

        Returns:
            Node: O novo nó raiz após a rotação.
        """
        y: Node = x.right
        T2: Optional[Node] = y.left

        y.left = x
        x.right = T2

        x.height = 1 + max(self.__get_height(x.left), self.__get_height(x.right))
        y.height = 1 + max(self.__get_height(y.left), self.__get_height(y.right))

        return y


    def insert(self, key: any) -> None:
        """
        Insere uma nova chave na árvore AVL.

        Args:
            key (any): A chave a ser inserida.

        Returns:
            None
        """
        self.__root = self.__insert(self.__root, key)


    def __insert(self, root: Optional[Node], key: any) -> Node:
        """
        Insere um novo nó na árvore AVL.

        Args:
            root (Optional[Node]): O nó raiz da árvore.
            key (any): A chave do novo nó a ser inserido.

        Returns:
            Node: O nó raiz atualizado após a inserção.
        """
        if not root:
            self.__list.append(key)
            return Node(key)

        if key < root.key:
            root.left = self.__insert(root.left, key)
        elif key > root.key:
            root.right = self.__insert(root.right, key)
        else:
            return root  # Ignora chaves duplicadas

        root.height = 1 + max(self.__get_height(root.left), self.__get_height(root.right))

        balance = self.__get_balance(root)

        # Casos de rotação
        if balance > 1:
            if key < root.left.key:
                return self.__right_rotate(root)

            root.left = self.__left_rotate(root.left)
            return self.__right_rotate(root)

        if balance < -1:
            if key > root.right.key:
                return self.__left_rotate(root)

            root.right = self.__right_rotate(root.right)
            return self.__left_rotate(root)

        return root


    def pre_order(self) -> None:
        """
        Realiza uma travessia pré-ordem na árvore AVL.
        """
        self.__pre_order(self.__root)


    def __pre_order(self, root: Optional[Node]) -> None:
        """
        Realiza a travessia pré-ordem na árvore a partir do nó raiz especificado.

        Args:
            root (Node): O nó raiz a partir do qual a travessia pré-ordem será realizada.

        Returns:
            None
        """
        if root:
            print(f'{root.key} ', end="")
            self.__pre_order(root.left)
            self.__pre_order(root.right)


    def in_order(self) -> None:
        """
        Realiza uma travessia em ordem na árvore AVL.

        Returns:
            None
        """
        self.__in_order(self.__root)


    def __in_order(self, root: Optional[Node]) -> None:
        """
        Realiza uma travessia em ordem na árvore a partir do nó raiz fornecido.

        Args:
            root(Optional[Node]): O nó raiz da árvore.

        Returns:
            None
        """
        if root:
            self.__in_order(root.left)
            print(f'{root.key} ',end="")
            self.__in_order(root.right)


    def post_order(self) -> None:
        """
        Executa uma travessia pós-ordem na árvore AVL.

        """
        self.__post_order(self.__root)


    def __post_order(self, root: Optional[Node]) -> None:
        """
        Realiza a travessia pós-ordem na árvore a partir do nó raiz especificado.

        Args:
            root (Node): O nó raiz da árvore.

        Returns:
            None
        """
        if root:
            self.__post_order(root.left)
            self.__post_order(root.right)
            print(f'{root.key} ',end="")


    def is_present(self, key: any) -> bool:
        """
        Verifica se a chave está presente na árvore AVL.

        Args:
            key: A chave a ser verificada.

        Returns:
            True se a chave estiver presente na árvore, False caso contrário.
        """
        return self.__search(self.__root, key) is not None


    def search(self, key: any) -> Optional[Node]:
        """
        Procura por um nó com a chave especificada na árvore.

        Args:
            key: A chave a ser procurada.

        Returns:
            O nó com a chave especificada, se encontrado. Caso contrário, retorna None.
        """
        return self.__search(self.__root, key)


    def __search(self, root: Node, key: any) -> Optional[Node]:
        """
        Realiza uma busca na árvore AVL pelo nó com a chave especificada.

        Args:
            root (Node): O nó raiz da árvore.
            key (any): A chave a ser buscada.

        Returns:
            Optional[Node]: O nó encontrado com a chave especificada, ou None 
            se a chave não for encontrada.
        """
        if not root or root.key == key:
            return root

        if key < root.key:
            return self.__search(root.left, key)
        return self.__search(root.right, key)


    def add_elements(self, lst: List[any]) -> None:
        """
        Adiciona uma lista de elementos à árvore AVL.

        Args:
            lst (List[any]): Lista de elementos a serem adicionados.

        Returns:
            None
        """
        for _, item in enumerate(lst):
            self.__root = self.__insert(self.__root, item)


    def turn_list(self) -> List[any]:
        """
        Retorna a lista de elementos da árvore AVL.

        Returns:
            List[any]: A lista de elementos da árvore AVL.
        """
        return self.__list


    def get_random(self) -> any:
        """
        Retorna um elemento aleatório da lista.
        
        Returns:
            (any) Um elemento aleatório da árvore

        """
        return self.__list[randint(0, len(self.__list)-1)]
