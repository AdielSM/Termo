def config_server():
    try: 
        with open('./utils/server.config', 'r') as arquivo:
            TAM_MSG = int(arquivo.readline().split('=')[1]) or 1024
            PORT = int(arquivo.readline().split('=')[1]) or 40000
            SEPARADOR = f'{arquivo.readline().split("=")[1]}' or '\n'
        return (TAM_MSG, PORT, SEPARADOR)
    except:
        return (1024, 40000, '\n')