from termo import Termo
from jogador import Jogador

import sys
sys.path.append('c:/Users/adiel/OneDrive/Termo')

from utils.sumario_protocolo import sumario_protocolo
from utils.server_config import server_config


import socket
import json

from threading import Thread, Lock


HOST = '0.0.0.0'
TAM_MSG, PORT = server_config()

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
    termo = None
    
    for jogador in jogadoresAtivos:
        if jogador.cliente == cliente:
            termo = jogador.jogo
            jogadorAtual = jogador
            break

    # Inicia um jogador com o seu jogo
    if comando == '/game/start':
        
        if jogadorAtual:  
            data = {
                "code_status": sumario_protocolo['JOGO_JA_INICIADO']
                # 400 Jogo já iniciado
            }
            
        else:
            # Iniciar jogador
            jogadorAtual = criarJogadorAtivo(cliente, con)
                
            data = {
                "code_status": sumario_protocolo['JOGO_INICIADO']
                # 200 Jogo Iniciado
            }
                        
        response = json.dumps(data)
        con.send(response.encode())
                
    # Encerra a conexão com o servidor
    elif comando == '/game/exit':
        try:
            removerJogadorAtivo(cliente)                            
            data = {
                "code_status" : sumario_protocolo['JOGO_ENCERRADO'],
                # 201 Jogo encerrado
            }
            
        except Exception:
            data = {
                "code_status" : sumario_protocolo['JOGO_NAO_INICIADO'],
                # 401 Jogo não iniciado
            }
                
        response = json.dumps(data)
        con.send(response.encode())
                
    # Verifica a situação da palavra enviada pelo player
    elif comando == "/game/check_word":
        
        if not termo:
            data = {
                "code_status" : sumario_protocolo['JOGO_NAO_INICIADO'],
                # 401 Jogo não iniciado
            }
            
        elif not parametro:
            data = {
                "code_status" : sumario_protocolo['NECESSARIO_PARAMETRO'],
                # 402 Necessário parâmetro
            }
            
        else:
            feedback = termo.checkWord(parametro)
            
            if feedback.isinstance(int):
                
                if feedback == 202:
                    jogadorAtual.addPontuacao()
                    jogadorAtual.jogadorVencedor = True
                    
                data = {
                    "code_status" : feedback, # 202 Palavra Correta
                    "remaining_attemps" : termo.qtdTentativasRestantes
                }
            
            else:
                
                data = {
                    "code_status" : sumario_protocolo['PALAVRA_INCORRETA'], # 203 Palavra Incorreta
                    "feedback" : feedback, # Lista com números para tradução no cliente
                    "remaining_attemps" : termo.qtdTentativasRestantes
                }
            
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
        if termo:
            data = {
                "code_status" : sumario_protocolo['COMANDO_INVALIDO'],
                "remaining_attemps" : termo.qtdTentativasRestantes
            }
            # 499 Comando inválido
        else:
            data = {
                "code_status" : sumario_protocolo['COMANDO_INVALIDO']
            }
            # 499 Comando inválido
        
        response = json.dumps(data)
        con.send(response.encode())


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