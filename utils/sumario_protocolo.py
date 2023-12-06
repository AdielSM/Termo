def sumario_protocolo():
    """
    Lê o arquivo 'sumario_protocolo.txt' e retorna um dicionário com as chaves e valores encontrados.

    Returns:
        dict: Um dicionário contendo as chaves e valores do arquivo 'sumario_protocolo.txt'.
    """
    try:
        with open('./utils/sumario_protocolo.txt', 'r') as arquivo:
            sumario = {}
            
            for linha in arquivo.readlines():
                key = linha.split(' = ')[0].strip().replace('\x00', '')
                value = int(linha.split(' = ')[1].strip().replace('\x00', ''))
                sumario[key] = value
                
            return sumario
    
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
                