def format_output(word, array):
    """
    Formata a palavra baseado na lista de codificação passada.

    Args:
        word (str): A palavra a ser formatada.
        array (list): A lista que contém as instruções da formatação.

    Returns:
        str: a string formatada.
    """
    if word and array:    
        saida = ''
        for index, itens in enumerate(array):
            if itens == 2:
                saida += "\033[92m" + word[index] + "\033[0m"
            elif itens == 1:
                saida += "\033[93m" + word[index] + "\033[0m"
            else:
                saida += "\033[90m" + word[index] + "\033[0m"
                
        return saida
    else:
        return