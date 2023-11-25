import socket
from threading import Thread, Lock

from termo import Termo
from Estruturas.listaEncadeadaSimples import Lista

from utils.server_config import config_server

from Enum.Resposta_CHECK_WORD import Resposta_CHECK_WORD

HOST = '0.0.0.0' # IP do Servidor
TAM_MSG, PORT, SEPARADOR = config_server()
SEPARADOR = '\n' # Corrigir erro do separador

jogadoresAtivos = Lista()
jogadoresAtivos_lock = Lock()

# Por que o inglês do nada? kkkkk
def handle_client(con, cliente):
    jogo = Termo()

    while True:
        msg = con.recv(TAM_MSG)
        if not msg: break
        processa_msg_cliente(msg, con, cliente, jogo)
    con.close()
    
    
def processa_msg_cliente(msg, con, cliente, jogo:Termo):
    msg = msg.decode().split()
    comando, parametro = msg[0], msg[1:]
    
    if comando.upper() == 'GET_GAME':
        jogo.iniciarJogo()
        con.send(str.encode(f'+START{SEPARADOR}Jogo Iniciado!'))
    
            
    # Encerra a conexão com o servidor
    elif comando.upper() == 'EXIT_GAME':
        con.send(str.encode(f'-EXIT{SEPARADOR}Serviço Encerrado!'))
        return False 
    
    # Verifica a situação da palavra enviada pelo player
    elif comando.upper() == 'CHECK_WORD':
        estado = jogo.checkPalavra(parametro[0])

        try:
            estadoModificado = estado.upper().replace(' ', '_')
            resposta = SEPARADOR.join([
                Resposta_CHECK_WORD[estadoModificado].value['status'],
                Resposta_CHECK_WORD[estadoModificado].value['msg_status'],
                str(jogo.qtdTentativasRestantes)
            ])
        except KeyError: #Devolveu a palavra colorida
            resposta = SEPARADOR.join([
                '-ERROU',
                estado,
                str(jogo.qtdTentativasRestantes)
            ])
        finally:
            print(resposta)
            con.send(str.encode(resposta))
        
        return True
        
    # Lista os jogadores ativos
    elif comando.upper() == 'LIST_PLAYERS':
        pass
    
    # Adiciona um jogador à lista de jogadores ativos, poderia ser um comando alternativo para o GetGame ?
    elif comando.upper() == 'ADD_PLAYER':
        with jogadoresAtivos_lock:
            jogador = (cliente[0], cliente[1])
            jogadoresAtivos.append(jogador)
        con.send(str.encode(f'+OK{SEPARADOR}'))
    
    # Remove um jogador da lista de jogadores ativos forçadamente
    elif comando.upper() == 'REMOVE_PLAYER':
        pass
        
    # Lista as partidas em andamento
    elif comando.upper() == 'LIST_GAMES':
        pass
    
    # Lista as palavras que estão sendo usadas no momento e em qual partida
    elif comando.upper() == 'LIST_WORDS':
        pass
        
    # daria para fazer um jogador jogador novamente, e caso o jogador continuasse, armazenasse a quantidade de palavras que ele acertou naquela sessão?
    elif comando.upper() == 'LIST_SCORE':
        pass
    
    elif comando.upper() == 'ADD_SCORE':
        pass
    
    else:
        con.send(str.encode(f'-ERR{SEPARADOR}Comando inválido'))
        return False
    
    return True

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(10)

while True:
    try:
        con, cliente = sock.accept()
    except: break
    # processa_cliente(con, cliente)
    t = Thread(target=handle_client, args=(con, cliente))
    t.start()
sock.close()