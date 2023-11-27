from termo import Termo
from Jogador import Jogador
import socket
import json

from threading import Thread, Lock
from utils import config_server


HOST = '0.0.0.0'
TAM_MSG, PORT = config_server()

jogadoresAtivos = []
jogadoresAtivos_lock = Lock()

def criarJogadorAtivo(cliente, con) -> Jogador:
    jogador = Jogador(cliente, con)
    jogador.jogadorAtivo = True
    jogador.jogo = Termo()                
    
    with jogadoresAtivos_lock: jogadoresAtivos.append(jogador)

    return jogador

def removerJogadorAtivo(cliente):
    for jogador in jogadoresAtivos:
        if jogador.cliente == cliente:
            with jogadoresAtivos_lock: jogadoresAtivos.remove(jogador)
            jogador.jogadorAtivo = False
            return
        

def handle_client(con, cliente):
    jogador = None
    while True:
        msg = con.recv(TAM_MSG)
        if not msg: break
        processa_msg_cliente(msg, con, cliente)
    con.close()
    
    
def processa_msg_cliente(msg, con, cliente):
    data = json.loads(msg.decode())  

    print(f'Conectei com', con, cliente, data)
    
    comando = data.get('comando').lower()
    parametro = data.get('parametro')
    
    jogadorAtual = None
    
    for jogador in jogadoresAtivos:
        if jogador.cliente == cliente:
            jogo = jogador.jogo
            jogadorAtual = jogador
            break
    else:
        jogo = None
    
    # Inicia um jogador com o seu jogo
    if comando == '/game/start':
        
        if jogadorAtual in jogadoresAtivos:  
            data = {
                "status": 400,
                "message": "Já existe um jogo iniciado"
            }
            
        else:
            try:
                # Iniciar jogador
                jogadorAtual = criarJogadorAtivo(cliente, con)
                    
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
    elif comando == '/game/exit':
        if jogadorAtual not in jogadoresAtivos:
            data = {
                "status" : 400,
                "message" : "Não existe nenhum jogo iniciado."
            }
            
        else:
            try:
                removerJogadorAtivo(cliente)                            
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
    elif comando == "/game/check_word":
        
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
                
                palavraAnimacao = None
                
                if feedback == "Palavra Correta.":
                    jogador.pontuacao += 1
                    jogador.jogadorVencedor = True
                    
                elif jogo.qtdTentativasRestantes == 0:
                    jogador.jogadorVencedor = False
                    palavraAnimacao = jogo.animacao_palavra_secreta()
                    
                data = {        
                    "status" : 200,
                    "message" : feedback,
                    "remaining_attemps" : jogo.qtdTentativasRestantes,
                    "word_animation" : palavraAnimacao if palavraAnimacao else None
                }
                
        response = json.dumps(data)
        con.send(response.encode())
    
            
        
    # Lista os jogadores ativos
    elif comando == 'LIST_PLAYERS':
        pass
    
    # Adiciona um jogador à lista de jogadores ativos, poderia ser um comando alternativo para o GetGame ?
    # elif comando == 'ADD_PLAYER':
    #     with jogadoresAtivos_lock:
    #         jogador = (cliente[0], cliente[1])
    #         jogadoresAtivos.append(jogador)
    #     con.send(str.encode(f'+OK{SEPARADOR}'))
    
    # Remove um jogador da lista de jogadores ativos forçadamente
    elif comando == 'REMOVE_PLAYER':
        pass
        
    # Lista as partidas em andamento
    elif comando == 'LIST_GAMES':
        pass
    
    # Lista as palavras que estão sendo usadas no momento e em qual partida
    elif comando == 'LIST_WORDS':
        pass
        
    # daria para fazer um jogador jogador novamente, e caso o jogador continuasse, armazenasse a quantidade de palavras que ele acertou naquela sessão?
    elif comando == 'LIST_SCORE':
        pass
    
    elif comando == 'ADD_SCORE':
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