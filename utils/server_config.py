def server_config():
    """
    Retorna as configurações do servidor.

    Retorna uma tupla contendo o tamanho máximo da mensagem (TAM_MSG) e a porta (PORT) 
    lidos do arquivo de configuração do servidor.

    Caso ocorra algum erro ao ler o arquivo de configuração, retorna os valores padrão 
    de tamanho máximo da mensagem (1024) e porta (40000).

    Returns:
        tuple: Uma tupla contendo o tamanho máximo da mensagem e a porta.
    """
    try: 
        with open('./utils/server.config', 'r') as arquivo:
            TAM_MSG = int(arquivo.readline().split('=')[1]) or 1024
            PORT = int(arquivo.readline().split('=')[1]) or 40000
        return (TAM_MSG, PORT)
    except:
        return (1024, 40000)