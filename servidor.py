#!/usr/bin/env python3
import socket
import os
from threading import Thread

from termo import Termo
from listaEncadeadaSimples import ListaEncadeadaSimples

TAM_MSG = 1024 # Tamanho do bloco de mensagem
HOST = '0.0.0.0' # IP do Servidor
PORT = 40000 # Porta que o Servidor escuta


def processa_msg_cliente(msg, con):
    msg = msg.decode().split()
    comando, parametro = msg[0], msg[1:]
    
    if comando.upper() == 'GET_GAME':
        jogo = Termo()
        con.send(str.encode(f'+OK \n'))
        #logica do jogo
        
    
    # Encerra a conexão com o servidor
    elif comando.upper() == 'EXIT_GAME':
        con.send(str.encode('+OK\n'))
        return False 
    
    # Verifica a situação da palavra enviada pelo player
    elif comando.upper() == 'CHECK_WORD':
        estado = jogo.checkPalavra(parametro[0])
        if estado == 'acertou':
            con.send(str.encode('+ACERTOU\n'))
            con.send(str.encode(f'Palavra: {jogo.palavra}\n'))
            con.send(str.encode(f'{jogo.qtdTentativasRestantes} tentativas restantes\n'))
            
        elif estado == 'Palavra repetida':
            con.send(str.encode('-ERRO Palavra repetida\n'))
            con.send(str.encode('Tente novamente\n'))
            processa_msg_cliente(msg, con)
            con.send(str.encode(f'{jogo.qtdTentativasRestantes} tentativas restantes\n'))
            
        elif estado == 'Tamanho incorreto':
            con.send(str.encode('-ERRO Palavra deve conter 6 letras\n'))
            con.send(str.encode('Tente novamente\n'))
            processa_msg_cliente(msg, con)
            con.send(str.encode(f'{jogo.qtdTentativasRestantes} tentativas restantes\n'))
            
        elif estado == 'Palavra inexiste':
            con.send(str.encode('-ERRO Essa palavra não é aceita\n'))
            con.send(str.encode('Tente novamente\n'))
            processa_msg_cliente(msg, con)
            con.send(str.encode(f'{jogo.qtdTentativasRestantes} tentativas restantes\n'))
            
        else:
            con.send(str.encode(f'-ERROU {estado}\n'))
            con.sed(str.encode(f'{jogo.qtdTentativasRestantes} tentativas restantes\n'))
        
    
    # Lista os jogadores ativos
    elif comando.upper() == 'LIST_PLAYERS':
        pass
    
    # Adiciona um jogador à lista de jogadores ativos, poderia ser um comando alternativo para o GetGame ?
    elif comando.upper() == 'ADD_PLAYER':
        pass
    
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


jogadoresAtivos = ListaEncadeadaSimples()

def main():
    # Cria o socket do servidor
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Permite que o servidor seja reiniciado rapidamente
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Associa o socket do servidor com o IP e a porta definidos
    sock.bind((HOST, PORT))
    # Habilita o servidor a aceitar conexões
    sock.listen()
    print(f'Servidor escutando em {HOST}:{PORT} ...')
    while True:
        # Aceita uma nova conexão
        con, cliente = sock.accept()
        print(f'Conexão estabelecida com {cliente}')
        # Cria uma nova thread para processar a mensagem do cliente
        t = Thread(target=processa_msg_cliente, args=(con.recv(TAM_MSG), con, cliente))
        t.start()
    sock.close()