import socket
import json
from threading import Thread, Lock

from termo import Termo
from Jogador import Jogador

from Estruturas.listaEncadeadaSimples import Lista

from utils.server_config import config_server

HOST = '0.0.0.0'
TAM_MSG, PORT = config_server()

jogadoresAtivos = []
jogadoresAtivos_lock = Lock()

def handle_client(con, cliente):
    
    while True:
        msg = con.recv(TAM_MSG)
        if not msg: break
        processa_msg_cliente(msg, con, cliente)
    con.close()
    
    
def processa_msg_cliente(msg, con, cliente):
    data = json.loads(msg.decode())  
    
    comando = data.get('comando').lower()
    parametro = data.get('parametro')
    
    for jogador in jogadoresAtivos:
        if jogador.cliente == cliente:
            jogo = jogador.jogo
            break
    
    else:
        jogo = None
    

    if comando == '/game/start':
        
        if cliente in jogadoresAtivos:  
            data = {
                "status": 400,
                "message": "Já existe um jogo iniciado"
            }
            
        else:
            try:    
                jogador = Jogador(cliente, con)
                jogador.jogadorAtivo = True
                jogador.jogo = Termo()                
                
                with jogadoresAtivos_lock:
                    jogadoresAtivos.append(cliente)
                    
                data = {
                    "status": 200,
                    "message": "Jogo iniciado com sucesso."
                }
                
            except Exception as e: 
                data = {
                    "status": 400,
                    "message": str(e)  
                }
            
        response = json.dumps(data)
        con.send(response.encode())
                
    # Encerra a conexão com o servidor
    elif comando.upper() == '/game/exit':
        if cliente not in jogadoresAtivos:
            data = {
                "status" : 400,
                "message" : "Não existe nenhum jogo iniciado."
            }
            
        else:
            try:
                for jogador in jogadoresAtivos:
                        
                        if jogador.cliente == cliente:
                            with jogadoresAtivos_lock:
                                jogadoresAtivos.remove(jogador)
                                jogador.jogadorAtivo = False
                                break
                            
                data = {
                    "status" : 200,
                    "message" : "Jogo encerrado"
                }
                
            except Exception as e:
                data = {
                    "status" : 400,
                    "message" : str(e)
                }
                
        response = json.dumps(data)
        con.send(response.encode())
                
    # Verifica a situação da palavra enviada pelo player
    elif comando.upper() == "/game/check_word":
        
        if not jogo:
            data = {
                "status" : 400,
                "message" : "Não existe nenhum jogo iniciado."
            }
            
        elif not parametro:
            data = {
                "status" : 400,
                "message" : "Nenhuma Palavra foi passada."
            }
            
        else:
            feedback = jogo.checkWord(parametro)
            
            listTermoError = ["Palavra Repetida","Tamanho Incorreto","Palavra Inexistente"]
            
            if feedback in listTermoError:
                data = {
                    "status" : 400,
                    "message" : feedback,
                    "remaining_attemps" : jogo.qtdTentativasRestantes
                }
                
            else:
                
                if feedback == "Palavra Correta.":
                    jogador.pontuacao += 1
                    jogador.jogadorVencedor = True
                    
                data = {        
                    "status" : 200,
                    "message" : feedback,
                    "remaining_attemps" : jogo.qtdTentativasRestantes
                }
                
        response = json.dumps(data)
        con.send(response.encode())
    
            
        
    # Lista os jogadores ativos
    elif comando.upper() == 'LIST_PLAYERS':
        pass
    
    # Adiciona um jogador à lista de jogadores ativos, poderia ser um comando alternativo para o GetGame ?
    # elif comando.upper() == 'ADD_PLAYER':
    #     with jogadoresAtivos_lock:
    #         jogador = (cliente[0], cliente[1])
    #         jogadoresAtivos.append(jogador)
    #     con.send(str.encode(f'+OK{SEPARADOR}'))
    
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
        data = {
            "status": 400,
            "message": "Comando inválido"
        }
        
        response = json.dumps(data)
        con.send(response.encode())
    
    return True

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(10)

while True:
    try:
        con, cliente = sock.accept()
        t = Thread(target=handle_client, args=(con, cliente))
        t.start()
    except: break
    
sock.close()