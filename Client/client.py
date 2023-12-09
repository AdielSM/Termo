from time import sleep
from enum import Enum
from prettytable import PrettyTable
import socket
import json
import sys
from typing import Tuple, Dict, Any, List, Optional

from utils import server_config, PilhaSequencial



class EstadoDoJogo(Enum):
    Sem_jogo = 1
    Jogo_em_andamento = 2
    Jogo_finalizado = 3
    

class Logger:
    def __init__(self) -> None:
        pass
    
    def update(self, message: str) -> None:
        print(message)
    
    def info(self, message: str) -> None:
        print(message)

class Client:
    def __init__(self) -> None:
        self.__HOST: str = '127.0.0.1'
        self.__TAM_MSG, self.__PORT = server_config()
        self.__sock: Optional[socket.socket] = None
        self.__estadoDoJogo: EstadoDoJogo = EstadoDoJogo.Sem_jogo
        self.__nomeUsuario: Optional[str] = None
        self.__observers: List[Logger] = []
        self.__pilhaPalavras = PilhaSequencial()
        
    def subscribe(self, observer: Logger) -> None:
        self.__observers.append(observer)
        
    def __notify(self, message: str) -> None:
        for observer in self.__observers:
            observer.update(message)
            
    def __info(self, message: str) -> None:
        for observer in self.__observers:
            observer.info(message)

    def connect_to_server(self) -> socket.socket:
        for _ in range(5):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.__HOST, self.__PORT))
                return sock
            except socket.error:
                self.__notify("Erro ao conectar ao servidor. Tentando novamente em 5 segundos.")
                sleep(5)
            except KeyboardInterrupt:
                self.__notify("Encerrando o Termo!")
                exit(0)

        raise socket.error("Não foi possível conectar ao servidor. Tente reiniciar o jogo.")

    def render_table(self) -> None:
        table = PrettyTable()
        table.clear_rows()
        table.field_names = ["Opção", "Descrição"]
        table.add_row(["1", "Começar um jogo"])
        table.add_row(["2", "Sair do jogo atual"])

        if self.__estadoDoJogo != EstadoDoJogo.Sem_jogo:
            table.add_row(["3", "Checar palavra"])
            table.add_row(["4", "Listar palavras digitadas nessa rodada"])
            table.add_row(["5", "Reiniciar jogo atual"])

        table.align["Opção"] = "l"
        table.align["Descrição"] = "l"

        self.__notify(str(table))

    def process_user_command(self, comando_usuario: str) -> Tuple[str, Any]:
        if comando_usuario == '1':
            comando = "start_game"
            parametro = None

        elif comando_usuario == '2':
            comando = "exit_game"
            parametro = None

        elif comando_usuario == '3' and self.__estadoDoJogo == EstadoDoJogo.Jogo_em_andamento:
            comando = "check_word"
            comando_usuario = input('Digite a palavra: ')
            parametro = comando_usuario.lower()

        elif comando_usuario == '4' and self.__estadoDoJogo == EstadoDoJogo.Jogo_em_andamento:
            comando = "list_words"
            parametro = None

        elif comando_usuario == '5' and self.__estadoDoJogo == EstadoDoJogo.Jogo_em_andamento:
            comando = "restart_game"
            parametro = self.__nomeUsuario

        else:
            raise ValueError("Comando inválido:" + " " + comando_usuario)

        return (comando, parametro)


    
    def send_requisition(self, req_body: Dict[str, Any]) -> Dict[str, Any]:
        json_data = json.dumps(req_body)
        self.__sock.sendall(json_data.encode())

        response = self.__sock.recv(self.__TAM_MSG)
        response_data = json.loads(response)
        return response_data

    
    #todo - refatorar para fazer apenas uma coisa, retornar ou exibir
    def check_end_game(self) -> bool:
        self.__estadoDoJogo = EstadoDoJogo.Jogo_finalizado

        self.__notify('')
        self.__notify('A rodada acabou!')
        self.__notify('Deseja continuar jogando?')
        usr_input = input('Digite 1 para continuar ou 2 para sair: ')

        while usr_input not in ['1', '2']:
            usr_input = input('Digite uma opção válida (1/2): ')

        # Reinicia com novo jogo pra continuar e retorna False pra indicar continuação
        if usr_input == '1':
            req_body = {
                "comando": "continue_game",
                "parametro": None
            }

            response_data = self.send_requisition(req_body)
            response_status = response_data["code_status"]

            self.__render_response(response_status, player_name=self.__nomeUsuario)

            self.__estadoDoJogo = EstadoDoJogo.Jogo_em_andamento

            return False

        self.__notify('')

        self.__notify(f'Obrigado por jogar {self.__nomeUsuario}!')
        self.__notify('Feito com ❤️  em 🐍')
        return True

    def print_welcome_message(self) -> None:
        self.__notify('=' * 50)
        self.__notify('Bem vindo ao jogo de palavras Termo!')
        self.__notify('=' * 50)

    def get_username(self) -> str:
        return input('Digite seu nome: ')

    def get_user_command(self) -> str:
        return input('Termo> ')
    
    def print_exit_message(self) -> None:
        self.__notify("\033[90mAperte Ctrl + C para encerrar o Termo!\033[0m")


    def create_request_body(self, comando: str, parametro: Any) -> Dict[str, Any]:
        return {
            "comando": comando,
            "parametro": parametro
        }

    def handle_keyboard_interrupt(self) -> None:
        self.__notify('')
        self.__notify(f'Obrigado por jogar {self.__nomeUsuario}!')
        self.__notify('Feito com ❤️  em 🐍')
    

    def __secret_word_animation(self, palavra) -> None:
        palavra_transformada = ['_' for _ in palavra]
        
        self.__info('Você não conseguiu adivinhar a palavra secreta!')
        self.__info('A palavra era:')
        
        for i in range(len(palavra)):
            palavra_transformada[i] = palavra[i]
            self.__info(''.join(palavra_transformada))
            sleep(1)
            

    def __handle_successful_cases(self, response_status, **extra_info):
        
        remaining_attempts = extra_info.get("remaining_attempts")
        format_output = extra_info.get("format_output")
        secret_word = extra_info.get("secret_word")
        player_name = extra_info.get("player_name")
        
        match response_status:
            case 200:
                self.__info("Jogo Iniciado com Sucesso\n")
            case 201:
                self.__info("Jogo Encerrado com Sucesso\n")
            case 202:
                self.__info("🏆 Parabéns! Palavra Correta! 😎")
                self.__info("Lista de Palavras Anteriores:")
                self.__info(str(self.__pilhaPalavras))
                self.__pilhaPalavras.clear()
                self.__info(f"Tentativas Restantes: {remaining_attempts}")
                
            case 203:
                self.__pilhaPalavras.empilha(format_output)
                self.__info('')
                self.__info("Palavra Incorreta!")
                self.__info(format_output)
                self.__info('')
                self.__info(f"Tentativas Restantes: {remaining_attempts}")
                
                if remaining_attempts == 0:
                    self.__pilhaPalavras.clear()
                    self.__secret_word_animation(secret_word)
                    
            case 204:
                self.__info("Lista de Palavras:")
                self.__info(str(self.__pilhaPalavras) + "\n")
            case 205:
                self.__info('Jogo Reiniciado com Sucesso\n')
            case 206:
                self.__info(f'Jogo Continuado com Sucesso, Boa Sorte na Próxima Rodada {player_name}!\n')

    def __handle_error_cases(self, response_status, **remaining_attempts):
        
        remaining_attempts = remaining_attempts.get("remaining_attempts")
        
        match response_status:
            case 400:
                self.__info("Jogo já iniciado\n")
            case 401:
                self.__info("Jogo não iniciado\n")
            case 402:
                self.__info("Necessário Forcener uma Palavra")
                self.__info(remaining_attempts)
            case 403:
                self.__info("A palavra deve conter 5 letras")
                self.__info(remaining_attempts)
            case 404:
                self.__info("Palavra inexiste no dicionário")
                self.__info(remaining_attempts)
            case 405:
                self.__info("Palavra já utilizada")
                self.__info(remaining_attempts)
            case 499:
                if remaining_attempts:
                    self.__info("Comando Inválido")
                    self.__info(remaining_attempts)
                else:
                    self.__info("Comando Inválido")

    def __render_response(self, response_status: int, **extra_info):
        
        if 200 <= response_status < 400:
            self.__handle_successful_cases(response_status, **extra_info)
        
        elif 400 <= response_status < 500:
            self.__handle_error_cases(response_status, **extra_info)

    
    def handle_response_status(self, response_status: int, response_data: Dict[str, Any], parametro: Any) -> bool:
        remaining_attempts = response_data.get("remaining_attempts")
        if response_status == 200:
            self.__render_response(response_status)
            self.__estadoDoJogo = EstadoDoJogo.Jogo_em_andamento

        elif response_status == 201:
            self.__render_response(response_status)
            self.__estadoDoJogo = EstadoDoJogo.Sem_jogo

        elif response_status == 202:
            self.__render_response(response_status, remaining_attempts=remaining_attempts)
            if self.check_end_game():
                self.__sock.close()
                sys.exit(0)        
                
        elif response_status == 203:
            color_str = self.__format_output(parametro, response_data["word_encoded"])

            if remaining_attempts != 0:
                self.__render_response(response_status, format_output=color_str, remaining_attempts=remaining_attempts)
            else:
                self.__render_response(response_status, format_output=color_str, secret_word=response_data["secret_word"],
                                remaining_attempts=remaining_attempts)
                if self.check_end_game():
                    self.__sock.close()     
                    sys.exit(0)  
                    

        elif response_status == 206:
            self.__render_response(response_status, player_name=self.__nomeUsuario)
            
        else:
            self.__render_response(response_status, remaining_attempts=remaining_attempts)
                
    def run(self) -> None:
            try:    
                self.__sock = self.connect_to_server()  
                self.print_welcome_message()
                self.__nomeUsuario = self.get_username()

                while True:
                    try:
                        self.render_table()
                        self.print_exit_message()
                        cmd_usr = self.get_user_command()

                        comando, parametro = self.process_user_command(cmd_usr)
                        req_body = self.create_request_body(comando, parametro)

                        response_data = self.send_requisition(req_body)
                        response_status = response_data["code_status"]

                        self.handle_response_status(response_status, response_data, parametro)

                    except KeyboardInterrupt:
                        self.handle_keyboard_interrupt()

                    except ValueError as e:
                        self.__info(str(e))  
                        continue

                    except Exception as e:
                        self.__info(str(e))  
                        continue
                    
            except Exception as e:
                self.__info(str(e))  
            return

    
            
    def __format_output(self, word, array):
        """
        Formata a palavra baseado na lista de codificação passada.

        Args:
            word (str): A palavra a ser formatada.
            array (list): A lista que contém as instruções da formatação.

        Returns:
            str: a string formatada.
        """
        if word and array:    
            output = ''
            for index, itens in enumerate(array):
                if itens == 2:
                    output += "\033[92m" + word[index] + "\033[0m"
                elif itens == 1:
                    output += "\033[93m" + word[index] + "\033[0m"
                else:
                    output += "\033[90m" + word[index] + "\033[0m"
                    
            return output
        else:
            return
