import socket
import json
from threading import Thread, Lock

from termo import Termo
from Estruturas.listaEncadeadaSimples import Lista

from utils.server_config import config_server

HOST = '0.0.0.0'
TAM_MSG, PORT = config_server()

jogadoresAtivos = Lista()
jogadoresAtivos_lock = Lock()


def handle_client(con, cliente):
    jogo = Termo()

    while True:
        msg = con.recv(TAM_MSG)
        if not msg: break
        processa_msg_cliente(msg, con, cliente, jogo)
    con.close()
    
    
def processa_msg_cliente(msg, con, cliente, jogo:Termo):
    data = json.loads(msg.decode())  
    
    comando = data.get('comando').lower()
    parametro = data.get('parametro')
    print(comando)
    print(parametro)

    if comando == '/game/start':
        if not jogo.jogoNaoIniciado():  
            data = {
                "status": 400,
                "message": "O jogo já foi iniciado."
            }
        else:
            try:    
                jogo.iniciarJogo()
                data = {
                    "status": 200,
                    "message": "Jogo iniciado com sucesso."
                }
            except Exception as e: 
                data = {
                    "status": 400,
                    "message": str(e)  
                }
            finally:
                response = json.dumps(data)
                con.sendall(response.encode())
                
    # Encerra a conexão com o servidor
    elif comando.upper() == '/game/exit':
        if jogo.jogoNaoInicado():
            data = {
                "status" : 400,
                "message" : "Não existe nenhum jogo iniciado."
            }
            
        else:
            try:
                del jogo
                data = {
                    "status" : 200,
                    "message" : "Jogo encerrado"
                }
            except Exception as e:
                data = {
                    "status" : 400,
                    "message" : "Não existe nenhum jogo iniciado"
                }
            finally:
                response = json.dumps(data)
                con.sendall(response.encode())
                
    # Verifica a situação da palavra enviada pelo player
    elif comando.upper() == "/game/check_word":
        feedback = jogo.checkWord(parametro)
        
        listTermoError = ["Palavra Repetida","Tamanho Incorreto","Palavra Inexistente"]
        
        if feedback in listTermoError:
            data = {
                "status" : 400,
                "message" : feedback,
                "remaining_attemps" : jogo.qtdTentativasRestantes
            }
            
        else:
            data = {        
                "status" : 200,
                "message" : feedback,
                "remaining_attemps" : jogo.qtdTentativasRestantes
            }
            
        response = json.dumps(data)
        con.sendall(response.encode())
            
        
    # Lista os jogadores ativos
    elif comando.upper() == 'LIST_PLAYERS':
        pass
    
    # Adiciona um jogador à lista de jogadores ativos, poderia ser um comando alternativo para o GetGame ?
    # elif comando.upper() == 'ADD_PLAYER':
    #     with jogadoresAtivos_lock:
    #         jogador = (cliente[0], cliente[1])
    #         jogadoresAtivos.append(jogador)
    #     con.sendall(str.encode(f'+OK{SEPARADOR}'))
    
    # Remove um jogador da lista de jogadores ativos forçadamente
    elif comando.upper() == 'REMOVE_PLAYER':
        pass
        
    # Lista as partidas em andamento
    elif comando.upper() == 'LIST_GAMES':
        pass
    
    # Lista as palavras que estão sendallo usadas no momento e em qual partida
    elif comando.upper() == 'LIST_WORDS':
        pass
        
    # daria para fazer um jogador jogador novamente, e caso o jogador continuasse, armazenasse a quantidade de palavras que ele acertou naquela sessão?
    elif comando.upper() == 'LIST_SCORE':
        pass
    
    elif comando.upper() == 'ADD_SCORE':
        pass
    
    else:
        data = {
            "status": 400,
            "message": "Comando iiiiinválido"
        }
        response = json.dumps(data)
        con.sendall(response.encode())
    
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