# pylint: disable= W0238 C0103 C0301

from threading import Lock, Thread
from time import sleep
from enum import Enum
from typing import Any, Dict, Tuple
import socket
import json
import sys
from zeroconf import Zeroconf
from prettytable import PrettyTable
from utils import server_config, LinkedStack, summary_protocol


class GameStatus(Enum):
    """
    Enum que representa o status de um jogo.

    Valores possíveis:
    - NO_CONNECTION: Sem conexão com o jogo.
    - NO_GAME: Sem jogo em andamento.
    - GAME_IN_PROGRESS: Jogo em andamento.
    - GAME_FINISHED: Jogo finalizado.
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
        self.__MSG_SIZE, _ = server_config()
        self.__sock: socket.socket = None
        self.__zeroconf = Zeroconf()
        self.__servers = {}
        self.__servers_Lock = Lock()
        self.__protocol = summary_protocol()
        self.__game_status: GameStatus = GameStatus.NO_CONNECTION
        self.__user_name: str = None
        self.__words_stack = LinkedStack()
        self.__table = PrettyTable()
        self.__scores_table = PrettyTable()
        self.__show_table = True

    def manage_servers_ttl(self):
        """
        Gerencia o tempo de vida dos servidores.

        Args:
            self: A instância da classe Client.

        Returns:
            None

        """
        while self.__game_status == GameStatus.NO_CONNECTION:
            with self.__servers_Lock:
                if not self.__servers:
                    sleep(3)
                    continue

                servers_to_remove = []
                for server in self.__servers.values():
                    if server["ttl"] == 0:
                        name_server = server['server'].properties.get(b'server_name').decode('utf-8')
                        servers_to_remove.append(name_server)
                    else:
                        server["ttl"] -= 1

                # Remove todos os servidores inativos
                for name_server in servers_to_remove:
                    del self.__servers[name_server]

            sleep(1)


    def __discover_servers(self):
        """
        Realiza a busca de novos servidores, adicionando a lista de servidores

        Args:
            self: A instância da classe Client.
            
        Raises:
            KeyboardInterrupt: Se o usuário interromper o programa.
            OSError: Se houver erro ao procurar o servidor com zeroconf

        """
        while self.__game_status == GameStatus.NO_CONNECTION:
            try:
                with self.__servers_Lock:
                    server = self.__zeroconf.get_service_info("Termo._server._tcp.local.", "_server._tcp.local.",timeout=5000)

                    if server:
                        self.__servers[server.properties.get(
                            b'server_name').decode('utf-8')] = {"server": server, "ttl": 5}
            except KeyboardInterrupt:
                sys.exit(0)
            except OSError:
                print("Erro ao procurar servidores disponíveis, tente novamente mais tarde.")

    def __show_servers(self):
        """
        Exibe a lista de servidores

        Args:
            self: A instância da classe Client.

        Returns:
            None
        """
        with self.__servers_Lock:
            print("\n")
            if not self.__servers:
                print("Nenhum servidor encontrado.")
                return

            print("\033[1mServidores disponíveis:\033[0m")
            for server in self.__servers.values():
                server_status = ""
                if server["ttl"] > 3:
                    server_status = "🟢"
                elif server["ttl"] > 1:
                    server_status = "🟡"
                else:
                    server_status = "🔴"

                print(f"{server_status}  Nome do Servidor: {server['server'].properties.get(b'server_name').decode('utf-8')}")
                print(f"  Endereço IP: {socket.inet_ntoa(server['server'].addresses[0])}")
                print(f"  Porta: {server['server'].port}")
                print()

    def __connect_to_server(self, host, port) -> socket.socket:
        """
        Estabelece uma conexão com o servidor.

        Args:
            self: A instância da classe Client.
            host: Endereço IP do servidor a se conectar
            port: Porta do servidor a se conectar

        Returns:
            socket.socket: O objeto de socket que representa a conexão estabelecida.

        Raises:
            socket.error: Se não for possível estabelecer a conexão 
            com o servidor após 5 tentativas.
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((host, port))
            self.__game_status = GameStatus.NO_GAME
            return sock
        except socket.error as err:
            print(str(err))

        raise socket.error(
            "Não foi possível conectar ao servidor. Tente reiniciar o cliente.")

    def __render_menu_table(self) -> None:
        """
        Renderiza uma tabela com as opções disponíveis para o usuário.

        Args:
            self: A referência para a instância da classe.

        Returns:
            None: Não há retorno.
            
        Raises:
            None: Não há exceções.
        
        """
        self.__table.clear_rows()
        self.__table.field_names = ["Opção", "Descrição"]
        self.__table.add_row(["start", "Começar um jogo"])
        self.__table.add_row(["ctrl + c", "Encerrar o jogo"])

        if self.__game_status != GameStatus.NO_GAME:
            self.__table.clear_rows()
            self.__table.field_names = ["Opção", "Descrição"]
            self.__table.add_row(["ctrl + c", "Encerrar o jogo"])
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
            self: A referência para a instância da classe.
            user_command (str): O comando fornecido pelo usuário.

        Returns:
            Tuple[str, Any]: Uma tupla contendo o comando e o parâmetro correspondente.

        Raises:
            ValueError: Se o comando fornecido pelo usuário for inválido.
        """
        if user_command == "start":
            command = "start_game"
            parameter = self.__user_name

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

            if len(user_command.strip()) == 0:
                raise ValueError("Comando inválido: Vazio")

            raise ValueError("Comando inválido:" + " " + user_command)

        return (command, parameter)

    def __send_requisition(self, req_body: Dict[str, Any]) -> Dict[str, Any]:
        """
        Envia uma requisição para o servidor.

        Args:
            self: A referência para a instância da classe.
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
        
        Args:
            self: A referência para a instância da classe.
        """
        print(f"\n{'=' * 50}\nBem vindo ao jogo de palavras Termo!\n{'=' * 50}")

    def __get_username(self) -> str:
        """
        Solicita ao usuário um nickname.

        Args:
            self: A referência para a instância da classe.
        """
        try:
            user_name = input("Digite seu nome de usuário: ")

            if user_name.strip() == "":
                return "Anônimo"

            return user_name
        except KeyboardInterrupt:
            print('\nPoxa, que pena que você não quis jogar :(')
            sys.exit(0)

    def __get_user_command(self) -> str:
        """
        Solicita ao usuário um comando.

        Args:
            self: A referência para a instância da classe.
        """
        return input('\nTermo> ')

    def __print_exit_message(self) -> None:
        """
        Exibe a mensagem de instrução para caso o jogador deseje encerrar o jogo.

        Args:
            self: A referência para a instância da classe.
        """
        state_to_show = "ocultar" if self.__show_table else "exibir"
        print()
        print(f"\033[90mDigite {Client.SHOW_TABLE_INPUT} para {state_to_show} a tabela de menu\033[0m")
        print("\033[90mPressione Ctrl + C para sair do jogo!\033[0m")

    def __print_end_game_message(self) -> None:
        """
        Exibe uma mensagem de fim de jogo.

        Args:
            self: A referência para a instância da classe.
        """
        print("\nA rodada acabou! Deseja continuar jogando?")

    def __print_goodbye_message(self) -> None:
        """
        Exibe uma mensagem de despedida.

        Args:
            self: A referência para a instância da classe.
        """
        print(f'\nAté a próxima, {self.__user_name}! Obrigado por jogar o Termo!')

    def __handle_keyboard_interrupt(self) -> None:
        """
        Lida com a interrupção do teclado.

        Fecha o socket e encerra o programa com uma mensagem.

        Args:
            self: A referência para a instância da classe.
        """
        print(f"\nObrigado por jogar, {self.__user_name}!\nFoi feito com ❤️  em 🐍\n")
        self.__close_client()

    def __create_request_body(self, command: str, parameter: Any) -> Dict[str, Any]:
        """
        Cria o corpo da requisição com base no comando e parâmetro fornecidos.

        Args:
            self: A referência para a instância da classe.
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

        Args:
            self: A referência para a instância da classe.

        Returns:
            str: A opção escolhida pelo usuário ('1' para continuar ou '2' para sair).
        """
        usr_input = input('Digite 1 para continuar ou 2 para sair: ')

        while usr_input not in ['1', '2']:
            usr_input = input('Digite uma opção válida (1/2): ')

        return usr_input

    def __return_attempts(self, remaining_attempts:int, status_code:int) -> str:
        """
        Retorna uma string com o número de tentativas restantes ou o número de tentativas até agora.

        Args:
            self: A referência para a instância da classe.
            remaining_attempts (int): O número de tentativas restantes.

        Returns:
            str: A string contendo o número de tentativas restantes ou o número de tentativas até agora.
        """
        if remaining_attempts >= 0 and status_code == self.__protocol['PALAVRA_CORRETA']:
            return '\033[1m' + f'Tentativas Restantes: {remaining_attempts - 1}' '\033[0m'

        if remaining_attempts >= 0:
            return '\033[1m' + f'Tentativas Restantes: {remaining_attempts}' '\033[0m'

        return f"Número de tentativas até agora: {len(self.__words_stack)}"

    def __check_exit_game(self, option) -> bool:
        """
        Verifica se o jogo deve ser encerrado com base na opção selecionada.

        Args:
            self: A referência para a instância da classe.
            option (str): A opção selecionada.

        Returns:
            bool: True se o jogo deve ser encerrado, False caso contrário.

        """
        if option == '1':
            self.__game_status = GameStatus.GAME_IN_PROGRESS
            return False

        self.__game_status = GameStatus.GAME_FINISHED
        return True

    def __close_client(self) -> None:
        self.__sock.close()
        sys.exit(0)


    def __game_continued_action(self) -> None:
        """
        Executa a ação de continuar o jogo.

        Envia uma requisição para o servidor solicitando a continuação do jogo.
        Caso a requisição seja bem-sucedida, renderiza a resposta do servidor.
        Caso contrário, exibe uma mensagem de erro.

        Args:
            self: A referência para a instância da classe.

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
            self: A referência para a instância da classe.
            word (str): A palavra a ser formatada.
            format_instructions (list): A lista que contém as instruções de formatação.

        Returns:
            str: A string formatada.
        """
        output = ''
        for index, items in enumerate(format_instructions):
            if items == 2:
                output += "\033[92m" + word[index] + "\033[0m"
            elif items == 1:
                output += "\033[93m" + word[index] + "\033[0m"
            else:
                output += "\033[90m" + word[index] + "\033[0m"

        return output


    def __secret_word_animation(self, word) -> None:
        """
        Realiza uma animação para exibir a palavra secreta.

        Args:
            self: A referência para a instância da classe.
            word (str): A palavra secreta a ser exibida.

        Returns:
            None
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
            self: A referência para a instância da classe.
            response_status (int): O status da resposta.
            **extra_info: Informações adicionais.

        Returns:
            None
        """
        if 200 <= response_status < 400:
            self.__handle_successful_cases(response_status, **extra_info)

        elif 400 <= response_status < 500:
            self.__handle_error_cases(response_status, **extra_info)

    def __handle_successful_cases(self, response_status, **extra_info):
        """
        Lida com os casos de sucesso com base no código de status da resposta.

        Args:
            self: A referência para a instância da classe.
            response_status (int): O código de status da resposta.
            **extra_info: Informações adicionais passadas como argumentos de palavra-chave.

        Returns:
            None

        """
        remaining_attempts = extra_info.get("remaining_attempts")
        format_output = extra_info.get("format_output")
        secret_word = extra_info.get("secret_word")
        player_name = extra_info.get("player_name")

        if response_status == self.__protocol['JOGO_INICIADO']:
            print("Jogo Iniciado com Sucesso")
            print("\n\033[1mTutorial básico:\033[0m")
            print("\033[90ma\033[0m - Letra não faz parte da palavra")
            print("\033[93ma\033[0m - Letra faz parte da palavra, mas em outra posição")
            print("\033[92ma\033[0m - Letra faz parte da palavra nessa posição")
            print("\033[90mPara mais informações, acesse: \033[4mhttps://adielsm.github.io/Termo/\033[0m")

            print("Bom jogo!\n")

        if response_status == self.__protocol['PALAVRA_CORRETA']:
            print(f'\n🏆 Parabéns! Palavra Correta! 😎\nLista de Palavras Anteriores:\n{(self.__words_stack)}\n{self.__return_attempts(remaining_attempts, response_status)}')
            self.__render_score_table(extra_info.get("rounds_scores"), extra_info.get("total_score"))
            self.__words_stack.clear()

        if response_status == self.__protocol['PALAVRA_INCORRETA']:
            self.__words_stack.stack_up(format_output)
            print(f"\nPalavra Incorreta!\n{format_output}\n{self.__return_attempts(remaining_attempts, response_status)}")

        if response_status == self.__protocol['LISTAR_PALAVRAS']:
            if self.__words_stack:
                print(f"Lista de Palavras:\n{self.__words_stack}")
            else:
                print("Não há palavras inseridas nesta rodada!")

        if response_status == self.__protocol['JOGO_REINICIADO']:
            print("Jogo reiniciado com sucesso")
            self.__words_stack.clear()

        if response_status == self.__protocol['JOGO_CONTINUADO']:
            print(f"Jogo Continuado com Sucesso, Boa Sorte na Próxima Rodada {player_name}!")

        if response_status == self.__protocol['FIM_DE_JOGO']:
            self.__words_stack.stack_up(format_output)
            print(f"\nPalavra Incorreta!\n{format_output}\n{self.__return_attempts(remaining_attempts, response_status)}")

            self.__words_stack.clear()
            self.__secret_word_animation(secret_word)
            self.__render_score_table(extra_info.get("rounds_scores"), extra_info.get("total_score"))


    def __handle_error_cases(self, response_status, **remaining_attempts):
        """
        Manipula os casos de erro de resposta do servidor.

        Args:
            self: A referência para a instância da classe.
            response_status (int): O código de status da resposta.
            remaining_attempts (dict): Dicionário contendo as tentativas restantes.
        
        Returns:
            None

        """
        remaining_attempts = remaining_attempts.get("remaining_attempts")

        if response_status == self.__protocol['JOGO_JA_INICIADO']:
            print("Jogo já iniciado")

        elif response_status == self.__protocol['JOGO_NAO_INICIADO']:
            print("Jogo não iniciado")

        elif response_status == self.__protocol['NECESSARIO_PARAMETRO']:
            print(f"É necessário digitar uma palavra\n{self.__return_attempts(remaining_attempts, response_status)}")

        elif response_status == self.__protocol['TAMANHO_INCORRETO']:
            print(f"A palavra deve ter 5 letras\n{self.__return_attempts(remaining_attempts, response_status)}")

        elif response_status == self.__protocol['PALAVRA_INEXISTENTE']:
            print(f'A palavra não existe no dicionário\n{self.__return_attempts(remaining_attempts, response_status)}')

        elif response_status == self.__protocol['PALAVRA_REPETIDA']:
            print(f'Palavra já utilizada\n{self.__return_attempts(remaining_attempts, response_status)}')

        elif response_status == self.__protocol['JOGO_COM_TENTATIVAS_VALIDAS']:
            print(f'Jogo não pode ser continuado por conter tentátivas válidas! \n{self.__return_attempts(remaining_attempts, response_status)}')

        elif response_status == self.__protocol['COMANDO_INVALIDO']:
            print("\033[91m Comando inválido\033[0m")
            if remaining_attempts:
                print(f'{self.__return_attempts(remaining_attempts, response_status)}')
        else:
            print("Erro desconhecido, tente novamente!")


    def __handle_response_status(self, response_status: int, response_data: Dict[str, Any], parameter: Any) -> None:
        """
        Trata o status de resposta recebido do servidor.

        Args:
            self: A referência para a instância da classe.
            response_status (int): O código de status da resposta.
            response_data (Dict[str, Any]): Os dados de resposta recebidos do servidor.
            parameter (Any): Um parâmetro adicional.

        Returns:
            None

        """
        remaining_attempts = response_data.get("remaining_attempts")
        if response_status == self.__protocol['JOGO_INICIADO']:
            self.__render_response(response_status)
            self.__game_status = GameStatus.GAME_IN_PROGRESS

        elif response_status == self.__protocol['PALAVRA_CORRETA']:
            self.__render_response(response_status, remaining_attempts=remaining_attempts, rounds_scores=response_data["rounds_scores"], total_score=response_data["total_score"])

            self.__print_end_game_message()
            option = self.__get_user_end_game_option()

            if self.__check_exit_game(option):
                self.__print_goodbye_message()
                self.__close_client()


            self.__game_continued_action()

        elif response_status == self.__protocol['PALAVRA_INCORRETA']:
            color_str = self.__format_output(
                parameter, response_data["word_encoded"])
            self.__render_response(
                response_status, format_output=color_str, remaining_attempts=remaining_attempts)

        elif response_status == self.__protocol['JOGO_CONTINUADO']:
            self.__render_response(
                response_status, player_name=self.__user_name)

        elif response_status == self.__protocol['FIM_DE_JOGO']:
            color_str = self.__format_output(
                parameter, response_data["word_encoded"])

            self.__render_response(response_status, format_output=color_str, secret_word=response_data["secret_word"], rounds_scores=response_data["rounds_scores"], total_score=response_data["total_score"], remaining_attempts=remaining_attempts)

            self.__print_end_game_message()
            option = self.__get_user_end_game_option()

            if self.__check_exit_game(option):
                self.__print_goodbye_message()
                self.__close_client()

            self.__game_continued_action()
        else:
            self.__render_response(
                response_status, remaining_attempts=remaining_attempts)

    def run(self) -> None:
        """
        Executa o cliente do jogo.

        Raises:
            Inicializa as threads de monitoramento de servidores ativos e gerenciamento de tempo de vida dos servidores.
            Solicita ao usuário o nome do servidor ao qual deseja se conectar.
            Realiza a conexão com o servidor e exibe uma mensagem de boas-vindas.
            Solicita o nome do usuário e inicia um loop para processar os comandos do usuário.
            Trata exceções como interrupção do teclado, desconexão do servidor e erros genéricos.

        Returns:
            None
        """
        try:
            # Inicializa a thread de monitoramento de servidores ativos
            thread_discover_servers = Thread(target=self.__discover_servers)
            thread_discover_servers.start()

            # Inicializa a thread de gerenciamento de tempo de vida dos servidores, que roda a cada 1s
            thread_manage_servers_ttl = Thread(target=self.manage_servers_ttl)
            thread_manage_servers_ttl.start()

            print("\033[90mProcurando servidores, aguarde um instante...\033[0m\n")
            sleep(3)

            name_server = ""
            while not name_server:
                try:
                    self.__show_servers()
                    print(
                        "\033[90mAperte ENTER para atualizar a lista de servidores\033[0m")
                    name_server = input("\nDigite o nome do servidor> ")

                    if not name_server:
                        continue

                    server = self.__servers.get(name_server)
                    if server:
                        host, port = socket.inet_ntoa(server["server"].addresses[0]), server["server"].port
                        self.__sock = self.__connect_to_server(host, port)
                    else:
                        print(
                            "Servidor não encontrado. Verifique se o servidor está ativo e tente novamente.")
                        name_server = ""
                except KeyboardInterrupt:
                    self.__close_client()
                    print('\nPoxa, que pena que você não quis jogar :(')
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

                except OSError:
                    print("Você foi desconectado do servidor. Servidor está offline ou você ficou inativo por 90 segundos.")
                    self.__sock.close()
                    sys.exit(0)

                except ValueError as e:
                    print(str(e))
                    continue

                except Exception as e:
                    print(str(e))
                    continue

        except KeyboardInterrupt:
            print('\nPoxa, que pena que você não quis jogar :(')
            sys.exit(0)

        except OSError:
            print("Você foi desconectado do servidor. Servidor está offline ou você ficou inativo por 90 segundos.")
            self.__sock.close()
            sys.exit(0)

        except Exception as e:
            print(str(e))