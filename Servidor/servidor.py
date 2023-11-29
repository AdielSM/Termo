from termo import Termo
from jogador import Jogador

from utils import  busca_chave_por_valor
from .utils import config_server
from .utils import sumario_protocolo

import socket
import json

from threading import Thread, Lock


HOST = '0.0.0.0'
TAM_MSG, PORT = config_server()

sumario_protocolo = sumario_protocolo()

jogadoresAtivos = []
jogadoresAtivos_lock = Lock()

def criarJogadorAtivo(cliente, con) -> Jogador:
    jogador = Jogador(cliente, con)
    jogador.jogadorAtivo = True
    jogador.jogo = Termo()                
    
    with jogadoresAtivos_lock: 
        jogadoresAtivos.append(jogador)

    return jogador

def removerJogadorAtivo(cliente):
    for jogador in jogadoresAtivos:
        if jogador.cliente == cliente:
            with jogadoresAtivos_lock: 
                jogadoresAtivos.remove(jogador)
            jogador.jogadorAtivo = False
            return
    raise Exception("Jogador não encontrado.")
        

def handle_client(con, cliente):
        
    while True:
        msg = con.recv(TAM_MSG)
        if not msg: break
        processa_msg_cliente(msg, con, cliente)
    con.close()
    
    
def processa_msg_cliente(msg, con, cliente):
    data = json.loads(msg.decode())  

    print(f'Conectei com',cliente, data)
    
    comando = data.get('comando').lower()
    parametro = data.get('parametro')
    

    jogadorAtual = None
    jogo = None
    
    for jogador in jogadoresAtivos:
        if jogador.cliente == cliente:
            jogo = jogador.jogo
            jogadorAtual = jogador
            break

    # Inicia um jogador com o seu jogo
    if comando == '/game/start':
        
        if jogadorAtual in jogadoresAtivos:  
            data = {
                "message": sumario_protocolo['JOGO_JA_INICIADO']
                # 400 Jogo já iniciado
            }
            
        else:
            # Iniciar jogador
            jogadorAtual = criarJogadorAtivo(cliente, con)
                
            data = {
                "message": sumario_protocolo['JOGO_INICIADO']
                # 200 Jogo Iniciado
            }
                        
        response = json.dumps(data)
        con.send(response.encode())
                
    # Encerra a conexão com o servidor
    elif comando == '/game/exit':
        try:
            removerJogadorAtivo(cliente)                            
            data = {
                "message" : sumario_protocolo['JOGO_ENCERRADO'],
                # 201 Jogo encerrado
            }
            
        except Exception:
            data = {
                "message" : sumario_protocolo['JOGO_NAO_INICIADO'],
                # 401 Jogo não iniciado
            }
                
        response = json.dumps(data)
        con.send(response.encode())
                
    # Verifica a situação da palavra enviada pelo player
    elif comando == "/game/check_word":
        
        if not jogo:
            data = {
                "message" : sumario_protocolo['JOGO_NAO_INICIADO'],
                # 401 Jogo não iniciado
            }
            
        elif not parametro:
            data = {
                "message" : sumario_protocolo['NECESSARIO_PARAMETRO'],
            }
            
        else:
            feedback = jogo.checkWord(parametro)
            
            
            if feedback.isinstance(int):
                
                feedback = busca_chave_por_valor(sumario_protocolo,feedback)
                
                data = {
                    "message" : sumario_protocolo[feedback],
                    "remaining_attemps" : jogo.qtdTentativasRestantes
                }
            
            else:
                ...
            
            # listTermoError = ["Palavra Repetida","Tamanho Incorreto","Palavra Inexistente"]
            
            # if feedback in listTermoError:
            #     data = {
            #         "status" : 400,
            #         "message" : feedback,
            #         "remaining_attemps" : jogo.qtdTentativasRestantes
            #     }
                
            # else:
                
            #     palavraAnimacao = None
                
            #     if feedback == "Palavra Correta.":
            #         jogador.pontuacao += 1
            #         jogador.jogadorVencedor = True
                    
            #     elif jogo.qtdTentativasRestantes == 0:
            #         jogador.jogadorVencedor = False
            #         palavraAnimacao = jogo.animacao_palavra_secreta()
                    
            #     data = {        
            #         "status" : 200,
            #         "message" : feedback,
            #         "remaining_attemps" : jogo.qtdTentativasRestantes,
            #         "word_animation" : palavraAnimacao if palavraAnimacao else None
            #     }
                
        response = json.dumps(data)
        con.send(response.encode())
    
            
        
    # Lista os jogadores ativos
    elif comando == 'LIST_PLAYERS':
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
        if jogo:
            data = {
                "message" : sumario_protocolo['COMANDO_INVALIDO'],
                "remaining_attemps" : jogo.qtdTentativasRestantes
            }
            # 499 Comando inválido
        else:
            data = {
                "message" : sumario_protocolo['COMANDO_INVALIDO']
            }
            # 499 Comando inválido
        
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