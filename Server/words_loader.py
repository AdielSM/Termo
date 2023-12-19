WORD_BANK_URL = 'words_bank/bd.txt'

def load_words() -> list:
    """
    Carrega as palavras do arquivo e retorna uma lista de palavras.

    Args:
        None

    Returns:
        list: Uma lista de palavras carregadas do arquivo.
    """
    with open(WORD_BANK_URL, "r", encoding="utf-8") as file:
        words = [word.strip().replace('\x00', '') for word in file.readlines()]
        return words