#!/usr/bin/env python3
import socket
from utils.server_config import config_server

HOST = '127.0.0.1' # IP do Servidor
TAM_MSG, PORT, SEPARADOR = config_server()
SEPARADOR = '\n' # Corrigir erro do separador

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

while True:
    try:
        cmd_usr = input('Termo> ')
    except:
        cmd_usr = 'EXIT_GAME'
    
    if not cmd_usr:
        print('Comando indefinido:', cmd_usr)
        
    else:
        sock.send(str.encode(cmd_usr))
        server_msg = sock.recv(TAM_MSG)
        server_msg_status = server_msg.decode().split(SEPARADOR)[0]
        
        saida = server_msg.decode()[len(server_msg_status)+len(SEPARADOR):]
        
        if server_msg_status == '-ERR': print(saida)        

        elif server_msg_status == '-EXIT':
            print(saida)
            sock.close()
            break
            
        # elif server_msg_status == '+START': print(saida)
        
        else: print(saida)
            # server_msg = saida
            # saida = server_msg.split(',')
            # print(saida[0])
            # print(saida[1])
            
    # msg_status = dados.decode().split('\n')[0]
    # dados = dados[len(msg_status)+1:]
    # cmd_usr = cmd_usr.split()
    # cmd_usr[0] = cmd_usr[0].upper()
