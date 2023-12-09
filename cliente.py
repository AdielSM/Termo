import socket
import json

from time import sleep
from enum import Enum
from utils import server_config

from Client import render_response, format_output

from prettytable import PrettyTable

HOST = '127.0.0.1'
TAM_MSG, PORT = server_config()

def connect_to_server():
    for _ in range(5):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
            return sock
        except socket.error:
            print("Erro ao conectar ao servidor. Tentando novamente em 5 segundos.")
            sleep(5)

    raise socket.error("Não foi possível conectar ao servidor. Tente reiniciar o jogo.")
    
try:
    sock = connect_to_server()
except socket.error as e:
    print('')
    print(e)
    exit()

class EstadoDoJogo(Enum):
    Sem_jogo = 1
    Jogo_em_andamento = 2
    Jogo_finalizado = 3

table = PrettyTable()
estadoDoJogo = EstadoDoJogo.Sem_jogo

print('='*50)
print('Bem vindo ao jogo de palavras Termo!')
print('='*50)
nomeUsuario = input('Digite seu nome: ')

def renderTable():
    table.clear_rows()
    table.field_names = ["Opção", "Descrição"]
    table.add_row(["1", "Começar um jogo"])
    table.add_row(["2", "Sair do jogo atual"])

    if estadoDoJogo != EstadoDoJogo.Sem_jogo:
        table.add_row(["3", "Checar palavra"])
        table.add_row(["4", "Listar palavras digitadas nessa rodada"])
        table.add_row(["5", "Reiniciar jogo atual"])

    table.align["Opção"] = "l"
    table.align["Descrição"] = "l"

    print(table)

def proccessUserCommand(comando_usuario:str)->tuple:
    if comando_usuario == '1':
        comando = "start_game"
        parametro = None
        
    elif comando_usuario == '2':
        comando = "exit_game"
        parametro = None
    
    elif comando_usuario == '3' and estadoDoJogo == EstadoDoJogo.Jogo_em_andamento:
        comando = "check_word"
        comando_usuario = input('Digite a palavra: ')
        parametro = comando_usuario.lower()
        
    elif comando_usuario == '4' and estadoDoJogo == EstadoDoJogo.Jogo_em_andamento:
        comando = "list_words"
        parametro = None
        
    elif comando_usuario == '5' and estadoDoJogo == EstadoDoJogo.Jogo_em_andamento:
        comando = "restart_game"
        parametro = nomeUsuario
    
    else:
        raise ValueError("Comando inválido:" + " " + comando_usuario)

    return (comando, parametro)

def sendRequisition(req_body) -> json:
    json_data = json.dumps(req_body)
    sock.sendall(json_data.encode())
    
    response = sock.recv(TAM_MSG)
    response_data = json.loads(response)
    return response_data
    
def checkEndGame() -> bool:
    global estadoDoJogo
    estadoDoJogo = EstadoDoJogo.Jogo_finalizado

    print('')
    print('A rodada acabou!')
    print('Deseja continuar jogando?')
    usr_input = input('Digite 1 para continuar ou 2 para sair: ')
    
    while usr_input not in ['1','2']:
        usr_input = input('Digite uma opção válida (1/2): ')
    
    # Reinicia com novo jogo pra continuar e retorna False pra indicar continuação
    if usr_input == '1':
        req_body = {
            "comando" : "continue_game",
            "parametro" : None
        }

        response_data = sendRequisition(req_body)
        response_status = response_data["code_status"]
        
        render_response(response_status, player_name=nomeUsuario)
        
        estadoDoJogo = EstadoDoJogo.Jogo_em_andamento

        return False
    
    print('')
    #Todo: Mostrar pontuação, colocar estatísticas
    print(f'Obrigado por jogar {nomeUsuario}!')
    print('Feito com ❤️  em 🐍')
    return True

while True:
    try:
        renderTable()
        print("\033[90mAperte Ctrl + C para encerrar o Termo!\033[0m")
        cmd_usr = input('Termo> ')

        comando, parametro = proccessUserCommand(cmd_usr)
        
        req_body = {
            "comando" : comando,
            "parametro" : parametro
        }
        
        response_data = sendRequisition(req_body)
        response_status =  response_data["code_status"]
        remaining_attempts = response_data.get("remaining_attempts")
        
        
        if response_status == 200:
            render_response(response_status)
            estadoDoJogo = EstadoDoJogo.Jogo_em_andamento

        elif response_status == 201:
            render_response(response_status)
            estadoDoJogo = EstadoDoJogo.Sem_jogo

        elif response_status == 202:
            render_response(response_status, remaining_attempts=remaining_attempts)
            if checkEndGame():
                break

        elif response_status == 203:
            color_str = format_output(parametro, response_data["word_encoded"])

            if remaining_attempts != 0:
                render_response(response_status, color_str, remaining_attempts=remaining_attempts)
            else:
                render_response(response_status, color_str, secret_word=response_data["secret_word"], remaining_attempts=remaining_attempts)
                if checkEndGame():
                    break

        elif response_status == 206:
            render_response(response_status, player_name=nomeUsuario)
            
        elif response_status in [402, 403, 404, 405]:
            render_response(response_status, remaining_attempts=remaining_attempts)

        else:
            if response_status == 499 and remaining_attempts:
                render_response(response_status, remaining_attempts=remaining_attempts)
            else:
                render_response(response_status)


    #*Colocar raises em validações ao longo do código da classe
    except KeyboardInterrupt:
        print('')
        print(f'Obrigado por jogar {nomeUsuario}!')
        print('Feito com ❤️  em 🐍')
        break
        
    except ValueError as e:
        print(e)
        continue
    
    except Exception as e:
        print(e)
        continue
    
sock.close()