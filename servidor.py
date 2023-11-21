import socket
from threading import Thread, Lock

from Termo import Termo
from Estruturas.listaEncadeadaSimples import Lista

from enum import Enum

class Estado(Enum):
    ACERTOU = 'acertou'
    PALAVRA_REPETIDA = 'Palavra repetida'
    TAMANHO_INCORRETO = 'Tamanho incorreto'
    PALAVRA_INEXISTENTE = 'Palavra inexistente'

TAM_MSG = 1024 # Tamanho do bloco de mensagem
HOST = '0.0.0.0' # IP do Servidor
PORT = 40000 # Porta que o Servidor escuta

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
        con.send(str.encode(f'+OK \n'))
        #logica do jogo
        
    
    # Encerra a conexão com o servidor
    elif comando.upper() == 'EXIT_GAME':
        con.send(str.encode('+OK\n'))
        return False 
    
    # Verifica a situação da palavra enviada pelo player
    elif comando.upper() == 'CHECK_WORD':
        estado = jogo.checkPalavra(parametro[0])
        
        
        erro_prefixo = '-ERROU,'
        estados_respostas = {
            Estado.ACERTOU : '+ACERTOU,' + jogo.palavra,
            Estado.PALAVRA_REPETIDA : '-ERROU,palavra_repetida',
            Estado.TAMANHO_INCORRETO : '-ERROU,tamanho_incorreto',
            Estado.PALAVRA_INEXISTENTE : '-ERROU,palavra_inexistente',
            estado: erro_prefixo + estado
        }
        
        resposta = estados_respostas.get(estado, '-ERROU,estado_desconhecido')
        resposta += f',{jogo.qtdTentativasRestantes}'
        
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
        con.send(str.encode('+OK\n'))
    
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
        con.send(str.encode('-ERR Comando inválido\n'))
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