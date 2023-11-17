#!/usr/bin/env python3
import socket
import os
from threading import Thread
from termo import Termo

TAM_MSG = 1024 # Tamanho do bloco de mensagem
HOST = '0.0.0.0' # IP do Servidor
PORT = 40000 # Porta que o Servidor escuta

def processa_msg_cliente(msg, con, cliente):
    msg = msg.decode().split()
    comando, parametro = msg[0], msg[1:]
    
    if comando.upper() == 'GET_GAME':
        jogo = Termo()
        
        
        
        
        # nome_arq = " ".join(msg[1:])
        # print('Arquivo solicitado:', nome_arq)
        # try:
        #     status_arq = os.stat(nome_arq)
        #     con.send(str.encode('+OK {}\n'.format(status_arq.st_size)))
        #     arq = open(nome_arq, "rb")
        #     while True:
        #         dados = arq.read(TAM_MSG)
        #         if not dados: break
        #         con.send(dados)
        # except Exception as e:
        #     con.send(str.encode('-ERR {}\n'.format(e)))
    elif comando.upper() == 'EXIT_GAME':
        con.send(str.encode('+OK\n'))
        return False 
    
    elif comando.upper() == 'CHECK_WORD':
        pass
    
    
    
    
    
    
    
    
    
#     elif msg[0].upper() == 'LIST':
#         lista_arq = os.listdir('.')
#         con.send(str.encode('+OK {}\n'.format(len(lista_arq))))
#         for nome_arq in lista_arq:
#             if os.path.isfile(nome_arq):
#                 status_arq = os.stat(nome_arq)
#                 con.send(str.encode('arq: {} - {:.1f}KB\n'.
#                     format(nome_arq, status_arq.st_size/1024)))

#             elif os.path.isdir(nome_arq):
#                 con.send(str.encode('dir: {}\n'.format(nome_arq)))
#             else:
#                 con.send(str.encode('esp: {}\n'.format(nome_arq)))

#     elif msg[0].upper() == 'CWD':
#         cam_dir = " ".join(msg[1:])
#         try:
#             os.chdir(cam_dir)
#             con.send(str.encode('+OK'))
#         except Exception as e:
#             con.send(str.encode(f'-ERR {e}\n'))
#     else:
#         con.send(str.encode('-ERR Invalid command\n'))
#     return True

# def processa_cliente(con, cliente):
#     print('Cliente conectado', cliente)
#     while True:
#         msg = con.recv(TAM_MSG)
#         if not msg or not processa_msg_cliente(msg, con, cliente): break
#     con.close()
#     print('Cliente desconectado', cliente)

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# serv = (HOST, PORT)
# sock.bind(serv)
# sock.listen(50)
# while True:
#     try:
#         con, cliente = sock.accept()
#     except: break
#     # processa_cliente(con, cliente)
#     t = Thread(target=processa_cliente, args=(con, cliente))
#     t.start()
# sock.close()