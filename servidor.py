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
        con.send(str.encode(f'+OK \n'))
        #logica do jogo
        
    
    # Encerra a conexão com o servidor
    elif comando.upper() == 'EXIT_GAME':
        con.send(str.encode('+OK\n'))
        return False 
    
    # Verifica a situação da palavra enviada pelo player
    elif comando.upper() == 'CHECK_WORD':
        pass
    
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
        
    # daria para fazer um jogador novamente, e caso o jogador continuasse, armazenasse a quantidade de palavras que ele acertou naquela sessão?
    elif comando.upper() == 'LIST_SCORE':
        pass
    
    elif comando.upper() == 'ADD_SCORE':
        pass
    
    
    else:
        con.send(str.encode('-ERR Comando inválido\n'))
        return False
    
    return True