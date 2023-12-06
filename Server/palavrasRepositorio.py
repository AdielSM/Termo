URL_BANCO_PALAVRAS = 'bancoDePalavras/bd.txt'
URL_BANCO_PALAVRAS_TERMO = 'bancoDePalavras/bdTermo.txt'

def carregarPalavras() -> list:
    """
    Carrega as palavras do arquivo e retorna uma lista de palavras.

    Returns:
        list: Uma lista de palavras carregadas do arquivo.
    """
    with open(URL_BANCO_PALAVRAS, 'r') as arquivo:
        palavras = [palavra.strip().replace('\x00', '') for palavra in arquivo.readlines()]
        return palavras

def carregarPalavrasTermo() -> list:
    """
    Carrega as palavras do arquivo e retorna uma lista de palavras.

    Returns:
        list: Uma lista de palavras carregadas do arquivo.
    """
    with open(URL_BANCO_PALAVRAS_TERMO, 'r') as arquivo:
        palavras = [palavra.strip().replace('\x00', '') for palavra in arquivo.readlines()]
        return palavras