import socket
import json

from utils import server_config

from Client import process_data, format_output

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
    table.add_row(["4", "Listar palavras do Termo"])
    table.align["Opção"] = "l"
    table.align["Descrição"] = "l"
    print('')
    print(table)
    print('')

def proccessUserCommand(comando_usuario:str)->tuple:
    if comando_usuario == '1':
        comando = "start"
        parametro = None
            
    elif comando_usuario == '2':
        comando = "exit"
        parametro = None
    
    elif comando_usuario == '3':
        comando = "check_word"
        comando_usuario = input('Digite a palavra: ')
        parametro = comando_usuario.lower()
        
    elif comando_usuario == '4':
        comando = "list_words"
        parametro = None
    
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
            process_data(response_status, remaining_attemps=remaining_attemps)
            
        elif response_status == 203:
            
            color_str = format_output(parametro, response_data["word_encoded"])
            
            
            if remaining_attemps != 0:
                process_data(response_status, color_str, remaining_attemps=remaining_attemps)
            
            else:
                process_data(response_status, color_str, secret_word=response_data["secret_word"], remaining_attemps=remaining_attemps)
                
                print('')
                print('A rodada acabou!')
                print('Deseja continuar jogando?')
                usr_input = input('Digite 1 para continuar ou 2 para sair: ')
                
                while usr_input not in ['1','2']:
                    usr_input = input('Digite 1 para continuar ou 2 para sair: ')
                
                if usr_input == '1':
                    continue
                
                print('')
                #Todo: Mostrar pontuação, colocar estatísticas
                print('Obrigado por jogar!')
                print('Feito com ❤️ em 🐍')
                break 
                
        else:
            response_message = process_data(response_status, remaining_attemps=remaining_attemps)


    #*Colocar raises em validações ao longo do código da classe
    except KeyboardInterrupt:
        comando = "/game/exit"
        parametro = None
        break
        
    except Exception as e:
        print('entrei na exception')
        print(e)
        continue
    
sock.close()