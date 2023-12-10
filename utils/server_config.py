def server_config():
    """
    Retorna as configurações do servidor.

    Retorna uma tupla contendo o tamanho máximo da mensagem (tam_msg) e a porta (port) 
    lidos do arquivo de configuração do servidor.

    Caso ocorra algum erro ao ler o arquivo de configuração, retorna os valores padrão 
    de tamanho máximo da mensagem (1024) e porta (40000).

    Returns:
        tuple: Uma tupla contendo o tamanho máximo da mensagem e a porta.
    """
    try:
        with open('./utils/server_config.txt', 'r', encoding='utf-8') as arquivo:
            tam_msg = int(arquivo.readline().split('=')[1]) or 1024
            port = int(arquivo.readline().split('=')[1]) or 40000
        return (tam_msg, port)
    except FileNotFoundError:
        return (1024, 40000)
