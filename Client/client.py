# pylint: disable= W0238 C0103 C0301

from zeroconf import Zeroconf
from threading import Lock, Thread
from time import sleep
from enum import Enum
from typing import Any, Dict, Tuple
import socket
import json
import sys
from prettytable import PrettyTable

from utils import server_config, LinkedStack


class GameStatus(Enum):
    """
    Classe Enum que representa o status de um jogo.
    """
    NO_CONNECTION = 0
    NO_GAME = 1
    GAME_IN_PROGRESS = 2
    GAME_FINISHED = 3


class Client:
    """
        Inicializa a classe Client.
    """

    SHOW_TABLE_INPUT = "TABELA"

    def __init__(self) -> None:
        self.__HOST: str = '127.0.0.1'
        self.__MSG_SIZE, self.__PORT = server_config()
        self.__sock: socket.socket = None
        self.__zeroconf = Zeroconf()
        self.__servers = {}
        self.__servers_Lock = Lock()
        self.__game_status: GameStatus = GameStatus.NO_CONNECTION
        self.__user_name: str = None
        self.__words_stack = LinkedStack()
        self.__table = PrettyTable()
        self.__scores_table = PrettyTable()
        self.__show_table = True

    def __discover_servers(self):
        # Descobrir serviços
        while self.__game_status == GameStatus.NO_CONNECTION:
            try:
                with self.__servers_Lock:
                    server = self.__zeroconf.get_service_info("Termo._server._tcp.local.", "_server._tcp.local.",
                                                          timeout=5000)

                self.__servers_Lock.acquire()
                if server:
                    self.__servers[server.properties.get(
                        b'server_name').decode('utf-8')] = {"server": server}
                self.__servers_Lock.release()
                # sleep(2)
                # for server in self.__servers.items():
                #     if server["ttl"] == 0:
                #         name_server = self.__servers[server.properties.get(
                #         b'server_name').decode('utf-8')]
                #         del self.__servers[name_server]
                #     else:
                #         server["ttl"] -= 1
                # self.__servers_Lock.release()
            except KeyboardInterrupt:
                sys.exit(0)
            except Exception as e:
                print(e)
                print(
                    "Erro ao procurar servidores disponíveis, tente novamente mais tarde.")

    def __show_servers(self):
        self.__servers_Lock.acquire()
        if self.__servers == {}:
            print("Nenhum servidor encontrado.")
            return

        print("Servidores disponíveis:")
        for server in self.__servers.values():
            # server_status = ""
            # if server["ttl"] > 3:
            #     server_status = "🟢"
            # elif server["ttl"] >= 1:
            #     server_status = "🟡"
            # elif server["ttl"] == 0:
            #     server_status = "🔴"

            print(f"  Nome do Servidor: {
                server['server'].properties.get(b'server_name').decode('utf-8')}")
            print(f"  Endereço IP: {socket.inet_ntoa(
                server['server'].addresses[0])}")
            print(f"  Porta: {server['server'].port}")
        self.__servers_Lock.release()

    def __connect_to_server(self):
        """
        Estabelece uma conexão com o servidor.

        Args:
            self: A instância da classe Client.

        Returns:
            socket.socket: O objeto de socket que representa a conexão estabelecida.

        Raises:
            socket.error: Se não for possível estabelecer a conexão 
            com o servidor após 5 tentativas.
        """
        name_server = ""
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        thread_discover_servers = Thread(target=self.__discover_servers)
        thread_discover_servers.start()
        sleep(3)
        while not name_server:
            try:
                print(
                    "\033[90mAperte ENTER para atualizar a lista de servidores\033[0m")
                self.__show_servers()
                name_server = input("Digite o nome do servidor: ")

                if not name_server:
                    continue

                server = self.__servers.get(name_server)
                if server:
                    self.__sock.connect(
                        (socket.inet_ntoa(server["server"].addresses[0]), server["server"].port))
                    self.__game_status = GameStatus.NO_GAME
                    break
                else:
                    raise socket.error(
                        "Servidor não encontrado. Verifique se o servidor está ativo e tente novamente.")
            except socket.error as err:
                print(str(err))
                continue
            except KeyboardInterrupt:
                print("Encerrando o Termo!")
                exit(0)

        raise socket.error(
            "Não foi possível conectar ao servidor. Tente reiniciar o cliente.")

    def __render_menu_table(self) -> None:
        """
        Renderiza uma tabela com as opções disponíveis para o usuário.

        Args:
            self: A referência para a instância da classe.

        """
        self.__table.clear_rows()
        self.__table.field_names = ["Opção", "Descrição"]
        self.__table.add_row(["start", "Começar um jogo"])
        self.__table.add_row(["stop", "Encerrar jogo atual"])

        if self.__game_status != GameStatus.NO_GAME:
            self.__table.add_row(["try", "Tentar acertar a palavra secreta"])
            self.__table.add_row(
                ["list", "Listar palavras digitadas nesta rodada"])
            self.__table.add_row(["reset", "Reiniciar o jogo atual"])

        self.__table.align["Opção"] = "l"
        self.__table.align["Descrição"] = "l"

        print(self.__table)

    def __render_score_table(self, rounds_scores: dict, total_score: float) -> str:
        """
        Renderiza uma tabela com os scores das rodadas.

        Args:
            self: A referência para a instância da classe.

        """
        self.__scores_table.clear_rows()
        self.__scores_table.title = f"Pontuação de {self.__user_name}"
        self.__scores_table.field_names = list(rounds_scores.keys())
        self.__scores_table.add_row(list(rounds_scores.values()))
        self.__scores_table.add_column("Pontuação Total", [total_score])

        self.__scores_table.align["Rodada"] = "c"
        self.__scores_table.align["Pontuação Total"] = "c"

        print("")
        print(self.__scores_table)

    def __process_user_command(self, user_command: str) -> Tuple[str, Any]:
        """
        Processa o comando do usuário e retorna uma tupla contendo 
        o comando e o parâmetro correspondente.

        Args:
            user_command (str): O comando fornecido pelo usuário.

        Returns:
            Tuple[str, Any]: Uma tupla contendo o comando e o parâmetro correspondente.

        Raises:
            ValueError: Se o comando fornecido pelo usuário for inválido.
        """
        if user_command == "start":
            command = "start_game"
            parameter = self.__user_name

        elif user_command == "stop":
            command = "exit_game"
            parameter = None

        elif user_command == "try" and self.__game_status == GameStatus.GAME_IN_PROGRESS:
            command = "check_word"
            user_input = input('Digite uma palavra: ')
            parameter = user_input.lower()

        elif user_command == "list" and self.__game_status == GameStatus.GAME_IN_PROGRESS:
            command = "list_words"
            parameter = None

        elif user_command == "reset" and self.__game_status == GameStatus.GAME_IN_PROGRESS:
            command = "restart_game"
            parameter = self.__user_name

        else:
            raise ValueError("Comando inválido:" + " " + user_command)

        return (command, parameter)

    def __send_requisition(self, req_body: Dict[str, Any]) -> Dict[str, Any]:
        """
        Envia uma requisição para o servidor.

        Args:
            req_body (Dict[str, Any]): O corpo da requisição em formato de dicionário.

        Returns:
            Dict[str, Any]: Os dados da resposta do servidor em formato de dicionário.

        Raises:
            OSError: Se ocorrer um erro ao enviar ou receber dados pelo socket.
            json.JSONDecodeError: Se ocorrer um erro ao decodificar a resposta do servidor.
        """
        json_data = json.dumps(req_body)
        self.__sock.sendall(json_data.encode())

        response = self.__sock.recv(self.__MSG_SIZE)
        response_data = json.loads(response)
        return response_data

    def __print_welcome_message(self) -> None:
        """
        Exibe uma mensagem de boas-vindas.
        """
        print(f"\n{'=' * 50}\nBem vindo ao jogo de palavras Termo!\n{'=' * 50}")

    def __get_username(self) -> str:
        """
        Solicita ao usuário um nickname.
        """
        user_name = input("Digite seu nome de usuário: ")

        if user_name.strip() == "":
            return "Anônimo"

        return user_name

    def __get_user_command(self) -> str:
        """
        Solicita ao usuário um comando.
        """
        return input('\nTermo> ')

    def __print_exit_message(self) -> None:
        """
        Exibe a mensagem de instrução para caso o jogador deseje encerrar o jogo.
        """
        state_to_show = "ocultar" if self.__show_table else "exibir"
        print()
        print(f"\033[90mDigite {Client.SHOW_TABLE_INPUT} para {
              state_to_show} a tabela de menu\033[0m")
        print("\033[90mPressione Ctrl + C para sair do jogo!\033[0m")

    def __print_end_game_message(self) -> None:
        """
        Exibe uma mensagem de fim de jogo.
        """
        print("\nA rodada acabou! Deseja continuar jogando?")

    def __print_goodbye_message(self) -> None:
        """
        Exibe uma mensagem de despedida.
        """
        print(f'\nAté a próxima, {
              self.__user_name}! Obrigado por jogar o Termo!')

    def __handle_keyboard_interrupt(self) -> None:
        """
        Lida com a interrupção do teclado.

        Fecha o socket e encerra o programa com uma mensagem.

        """
        print(f"\nObrigado por jogar, {
              self.__user_name}!\n Foi feito com ❤️  em 🐍\n")
        self.__sock.close()
        sys.exit(0)

    def __create_request_body(self, command: str, parameter: Any) -> Dict[str, Any]:
        """
        Cria o corpo da requisição com base no comando e parâmetro fornecidos.

        Args:
            command (str): O comando da requisição.
            parameter (Any): O parâmetro da requisição.

        Returns:
            Dict[str, Any]: O corpo da requisição.
        """
        return {
            "command": command,
            "parameter": parameter
        }

    def __get_user_end_game_option(self) -> str:
        """
        Solicita ao usuário a opção de continuar ou sair do jogo.

        Returns:
            str: A opção escolhida pelo usuário ('1' para continuar ou '2' para sair).
        """
        usr_input = input('Digite 1 para continuar ou 2 para sair: ')

        while usr_input not in ['1', '2']:
            usr_input = input('Digite uma opção válida (1/2): ')

        return usr_input

    def __return_attempts(self, remaining_attempts, status_code) -> str:
        """
        Retorna uma string com o número de tentativas restantes ou o número de tentativas até agora.

        Args:
            remaining_attempts (int): O número de tentativas restantes.

        Returns:
            str: A string contendo o número de tentativas restantes ou o número de tentativas até agora.
        """
        if remaining_attempts >= 0 and status_code == 202:
            return f"Tentativas Restantes: {(remaining_attempts) - 1}"

        elif remaining_attempts >= 0:
            return f"Tentativas Restantes: {remaining_attempts}"

        return f"Número de tentativas até agora: {len(self.__words_stack)}"

    def __check_exit_game(self, option) -> bool:
        """
        Verifica se o jogo deve ser encerrado com base na opção selecionada.

        Args:
            option (str): A opção selecionada.

        Returns:
            bool: True se o jogo deve ser encerrado, False caso contrário.

        """
        if option == '1':
            self.__game_status = GameStatus.GAME_IN_PROGRESS
            return False

        self.__game_status = GameStatus.GAME_FINISHED
        return True

    def __game_continued_action(self) -> None:
        """
        Executa a ação de continuar o jogo.

        Envia uma requisição para o servidor solicitando a continuação do jogo.
        Caso a requisição seja bem-sucedida, renderiza a resposta do servidor.
        Caso contrário, exibe uma mensagem de erro.

        Raises:
            OSError: Ocorre quando há um erro ao enviar ou receber dados pelo socket.
            json.JSONDecodeError: Ocorre quando há um erro ao decodificar a resposta do servidor.
        """
        req_body = {
            "command": "continue_game",
            "parameter": None
        }

        for _ in range(3):
            try:
                response_data = self.__send_requisition(req_body)
                response_status = response_data["status_code"]

                self.__render_response(
                    response_status, player_name=self.__user_name)
                return

            except OSError:
                print("Ocorreu um erro ao enviar ou receber dados pelo socket.")

            except json.JSONDecodeError:
                print("Ocorreu um erro ao decodificar a resposta do servidor.")

        print("Ocorreu um erro ao continuar o jogo. Por favor, considere reiniciar")

    def __format_output(self, word, format_instructions) -> str:
        """
        Formata a palavra com base na lista de codificação fornecida.

        Args:
            word (str): A palavra a ser formatada.
            format_instructions (list): A lista que contém as instruções de formatação.

        Returns:
            str: A string formatada.
        """
        if word and format_instructions:
            output = ''
            for index, items in enumerate(format_instructions):
                if items == 2:
                    output += "\033[92m" + word[index] + "\033[0m"
                elif items == 1:
                    output += "\033[93m" + word[index] + "\033[0m"
                else:
                    output += "\033[90m" + word[index] + "\033[0m"

            return output

        return

    def __secret_word_animation(self, word) -> None:
        """
        Realiza uma animação para exibir a palavra secreta.

        Args:
            word (str): A palavra secreta a ser exibida.

        """
        transformed_word = ['_' for _ in word]

        print("Você não conseguiu acertar a palavra secreta!\nA palavra era:\n")

        for i, char in enumerate(word):
            transformed_word[i] = char
            print(''.join(transformed_word))
            sleep(1)

    def __render_response(self, response_status: int, **extra_info):
        """
        Renderiza a resposta com base no status recebido.

        Args:
            response_status (int): O status da resposta.
            **extra_info: Informações adicionais.


        """
        if 200 <= response_status < 400:
            self.__handle_successful_cases(response_status, **extra_info)

        elif 400 <= response_status < 500:
            self.__handle_error_cases(response_status, **extra_info)

    def __handle_successful_cases(self, response_status, **extra_info):
        """
        Lida com os casos de sucesso com base no código de status da resposta.

        Args:
            response_status (int): O código de status da resposta.
            **extra_info: Informações adicionais passadas como argumentos de palavra-chave.

        """
        remaining_attempts = extra_info.get("remaining_attempts")
        format_output = extra_info.get("format_output")
        secret_word = extra_info.get("secret_word")
        player_name = extra_info.get("player_name")

        match response_status:
            case 200:
                print("Jogo Iniciado com Sucesso")
                print("\n\033[1mTutorial básico:\033[0m")
                print("\033[90ma\033[0m - Letra não faz parte da palavra")
                print(
                    "\033[93ma\033[0m - Letra faz parte da palavra, mas em outra posição")
                print(
                    "\033[92ma\033[0m - Letra faz parte da palavra nessa posição")
                print("Bom jogo!\n")

            case 201:
                print("Jogo Finalizado com Sucesso")

            case 202:
                print(f'\n🏆 Parabéns! Palavra Correta! 😎\nLista de Palavras Anteriores:\
                      n{(self.__words_stack)}\n{self.__return_attempts(remaining_attempts, response_status)}')
                self.__render_score_table(extra_info.get(
                    "rounds_scores"), extra_info.get("total_score"))
                self.__words_stack.clear()

            case 203:
                self.__words_stack.stack_up(format_output)
                print(f"\nPalavra Incorreta!\n{format_output}\n{
                      self.__return_attempts(remaining_attempts, response_status)}")

            case 204:
                if self.__words_stack:
                    print(f"Lista de Palavras:\n{self.__words_stack}")
                else:
                    print("Não há palavras inseridas nesta rodada!")

            case 205:
                print("Jogo reiniciado com sucesso")
                self.__words_stack.clear()

            case 206:
                print(f"Jogo Continuado com Sucesso, Boa Sorte na Próxima Rodada {
                      player_name}!")

            case 207:
                self.__words_stack.stack_up(format_output)
                print(f"\nPalavra Incorreta!\n{format_output}\n{
                      self.__return_attempts(remaining_attempts, response_status)}")

                self.__words_stack.clear()
                self.__secret_word_animation(secret_word)
                self.__render_score_table(extra_info.get(
                    "rounds_scores"), extra_info.get("total_score"))

    def __handle_error_cases(self, response_status, **remaining_attempts):
        """
        Manipula os casos de erro de resposta do servidor.

        Args:
            response_status (int): O código de status da resposta.
            remaining_attempts (dict): Dicionário contendo as tentativas restantes.

        """
        remaining_attempts = remaining_attempts.get("remaining_attempts")

        match response_status:
            case 400:
                print("Jogo já iniciado")

            case 401:
                print("Jogo não iniciado")

            case 402:
                print(f"É necessário digitar uma palavra\n{
                      self.__return_attempts(remaining_attempts, response_status)}")

            case 403:
                print(f"A palavra deve ter 5 letras\n{
                      self.__return_attempts(remaining_attempts, response_status)}")

            case 404:
                print(f'A palavra não existe no dicionário\n{
                      self.__return_attempts(remaining_attempts, response_status)}')

            case 405:
                print(f'Palavra já utilizada\n{self.__return_attempts(
                    remaining_attempts, response_status)}')

            case 499:
                print("\033[91m Comando inválido\033[0m")

                if remaining_attempts:
                    print(f'{self.__return_attempts(
                        remaining_attempts, response_status)}')

    def __handle_response_status(self, response_status: int, response_data: Dict[str, Any], parameter: Any) -> None:
        """
        Trata o status de resposta recebido do servidor.

        Args:
            response_status (int): O código de status da resposta HTTP.
            response_data (Dict[str, Any]): Os dados de resposta recebidos do servidor.
            parameter (Any): Um parâmetro adicional.

        """
        remaining_attempts = response_data.get("remaining_attempts")
        if response_status == 200:
            self.__render_response(response_status)
            self.__game_status = GameStatus.GAME_IN_PROGRESS

        elif response_status == 201:
            self.__render_response(response_status)
            self.__game_status = GameStatus.NO_GAME

        elif response_status == 202:
            self.__render_response(response_status, remaining_attempts=remaining_attempts,
                                   rounds_scores=response_data["rounds_scores"], total_score=response_data["total_score"])

            self.__print_end_game_message()
            option = self.__get_user_end_game_option()

            if self.__check_exit_game(option):
                self.__print_goodbye_message()
                self.__sock.close()
                sys.exit(0)

            self.__game_continued_action()

        elif response_status == 203:
            color_str = self.__format_output(
                parameter, response_data["word_encoded"])
            self.__render_response(
                response_status, format_output=color_str, remaining_attempts=remaining_attempts)

        elif response_status == 206:
            self.__render_response(
                response_status, player_name=self.__user_name)

        elif response_status == 207:
            color_str = self.__format_output(
                parameter, response_data["word_encoded"])

            self.__render_response(response_status, format_output=color_str, secret_word=response_data["secret_word"], rounds_scores=response_data[
                                   "rounds_scores"], total_score=response_data["total_score"], remaining_attempts=remaining_attempts)

            self.__print_end_game_message()
            option = self.__get_user_end_game_option()

            if self.__check_exit_game(option):
                self.__print_goodbye_message()
                self.__sock.close()
                sys.exit(0)

            self.__game_continued_action()
        else:
            self.__render_response(
                response_status, remaining_attempts=remaining_attempts)

    def run(self) -> None:
        """
        Executa a aplicação cliente.

        Este método estabelece uma conexão com o servidor, solicita ao usuário um nome de usuário
        e entra em um loop onde exibe uma tabela, solicita ao usuário um comando, envia
        o comando para o servidor e trata a resposta.

        Raises:
            KeyboardInterrupt: Se o usuário interromper o programa.
            ValueError: Se um valor inválido for inserido pelo usuário.
            Exception: Se ocorrer qualquer outra exceção.
        """
        try:
            self.__sock = self.__connect_to_server()
            self.__print_welcome_message()
            self.__user_name = self.__get_username()

            while True:
                try:
                    if self.__show_table:
                        self.__render_menu_table()
                    self.__print_exit_message()
                    user_cmd = self.__get_user_command()

                    if user_cmd.strip().upper() == Client.SHOW_TABLE_INPUT:
                        self.__show_table = not self.__show_table
                        print()
                        continue

                    command, parameter = self.__process_user_command(user_cmd)
                    req_body = self.__create_request_body(command, parameter)

                    response_data = self.__send_requisition(req_body)
                    response_status = response_data["status_code"]

                    self.__handle_response_status(
                        response_status, response_data, parameter)

                except KeyboardInterrupt:
                    self.__handle_keyboard_interrupt()

                except ValueError as e:
                    print(str(e))
                    continue

                except Exception as e:
                    print(str(e))
                    continue

        except Exception as e:
            print(str(e))
        return
