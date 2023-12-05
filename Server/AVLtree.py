from random import randint
from typing import List, Optional

class Node:
    def __init__(self, key: str):
        self.key: str = key
        self.height: int = 1
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

class AVLtree:
    def __init__(self):
        self.__root: Optional[Node] = None
        self.__list: List[str] = []
    
    def __len__(self) -> int:
        return len(self.__list)
    
    def getHeight(self, node: Optional[Node]) -> int:
        if not node:
            return 0
        return node.height

    def getBalance(self, node: Optional[Node]) -> int:
        if not node:
            return 0
        return self.getHeight(node.left) - self.getHeight(node.right)

    def rightRotate(self, y: Node) -> Node:
        x: Node = y.left
        T2: Optional[Node] = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        x.height = 1 + max(self.getHeight(x.left), self.getHeight(x.right))

        return x

    def leftRotate(self, x: Node) -> Node:
        y: Node = x.right
        T2: Optional[Node] = y.left

        y.left = x
        x.right = T2

        x.height = 1 + max(self.getHeight(x.left), self.getHeight(x.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))

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

        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

        balance = self.getBalance(root)

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
        return self.search(self.__root, key) is not None

    def search(self, key: str) -> Optional[Node]:
        return self.search(self.__root, key)
    
    def __search(self, root: Node, key: str) -> Optional[Node]:
        if not root or root.key == key:
            return root

        if key < root.key:
            return self.search(root.left, key)
        return self.search(root.right, key)
        
    def add_elements(self, lst: List[str]) -> None:
        for _, item in enumerate(lst):
            self.__root = self.insert(self.__root, item)

    def turn_list(self) -> List[str]:
        return self.__list

    def get_random(self) -> str:
        return self.__list[randint(0, len(self.__list)-1)]
    

