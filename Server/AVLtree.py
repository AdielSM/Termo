from random import randint
from typing import List, Optional

class Node:
    def __init__(self, key: str):
        self.key: str = key
        self.height: int = 1
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

class AVLtree:
    
    """
    Uma classe que representa uma estrutura de dados de árvore AVL.

    Atributos:
        __root (Optional[Node]): O nó raiz da árvore AVL.
        __list (List[str]): Uma lista para armazenar os elementos da árvore AVL.

    Métodos:
        insert(root: Optional[Node], key: str) -> Node: Insere uma nova chave na árvore AVL.
        pre_order(): Imprime os elementos da árvore AVL em uma travessia pré-ordem.
        in_order(): Imprime os elementos da árvore AVL em uma travessia em ordem.
        post_order(): Imprime os elementos da árvore AVL em uma travessia pós-ordem.
        is_present(key: str) -> bool: Verifica se uma determinada chave está presente na árvore AVL.
        search(key: str) -> Optional[Node]: Procura por uma determinada chave na árvore AVL e retorna o nó correspondente.
        add_elements(lst: List[str]) -> None: Adiciona uma lista de elementos à árvore AVL.
        turn_list() -> List[str]: Retorna uma lista de todos os elementos na árvore AVL.
        get_random() -> str: Retorna um elemento aleatório da árvore AVL.
    """
    
    def __init__(self):
        self.__root: Optional[Node] = None
        self.__list: List[str] = []
    
    def __len__(self) -> int:
        return len(self.__list)
    
    def __get_height(self, node: Optional[Node]) -> int:
        if not node:
            return 0
        return node.height

    def __get_balance(self, node: Optional[Node]) -> int:
        if not node:
            return 0
        return self.__get_height(node.left) - self.__get_height(node.right)

    def right_rotate(self, y: Node) -> Node:
        x: Node = y.left
        T2: Optional[Node] = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(self.__get_height(y.left), self.__get_height(y.right))
        x.height = 1 + max(self.__get_height(x.left), self.__get_height(x.right))

        return x

    def left_rotate(self, x: Node) -> Node:
        y: Node = x.right
        T2: Optional[Node] = y.left

        y.left = x
        x.right = T2

        x.height = 1 + max(self.__get_height(x.left), self.__get_height(x.right))
        y.height = 1 + max(self.__get_height(y.left), self.__get_height(y.right))

        return y

    def insert(self, root: Optional[Node], key: str) -> Node:
        if not root:
            self.__list.append(key)
            return Node(key)
        
        if key < root.key:
            root.left = self.insert(root.left, key)
        elif key > root.key:
            root.right = self.insert(root.right, key)
        else:
            return root  # Ignora chaves duplicadas

        root.height = 1 + max(self.__get_height(root.left), self.__get_height(root.right))

        balance = self.__get_balance(root)

        # Casos de rotação
        if balance > 1:
            if key < root.left.key:
                return self.right_rotate(root)
            else:
                root.left = self.left_rotate(root.left)
                return self.right_rotate(root)

        if balance < -1:
            if key > root.right.key:
                return self.left_rotate(root)
            else:
                root.right = self.right_rotate(root.right)
                return self.left_rotate(root)

        return root
    

    def pre_order(self) -> None:
        self.__pre_order(self.__root)

    def __pre_order(self, root: Optional[Node]) -> None:
        if root:
            print(f'{root.key} ', end="")
            self.__pre_order(root.left)
            self.__pre_order(root.right)
            
            
    def in_order(self) -> None:
        self.__in_order(self.__root)
    
    def __in_order(self, root: Optional[Node]) -> None:
        if root:
            self.__in_order(root.left)
            print(f'{root.key} ',end="")
            self.__in_order(root.right)
            
            
    def post_order(self) -> None:
        self.__post_order(self.__root)        
    
    def __post_order(self, root: Optional[Node]) -> None:
        if root:
            self.__post_order(root.left)
            self.__post_order(root.right)
            print(f'{root.key} ',end="")
            

    def is_present(self, key: str) -> bool:
        return self.__search(self.__root, key) is not None

    def search(self, key: str) -> Optional[Node]:
        return self.__search(self.__root, key)
    
    def __search(self, root: Node, key: str) -> Optional[Node]:
        if not root or root.key == key:
            return root

        if key < root.key:
            return self.__search(root.left, key)
        return self.__search(root.right, key)
        
    def add_elements(self, lst: List[str]) -> None:
        for _, item in enumerate(lst):
            self.__root = self.insert(self.__root, item)

    def turn_list(self) -> List[str]:
        return self.__list

    def get_random(self) -> str:
        return self.__list[randint(0, len(self.__list)-1)]
