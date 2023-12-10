def summary_protocol():
    """
    Lê o arquivo 'sumario_protocolo.txt' e retorna um dicionário com as chaves e 
    valores encontrados.

    Returns:
        dict: Um dicionário contendo as chaves e valores do arquivo 'sumario_protocolo.txt'.
    """

    try:
        with open('./utils/summary_protocol.txt', 'r', encoding='utf-8') as file:
            sumario = {}

            for linha in file.readlines():
                key = linha.split(' = ')[0].strip().replace('\x00', '')
                value = int(linha.split(' = ')[1].strip().replace('\x00', ''))
                sumario[key] = value

            return sumario

    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return None
