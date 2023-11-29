def buscar_chave_por_valor(dicionario, valor):
    for chave, valor_item in dicionario.items():
        if valor_item == valor:
            return chave