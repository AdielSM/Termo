from random import randint

class Node:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None

class AVLTree:
    def __init__(self):
        self.root = None
    
    
    def getHeight(self, node):
        if not node:
            return 0
        return node.height

    def getBalance(self, node):
        if not node:
            return 0
        return self.getHeight(node.left) - self.getHeight(node.right)

    def rightRotate(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        x.height = 1 + max(self.getHeight(x.left), self.getHeight(x.right))

        return x

    def leftRotate(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        x.height = 1 + max(self.getHeight(x.left), self.getHeight(x.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))

        return y

    def insert(self, root, key):
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

    def preOrder(self, root):
        if root:
            print("{0} ".format(root.key), end="")
            self.preOrder(root.left)
            self.preOrder(root.right)
            

    
    def inOrder(self, root):
        if root:
            self.inOrder(root.left)
            print("{0} ".format(root.key), end="")
            self.inOrder(root.right)
        

    def is_present(self, key):
        return self.search(self.root, key) is not None

    def search(self, root, key):
        if not root or root.key == key:
            return root
        
        if key < root.key:
            return self.search(root.left, key)
        else:
            return self.search(root.right, key)
        
    def add_elements(self, lista):
        for _,item in enumerate(lista):
            self.root = self.insert(self.root, item)

    def get_random(self):
        return self.__get_random(self.root)

    def __get_random(self, root):
        # -1 = left, 0 = get, 1 = right
        random_choice = randint(-1, 1)

        if random_choice == 0:
            return root.key
        elif random_choice == -1 and root.left is not None:
            return self.__get_random(root.left)
        elif random_choice == 1 and root.right is not None:
            return self.__get_random(root.right)
            
        return root.key