import socket
import json

from time import sleep

import sys
sys.path.append('c:/Users/adiel/OneDrive/Termo')

from utils.server_config import server_config

from utilsClient import process_data

from prettytable import PrettyTable

HOST = '127.0.0.1'
TAM_MSG, PORT = server_config()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

def tableOptions():
    table = PrettyTable()
    table.field_names = ["Opção", "Descrição"]
    table.add_row(["1", "Começar um jogo"])
    table.add_row(["2", "Sair do jogo atual"])
    table.add_row(["3", "Checar palavra"])
    table.align["Opção"] = "l"
    table.align["Descrição"] = "l"
    print('')
    print(table)
    print('')

def proccessUserCommand(comando_usuario:str)->tuple:
    if comando_usuario == '1':
        comando = "/game/start"
        parametro = None
            
    elif comando_usuario == '2':
        comando = "/game/exit"
        parametro = None
    
    elif comando_usuario == '3':
        comando = "/game/check_word"
        comando_usuario = input('Digite a palavra: ')
        parametro = comando_usuario.lower()
    
    else:
        raise Exception("Comando inválido:",comando_usuario)

    return (comando, parametro)


while True:
    try:
        tableOptions()
        cmd_usr = input('Termo> ')

        comando, parametro = proccessUserCommand(cmd_usr)
        
        data = {
            "comando" : comando,
            "parametro" : parametro
        }
        
        json_data = json.dumps(data)
        sock.sendall(json_data.encode())
        
        response = sock.recv(TAM_MSG)
        response_data = json.loads(response)
        
        response_status =  response_data["code_status"]
        remaining_attemps = response_data.get("remaining_attemps")
        
        if response_status in [200,201,401]:
            response_message = process_data(response_status)
            
        elif response_status == 203:
            response_message = process_data(response_status, word_encoded=response_data["word_encoded"], word_user=parametro, remaining_attemps=remaining_attemps)
            
            if remaining_attemps == 0:
                break
            
        else:
            response_message = process_data(response_status, remaining_attemps=remaining_attemps)


    #*Colocar raises em validações ao longo do código da classe
    except KeyboardInterrupt:
        comando = "/game/exit"
        parametro = None
        break
        
    except Exception as e:
        print(e)
        continue
    
sock.close()