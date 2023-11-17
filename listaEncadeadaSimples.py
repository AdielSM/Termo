class ListaException(Exception):
    """Classe de exceção lançada quando uma violação de ordem genérica
        da lista é identificada.
    """

    def __init__(self,msg):
        """ Construtor padrão da classe, que recebe uma mensagem que se deseja
            embutir na exceção
        """
        super().__init__(msg)



class Node:
    '''
    Classe de objetos para um nó dinâmico na memória
    '''
    def __init__(self,data):
        self.__data = data
        self.__next = None
    
    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self, newData):
        self.__data = newData

    @property
    def next(self):
        return self.__next
    
    @next.setter
    def next(self, newNext):
        self.__next = newNext

    def hasNext(self):
        return self.__next != None
    
    def __str__(self):
        return str(self.__data)


'''
Esta classe implementa uma estrutura Lista Simplesmente Encadeada
'''
class Lista:
    # constructor initializes an empty linkd list
    def __init__(self):
        self.__head = None
        self.__tamanho = 0

    def estaVazia(self):
        return self.__tamanho == 0 

    def __len__(self):
        return self.__tamanho

    def elemento(self, posicao:int)->any:
        try:
            assert not self.estaVazia(), 'Lista vazia'
            assert posicao > 0 and posicao <= len(self), f'Posicao invalida. Lista contém {self.__tamanho} elementos'

            cursor = self.__head
            contador = 1
            while( cursor != None  and contador < posicao):
                cursor = cursor.next
                contador += 1

            return cursor.data

        except AssertionError as ae:
            raise ListaException(ae)



    def modificar(self, posicao:int, carga: any):

        try:
            assert posicao > 0, f'A posicao não pode ser 0 (zero) ou um número negativo'
            assert posicao <= len(self), f'Posicao invalida. Lista contém {self.__tamanho} elementos'
            assert not self.estaVazia(), 'Lista vazia'

            cursor = self.__head
            contador = 1
            while( cursor != None and contador < posicao ):
                cursor = cursor.next
                contador += 1

            cursor.data = carga
        except TypeError:
            raise ListaException(f'A posição deve ser um número do tipo inteiro')            
        except AssertionError as ae:
            raise ListaException(ae.__str__())

    
    def busca(self, chave:any)->int:
        if (self.estaVazia()):
            raise ListaException(f'Lista vazia')

        cursor = self.__head
        contador = 1

        while( cursor != None ):
            if( cursor.data == chave):
                return contador
            cursor = cursor.next
            contador += 1
            
        raise ListaException(f'O valor {valor} não está armazenado na lista')

    def inserir(self, posicao:int, carga:any ):
        try:
            assert posicao > 0 and posicao <= len(self)+1, f'Posicao invalida. Lista contém {self.__tamanho} elementos' 

            # CONDICAO 1: insercao se a lista estiver vazia
            if (self.estaVazia()):
                if ( posicao != 1):
                    raise ListaException(f'A lista esta vazia. A posicao correta para insercao é 1.')

                self.__head = Node(carga)
                self.__tamanho += 1
                return
            
            # CONDICAO 2: insercao na primeira posicao em uma lista nao vazia
            if ( posicao == 1):
                novo = Node(carga)
                novo.next = self.__head
                self.__head = novo
                self.__tamanho += 1
                return

            # CONDICAO 3: insercao apos a primeira posicao em lista nao vazia
            cursor = self.__head
            contador = 1
            while ( contador < posicao-1):
                cursor = cursor.next
                contador += 1

            novo = Node(carga)
            novo.next = cursor.next
            cursor.next = novo
            self.__tamanho += 1

        except TypeError:
            raise ListaException(f'A posição deve ser um número inteiro')            
        except AssertionError:
            raise ListaException(f'A posicao não pode ser um número negativo ou 0 (zero)')



    def remover(self, posicao:int)->any:
        try:
            if( self.estaVazia() ):
                raise ListaException(f'Não é possível remover de uma lista vazia')
            
            assert posicao > 0 and posicao <= len(self), f'Posicao invalida. Lista contém {self.__tamanho} elementos'

            cursor = self.__head
            contador = 1

            while( contador <= posicao-1 ) :
                anterior = cursor
                cursor = cursor.next
                contador+=1

            data = cursor.data

            if( posicao == 1):
                self.__head = cursor.next
            else:
                anterior.next = cursor.next

            self.__tamanho -= 1
            return data
        
        except TypeError:
            raise ListaException(f'A posição deve ser um número inteiro')            
        except AssertionError:
            raise ListaException(f'A posicao não pode ser um número negativo')


    def __str__(self):

        str = 'Lista: [ '
        if self.estaVazia():
            str+= ']'
            return str

        cursor = self.__head

        while( cursor != None ):
            str += f'{cursor.data}, '
            cursor = cursor.next

        str = str[:-2] + " ]"
        return str