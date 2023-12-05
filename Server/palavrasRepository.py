URL_BANCO_PALAVRAS = 'bancoDePalavras/bd.txt'

def carregarPalavras() -> list:
        with open(URL_BANCO_PALAVRAS, 'r') as arquivo:
            palavras = [palavra.strip().replace('\x00', '') for palavra in arquivo.readlines()]
            return palavras