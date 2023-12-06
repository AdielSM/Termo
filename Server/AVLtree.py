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
        preOrder(): Imprime os elementos da árvore AVL em uma travessia pré-ordem.
        inOrder(): Imprime os elementos da árvore AVL em uma travessia em ordem.
        postOrder(): Imprime os elementos da árvore AVL em uma travessia pós-ordem.
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
    
    def __getHeight(self, node: Optional[Node]) -> int:
        if not node:
            return 0
        return node.height

    def __getBalance(self, node: Optional[Node]) -> int:
        if not node:
            return 0
        return self.__getHeight(node.left) - self.__getHeight(node.right)

    def rightRotate(self, y: Node) -> Node:
        x: Node = y.left
        T2: Optional[Node] = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(self.__getHeight(y.left), self.__getHeight(y.right))
        x.height = 1 + max(self.__getHeight(x.left), self.__getHeight(x.right))

        return x

    def leftRotate(self, x: Node) -> Node:
        y: Node = x.right
        T2: Optional[Node] = y.left

        y.left = x
        x.right = T2

        x.height = 1 + max(self.__getHeight(x.left), self.__getHeight(x.right))
        y.height = 1 + max(self.__getHeight(y.left), self.__getHeight(y.right))

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

        root.height = 1 + max(self.__getHeight(root.left), self.__getHeight(root.right))

        balance = self.__getBalance(root)

        # Casos de rotação
        if balance > 1:
            if key < root.left.key:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)

        if balance < -1:
            if key > root.right.key:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)

        return root
    

    def preOrder(self) -> None:
        self.__preOrder(self.__root)

    def __preOrder(self, root: Optional[Node]) -> None:
        if root:
            print(f'{root.key} ', end="")
            self.__preOrder(root.left)
            self.__preOrder(root.right)
            
            
    def inOrder(self) -> None:
        self.__inOrder(self.__root)
    
    def __inOrder(self, root: Optional[Node]) -> None:
        if root:
            self.__inOrder(root.left)
            print(f'{root.key} ',end="")
            self.__inOrder(root.right)
            
            
    def postOrder(self) -> None:
        self.__postOrder(self.__root)        
    
    def __postOrder(self, root: Optional[Node]) -> None:
        if root:
            self.__postOrder(root.left)
            self.__postOrder(root.right)
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
    

