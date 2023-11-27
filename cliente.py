import socket
import json

from time import sleep

from utils.server_config import config_server

from prettytable import PrettyTable

HOST = '127.0.0.1'
TAM_MSG, PORT = config_server()

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
        
        response_status =  response_data["status"]
        response_message = response_data["message"]
        
        if response_status == 400:
            print(response_message)
            
            if "remaining_attemps" in response_data.keys():
                print(f'Tentativas Restantes: {response_data["remaining_attemps"]}')
            continue
        
        else:
            if comando == "/game/start":
                print(response_message)
                
            elif comando == "/game/exit":
                print(response_message)
                break
            
            elif comando == "/game/check_word":
                
                tentativas = response_data["remaining_attemps"]
                
                if response_message == "Palavra Correta.":
                    print('Parabéns! Você conseguiu acertar a palavra!')
                    print('Suas Tentativas Restantes:',tentativas)
                    print('')
                    print('Obrigado por jogar!')
                    break
                
                else:
                    
                    if tentativas == 0:
                        saida = response_data["word_animation"]
                        print(saida[0])
                        
                        for i in range(1,len(saida)):
                            
                            letra =  "\033[92m" + saida[i] + "\033[0m"
                            
                            if i == len(saida)-1:
                                print(letra,end="")
                            else:
                                print(letra)
                                sleep(1)
                        break
                    
                    else:
                        palavra = ''
                        for index,itens in enumerate(response_message):
                            if itens == "green":
                                palavra += "\033[92m" + parametro[index] + "\033[0m"
                            elif itens == "yellow":
                                palavra += "\033[93m" + parametro[index] + "\033[0m"
                            else:
                                palavra += "\033[90m" + parametro[index] + "\033[0m"
                        print(palavra)
                        print('Tentativas Restantes:',tentativas)
                        print('')


    #*Colocar raises em validações ao longo do código da classe
    except KeyboardInterrupt:
        comando = "/game/exit"
        parametro = None
        break
        
    except Exception as e:
        print(e)
        continue
    
sock.close()