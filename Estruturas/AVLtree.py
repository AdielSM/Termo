from random import randint
from typing import List, Optional

class Node:
    def __init__(self, key: int):
        self.key: int = key
        self.height: int = 1
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

class AVLTree:
    def __init__(self):
        self.root: Optional[Node] = None
    
    
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

    def insert(self, root: Optional[Node], key: int) -> Node:
        if not root:
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
        self.__preOrder(self.root)

    def __preOrder(self, root: Optional[Node]) -> None:
        if root:
            print(f'{root.key} ', end="")
            self.__preOrder(root.left)
            self.__preOrder(root.right)
            
            
    def inOrder(self) -> None:
        self.__inOrder(self.root)
    
    def __inOrder(self, root: Optional[Node]) -> None:
        if root:
            self.__inOrder(root.left)
            print(f'{root.key} ',end="")
            self.__inOrder(root.right)
            
            
    def postOrder(self) -> None:
        self.__postOrder(self.root)        
    
    def __postOrder(self, root: Optional[Node]) -> None:
        if root:
            self.__postOrder(root.left)
            self.__postOrder(root.right)
            print(f'{root.key} ',end="")
            

    def is_present(self, key: int) -> bool:
        return self.search(self.root, key) is not None

    def search(self, root: Optional[Node], key: int) -> Optional[Node]:
        if not root or root.key == key:
            return root
        
        if key < root.key:
            return self.search(root.left, key)
        else:
            return self.search(root.right, key)
        
    def add_elements(self, lst: List[int]) -> None:
        for _, item in enumerate(lst):
            self.root = self.insert(self.root, item)

    def turn_list(self) -> List[int]:
        self.lst = []
        self.__turn_list(self.root)
        return self.lst

    def __turn_list(self, root: Optional[Node]) -> None:
        if root:
            self.__turn_list(root.left)
            self.lst.append(root.key)
            self.__turn_list(root.right)
            
    def get_random(self) -> int:
        self.lst = []
        self.turn_list()
        return self.lst[randint(0, len(self.lst)-1)]
    

if __name__ == '__main__':
    tree = AVLTree()
    lst = [1,2,3,4,5,6,7,8,9]
    tree.add_elements(lst)
    tree.inOrder()
    print(tree.turn_list())
