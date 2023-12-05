def format_output(word,array):
    if word and array:    
        saida = ''
        for index,itens in enumerate(array):
            if itens == 2:
                saida += "\033[92m" + word[index] + "\033[0m"
            elif itens == 1:
                saida += "\033[93m" + word[index] + "\033[0m"
            else:
                saida += "\033[90m" + word[index] + "\033[0m"
                
        return saida
    else:
        return