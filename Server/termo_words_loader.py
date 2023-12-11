TERMO_WORD_BANK_URL = 'words_bank/bd_termo.txt'

def load_termo_words() -> list:
    """
    Carrega as palavras do arquivo e retorna uma lista de palavras.

    Returns:
        list: Uma lista de palavras carregadas do arquivo.
    """
    with open(TERMO_WORD_BANK_URL, "r", encoding="utf-8") as file:
        words = [word.strip().replace('\x00', '') for word in file.readlines()]
        return words