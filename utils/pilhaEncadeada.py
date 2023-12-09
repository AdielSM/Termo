class PilhaException(Exception):
    """Classe de exceção lançada quando uma violação de acesso aos elementos
       da pilha é identificada.
    """
    def __init__(self,msg):
        """ Construtor padrão da classe, que recebe uma mensagem que se deseja
            embutir na exceção
        """
        super().__init__(msg)


class Node:
    def __init__(self, dado:any):
        self.__dado = dado
        self.__prox = None

    @property
    def dado(self)->any:
        return self.__dado
    
    @dado.setter
    def dado(self, dado):
        self.__dado = dado

    @property
    def prox(self)->'Node':
        return self.__prox
    
    @prox.setter
    def prox(self, prox:'Node'):
        self.__prox = prox

    def temProximo(self)->'Node':
        return self.__prox != None
    
    def __str__(self):
        return str(self.__dado)


class PilhaEncadeada:
    """
    Classe que implementa a estrutura de dados "Pilha" utilizando a técnica
    simplesmente encadeada.

     Attributes:
        head (Node): apontador para o nó topo da pilha
        tamanho (int): quantidade de elementos existentes na pilha
    """

    def __init__(self):
        """ Construtor padrão da classe Pilha sem argumentos. 
            Ao instanciar um objeto do tipo Pilha, esta iniciará 
            sem elementos. 
        """
        self.__head = None
        self.__tamanho = 0        

    def estaVazia(self)->bool:
        """ Método que verifica se a pilha está vazia.

        Returns:
            boolean: True se a pilha estiver vazia, False caso contrário

        Examples:
            p = Pilha()
            # considere que temos internamente na pilha  topo->[10,20,30,40]
            if(p.estaVazia()): #
               # instrucoes
        """
        return self.__head == None

    def __len__(self)->int:
        """ Método para obter a quantidade de elementos existentes na pilha

        Returns:
            int: um número inteiro que determina o número de elementos existentes na pilha

        Examples:
            p = Pilha()
            # considere que temos internamente a pilha topo->[10,20,30,40]
            print (p.tamanho()) # exibe 4
        """        

        return self.__tamanho

    def elemento(self, posicao:int)->any:
        """ Método que recupera o valor armazenado em um determinado elemento da pilha

        Argumentos:
            posicao (int): o elemento que deseja obter a carga.
            A ordem dos elementos é na direção da base até o topo da pilha.
        
        Returns:
            any: a carga armazenada na ordem indicada por posição.

        Raises:
            PilhaException: Exceção lançada quando uma posição inválida é
                  fornecida pelo usuário. São inválidas posições que se referem a:
                  (a) números negativos
                  (b) zero
                  (c) número natural correspondente a um elemento que excede a
                      quantidade de elementos existentes na pilha.                      
        Examples:
            p = Pilha()
            # considere que temos internamente a pilha topo->[10,20,30,40]
            print (p.elemento(3)) # exibe 30
        """
        try:
            assert not self.estaVazia(), 'A pilha está vazia'
            assert posicao > 0 and posicao <= len(self),f'A posicao {posicao} NAO é válida para a pilha de tamanho {self.__tamanho}'
 
            cursor = self.__head
            contador = 1
            steps = len(self) - posicao
            while(cursor != None and contador <= steps ):
                contador += 1
                cursor = cursor.prox

            return cursor.dado
                
        except TypeError:
            raise PilhaException('Digite um número inteiro referente ao elemento desejado')
        except AssertionError as ae:
            raise PilhaException(ae.__str__(),'elemento()')
        except:
            raise

    def busca(self, chave:any)->int:
        """ Método que recupera a posicao ordenada, dentro da pilha, em que se
            encontra a chave passada como argumento. No caso de haver mais 
            de uma da chave, será retornada apenas a primeira ocorrência.

        Argumentos:
            chave: um item de dado que deseja procurar na pilha
        
        Returns:
            int: um número inteiro representando a posição, na pilha, em que foi
                 encontrada a  "chave". A posição é contada a partir da base da
                 pilha, em direção ao topo

        Raises:
            PilhaException: Exceção lançada quando a chave não 
                  estiver presente na pilha.

        Examples:
            p = Pilha()
            # considere que temos internamente na pilha  topo-> [10,20,30,40]
            print (p.elemento(40)) # exibe 4
        """

        cursor = self.__head
        contador = 1

        while( cursor != None):
            if cursor.dado == chave:
                return (len(self) - contador)+1
            cursor = cursor.prox
            contador += 1

        return None
        
    def topo(self)->any:
        """ Método que devolve o elemento localizado no topo, sem desempilhá-lo
    
        Returns:
            any: o conteúdo referente ao elemento do topo

        Raises:
            PilhaException: Exceção lançada quando se tenta consultar o topo de uma
                   uma pilha vazia
                    
        Examples:
            p = Pilha()
            ...   # considere que temos internamente a lista [10,20,30,40]
            dado = p.topo()
            print(dado) # exibe 40
        """
        if not self.estaVazia():
            return self.__head.dado
        raise PilhaException('A pilha está vazia')
    

    def empilha(self, carga:any):
        """ Método que adiciona um novo elemento ao topo da pilha

        Argumentoss:
            carga(any): o conteúdo a ser inserido no topo da pilha.

        Examples:
            p = Pilha()
            # considere a pilha  topo->[10,20,30,40]
            p.empilha(50)
            print(p)  # exibe [10,20,30,40,50]
        """
        novo = Node(carga)
        novo.prox = self.__head
        self.__head = novo
        self.__tamanho += 1


    def desempilha(self)->any:
        """ Método que remove um elemento do topo da pilha e devolve 
            a carga correspondente a esse elemento removido.
    
        Returns:
            any: a carga removida do topo da pilha

        Raises:
            PilhaException: Exceção lançada quando se tenta remover de uma pilha vazia
                    
        Examples:
            p = Pilha()
            # considere que temos internamente a pilha [10,20,30,40]<-topo
            dado = p.desemplha()
            print(p) # exibe [10,20,30]
            print(dado) # exibe 40
        """
        if not self.estaVazia():
            dado = self.__head.dado
            self.__head = self.__head.prox
            self.__tamanho -= 1
            return dado
        raise PilhaException('A pilha está vazia')
   
    
    def __str__(self):
        """ Método que devolve uma string contendo os elementos da pilha
            separados por vírgula e entre colchetes. A ordem de exibição é
            da base para o topo da pilha.   
        """
        cursor = self.__head
        primeiro = True
        s = ''
        while( cursor != None):
            if primeiro:
                s += f'{cursor.dado}'
                primeiro = False
            else:
                s += f', {cursor.dado}'
            cursor = cursor.prox
        return s
    
    def clear(self):
        """
        Método que limpa a pilha encadeada, removendo o head e reiniciando o tamanho  
        """
        self.__head = None
        self.__tamanho = 0