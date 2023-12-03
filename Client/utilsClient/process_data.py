def process_data(data, **kwargs) -> str:
    
    remaining_attemps = kwargs.get("remaining_attemps")
    if remaining_attemps:
        remaining_attemps = "Tentativas Restantes: " + str(remaining_attemps)
    else:
        remaining_attemps = ''
    
    match data:
        case 200:
            print("Jogo Iniciado com Sucesso")
            
        case 201:
            print("Jogo Encerrado com Sucesso")
            
        case 202:
            print("Palavra Correta!")
            print(remaining_attemps)
            
        case 203:
            print("Palavra Incorreta!")
            
            
            palavraCodificada = kwargs["word_encoded"]
            palavraUsuario = kwargs["word_user"]

            print('palavra codificado',palavraCodificada)
            print('palavra do usuario',palavraUsuario)
            
            saida = ''
            for index,itens in enumerate(palavraCodificada):
                if itens == 2:
                    saida += "\033[92m" + palavraUsuario[index] + "\033[0m"
                elif itens == 1:
                    saida += "\033[93m" + palavraUsuario[index] + "\033[0m"
                else:
                    saida += "\033[90m" + palavraUsuario[index] + "\033[0m"
            
            print(saida)
            print(remaining_attemps)
            print('')

            
            if kwargs["remaining_attemps"] == 0:
                print('''
                    
                    Você não conseguiu acertar a palavra!
                    Obrigado por jogar!
                    
                    ''')
        case 400:
            print("Jogo já iniciado")
            print(remaining_attemps)
            
        case 401:
            print("Jogo não iniciado")
            
            
        case 402:
            print("Necessário Forcener uma Palavra")
            print(remaining_attemps)

            
        case 403:
            print("A palavra deve conter 6 letras")
            print(remaining_attemps)

            
        case 404:
            print("Palavra inexiste no dicionário")
            print(remaining_attemps)

            
        case 405:
            print("Palavra já utilizada")
            print(remaining_attemps)
            
        case 499:
            print("Comando Inválido")
            print(remaining_attemps)
