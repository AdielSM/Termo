#!/usr/bin/env python3
import socket

TAM_MSG = 1024 # Tamanho do bloco de mensagem
HOST = '127.0.0.1' # IP do Servidor
PORT = 40000 # Porta que o Servidor escuta

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
        dados = sock.recv(TAM_MSG)
    if not dados: break

    msg_status = dados.decode().split('\n')[0]
    dados = dados[len(msg_status)+1:]
    print(msg_status)
    cmd_usr = cmd_usr.split()
    cmd_usr[0] = cmd_usr[0].upper()
