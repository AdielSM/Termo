# pylint: disable= E0611 C0103 W0718

from time import sleep, time
from threading import Thread, Lock
import socket
import json
import sys
import psutil
from zeroconf import ServiceInfo, Zeroconf, NonUniqueNameException

from Server import Player, Termo, TermoStatus, PlayerNotFoundException, SingletonException

from utils import summary_protocol, server_config


class PlayerFactory:
    """
    Classe responsável por criar um player ativo.

    Métodos:
        make_player_active(cliente, con, user_name): Cria um player ativo com base no cliente e conexão fornecidos.

    """
    @staticmethod
    def make_player_active(cliente, con, user_name) -> Player:
        """
        Cria um player ativo com base no cliente e conexão fornecidos.

        Args:
            cliente: O cliente associado ao player.
            con: A conexão associada ao player.

        Returns:
            Um objeto player ativo criado com base nosArgs fornecidos.
        """
        player = Player(cliente, con, user_name)
        player.game = Termo()
        return player


class Server:
    """
    Classe responsável por representar o servidor do jogo.

    Métodos:
        run(): Inicia a execução do servidor, aguardando a conexão de clientes e tratando 
        cada cliente em uma thread separada.
        get_instance(): Retorna a instância única da classe.
    """

    _instance = None

    def __init__(self):
        if Server._instance is not None:
            raise SingletonException("Esta classe é um Singleton!")

        Server._instance = self
        self.__HOST = '0.0.0.0'
        self.__TAM_MSG, self.__PORT = server_config()
        self.__protocol = summary_protocol()
        self.__zeroconf = Zeroconf()
        self.__active_players = []
        self.__active_players_lock = Lock()
        # self.__parties = []
        # self.__parties_lock = Lock()
        self.__last_msgs_clients = {}
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.__sock.bind((self.__HOST, self.__PORT))
        except OSError:
            try:
                # Tenta conexão em porta dinâmica
                self.__sock.bind((self.__HOST, 0))
                self.__PORT = self.__sock.getsockname()[1]
                print(f"Não foi possível iniciar o servidor. Tentando conexão na porta {self.__PORT}")
            except OSError:
                print('Não foi possível iniciar o servidor. Verifique sua conexão de rede e tente novamente')
                sys.exit(0)

        self.__sock.listen(10)
        Thread(target=self.__verify_time_last_msg).start()

    @classmethod
    def get_instance(cls) -> 'Server':
        """
        Retorna a instância única da classe.

        Args:
            cls (Server): A classe Server.
        
        Returns:
            Server: A instância única da classe.

        """
        if cls._instance is None:
            cls._instance = Server()
        return cls._instance


    def __verify_time_last_msg(self):
        while True:
            if self.__active_players:  
                current_time = time()
                clients_to_remove = []

                for player, last_msg_time in self.__last_msgs_clients.items():
                    if current_time - last_msg_time > 90:
                        clients_to_remove.append(player)

                if clients_to_remove:
                    for player in clients_to_remove:
                        if player is not None:
                            self.__remove_player_active(player.client)
                            print(f"Cliente {player.client} desconectado por inatividade")

            sleep(10)


    def __advertise_service(self):
        # Configuração do serviço
        local_ip = self.__get_active_network_interface_ip()
        print(f"Endereço IP local: {local_ip}")
        print(f"Porta: {self.__PORT}")

        local_ip = socket.inet_aton(local_ip)
        time_interval_sec = 3

        # Escolhe um nome para o servidor

        
        server_name = input("\nEscolha o nome para esse servidor ser encontrado> ")
        while server_name.strip() == "":
            server_name = input("\nEscolha um nome válido para esse servidor ser encontrado> ")

        try:
            info = ServiceInfo(f"Termo._{server_name}._server._tcp.local.",
                            "_server._tcp.local.", int(self.__PORT), addresses=[local_ip],
                            properties={"server_name": server_name})
            print(f"Anunciando o serviço a cada {time_interval_sec} segundo(s)")

            while True:
                self.__zeroconf.register_service(info)
                sleep(time_interval_sec)
                self.__zeroconf.unregister_all_services()
        except KeyboardInterrupt:
            sys.exit(0)
        except NonUniqueNameException:
            print("Erro ao anunciar o servidor, nome pode já estar em uso. Tente novamente")
            self.__advertise_service()
            

    def __get_active_network_interface_ip(self):
        """
        Obtém o endereço IP da interface de rede ativa que pertence a uma rede local.

        Returns:
            str: O endereço IP da interface de rede ativa.
        """
        try:
            # Obtém todas as interfaces de rede
            interfaces = psutil.net_if_addrs()

            # Procura por uma interface ativa que não seja 'lo' (loopback)
            for interface, addrs in interfaces.items():
                if interface != 'lo':
                    for addr in addrs:
                        if addr.family == socket.AF_INET:
                        # Verifica se o endereço IP está no intervalo 192.168.0.0/16 ou 10.0.0.0/8, fazendo parte de uma rede local
                            ip_parts = addr.address.split('.')
                            if ip_parts[0] == '10' or (ip_parts[0] == '192' and ip_parts[1] == '168'):
                                return addr.address

        except Exception as e:
            print(f"Erro ao obter endereço IP: {e}")

        return self.__HOST

    def __make_player_active(self, client, con, user_name) -> Player:
        """
        Cria um player ativo com base no cliente e conexão fornecidos.

        Args:
            cliente (Cliente): O cliente associado ao player.
            con (Conexao): A conexão associada ao player.

        Returns:
            Player: O player ativo criado.

        """
        player = PlayerFactory.make_player_active(client, con, user_name)

        with self.__active_players_lock:
            self.__active_players.append(player)

        return player

    def __remove_player_active(self, client):
        """
        Remove um player ativo com base no cliente fornecido.

        Args:
            cliente: O cliente do playera ser removido.

        Returns:
            PlayerNotFoundException: Se o player não for encontrado na lista de players ativos.
        """

        player = self.__get_current_player(client)

        if player and player in self.__active_players:
            with self.__active_players_lock:
                self.__active_players.remove(player)
                self.__last_msgs_clients.pop(player)
                player.con.close()
                return

        raise PlayerNotFoundException('Player não encontrado na lista de players ativos.')

    def __get_current_player(self, client):
        """
        Retorna o objeto player correspondente ao cliente fornecido.

        Args:
            cliente: O cliente para o qual se deseja obter o jogador correspondente.

        Returns:
            O objeto player correspondente ao cliente fornecido, ou None se não for encontrado.
        """
        for player in self.__active_players:
            if player.client == client:
                return player
        return None

    def __start_game(self, current_player, client, con, parameter):
        """
        Inicia um novo jogo para o jogador atual.

        Args:
            current_player (Player): O jogador atual.
            client (str): O cliente conectado.
            con (socket): O objeto de conexão do cliente.
            parameter (str): O parâmetro fornecido pelo cliente.

        Returns:
            dict: Um dicionário contendo o código de status da operação.
        """
        if current_player:
            return {
                "status_code": self.__protocol['JOGO_JA_INICIADO']
            }

        current_player = self.__make_player_active(client, con, parameter)
        return {
            "status_code": self.__protocol['JOGO_INICIADO']
        }

    def __restart_game(self, current_player):
        """
        Reinicia o jogo para o cliente especificado.

        Args:
            current_player (Player): O player atual.

        Returns:
            dict: Um dicionário contendo o código de status da operação.

        Raises:
            PlayerNotFoundException: Se o jogador não for encontrado.

        """
        try:
            current_player.restart()

            return {
                "status_code": self.__protocol['JOGO_REINICIADO'],
            }

        except AttributeError:
            return {
                "status_code": self.__protocol['JOGO_NAO_INICIADO'],
            }

    def __continue_game(self, current_player):
        """
        Continua o jogo para o player atual.

        Args:
            current_player: O player atual.

        Retorna:
            Um dicionário contendo o código de status da operação.
        """
        if not current_player:
            return {
                "status_code": self.__protocol['JOGO_NAO_INICIADO']
            }

        if current_player.game.game_status not in [TermoStatus.VICTORY, TermoStatus.DEFEAT]:
            return {
                "status_code": self.__protocol['JOGO_COM_TENTATIVAS_VALIDAS'],
                "remaining_attempts": current_player.game.remaining_attempts
            }

        current_player.game.start_game()
        return {
            "status_code" : self.__protocol['JOGO_CONTINUADO']
        }

    def __check_word(self, current_player, parameter):
        """
        Verifica se a palavra fornecida pelo player está correta ou incorreta.

        Args:
            current_player: O player atual.
            parameter: A palavra fornecida pelo player.
        
        Returns:
            Um dicionário contendo o código de status e outras informações relevantes,
            como a pontuação do player, 
            o número de tentativas restantes e a palavra secreta (caso o player tenha esgotado todas as tentativas).
        """

        if not current_player:
            return {
                "status_code": self.__protocol['JOGO_NAO_INICIADO'],
            }

        if not parameter:
            return {
                "status_code": self.__protocol['NECESSARIO_PARAMETRO'],
                "remaining_attempts": current_player.game.remaining_attempts
            }

        feedback = current_player.game.check_word(parameter)

        if not current_player.round_start_time:
            current_player.turn_start()

        if isinstance(feedback,int):

            if feedback == 201:
                current_player.add_score(current_player.game.remaining_attempts)

                return {
                    "status_code" : self.__protocol['PALAVRA_CORRETA'],
                    "remaining_attempts" : current_player.game.remaining_attempts,
                    "rounds_scores" : current_player.rounds_scores,
                    "total_score" : current_player.total_score
                }

            return {
                "status_code" : feedback,
                "remaining_attempts" : current_player.game.remaining_attempts
            }


        if current_player.game.remaining_attempts != 0:

            return {
                "status_code" : self.__protocol['PALAVRA_INCORRETA'],
                "word_encoded" : feedback,
                "remaining_attempts" : current_player.game.remaining_attempts
            }


        current_player.add_score(current_player.game.remaining_attempts)

        return {
            "status_code" : self.__protocol['FIM_DE_JOGO'],
            "word_encoded" : feedback,
            "remaining_attempts" : current_player.game.remaining_attempts,
            "secret_word" : current_player.game.secret_word,
            "rounds_scores" : current_player.rounds_scores,
            "total_score" : current_player.total_score
        }

    def __list_words(self, current_player):
        """
        Retorna um dicionário contendo o código de status para listar as palavras.

        Args:
            current_player: O player atual.

        Returns:
            Um dicionário contendo o código de status para listar as palavras.
        """

        if not current_player:
            return {
                "status_code": self.__protocol['JOGO_NAO_INICIADO'],
            }


        return {
            "status_code" : self.__protocol['LISTAR_PALAVRAS'],
        }


    def __invalid_command(self, current_player):
        """
        Função que retorna um dicionário com o código de status e, opcionalmente, 
        o número de tentativas restantes.

        Args:
            current_player (Player): O player atual.

        Returns:
            dict: Um dicionário contendo o código de status e, caso haja um jogo, 
            o número de tentativas restantes.
        """
        if current_player:
            return {
                "status_code": self.__protocol['COMANDO_INVALIDO'],
                "remaining_attempts": current_player.game.remaining_attempts
            }

        return {
            "status_code" : self.__protocol['COMANDO_INVALIDO'],
        }

    def __process_client_message(self, msg, con, client):
        """
        Processa a mensagem recebida do cliente.

        Args:
            msg (bytes): A mensagem recebida do cliente.
            con (socket): O objeto de conexão do cliente.
            client (str): O identificador do cliente.

        Returns:
            dict: Os dados de resposta a serem enviados ao cliente.

        Raises:
            Exception: Se ocorrer um erro ao processar a mensagem do cliente.
        """
        try:
            data = json.loads(msg.decode())
            print('Recebi de ', client, 'os comandos:', data)

            command = data.get('command').lower()
            parameter = data.get('parameter')

            current_player = self.__get_current_player(client)

            match command:
                case "start_game":
                    data = self.__start_game(current_player, client, con, parameter)

                case "restart_game":
                    data = self.__restart_game(current_player)

                case "continue_game":
                    data = self.__continue_game(current_player)

                case "check_word":
                    data = self.__check_word(current_player, parameter)

                case "list_words":
                    data = self.__list_words(current_player)

                case _:
                    data = self.__invalid_command(current_player)

            response = json.dumps(data)
            con.sendall(response.encode())

        except Exception as e:
            print(f"Erro ao processar mensagem do cliente: {e}")

    def handle_client(self, con, client):
        """
        Lida com um cliente conectado ao servidor.

        Args:
            con: objeto de conexão do cliente.
            client: informações do cliente conectado.

        Returns:
            None

        Raises:
            Exception: Se ocorrer um erro ao lidar com o cliente.
        
        """
        while True:
            try:
                msg = con.recv(self.__TAM_MSG)

                if not msg:
                    break

                self.__process_client_message(msg, con, client)

                with self.__active_players_lock:
                    self.__last_msgs_clients[self.__get_current_player(client)] = time()

            except OSError as e:
                if e.winerror == 10053:
                    print('')
                    break

            except Exception as e:
                print(f"Erro ao lidar com o cliente: {e}")
                break


    def run(self):
        """
        Inicia a execução do servidor, aguardando a conexão de clientes e tratando cada cliente 
        em uma thread separada.

        Args:
            None
        
        Returns:
            None

        Raises:
            Exception: Caso ocorra algum erro ao lidar com o cliente.

        """

        # Inicia anúncio do servidor na rede
        thread_advertise = Thread(target=self.__advertise_service)
        thread_advertise.start()
        while True:
            try:
                con, cliente = self.__sock.accept()
                print('Conectei com ', cliente)
                t = Thread(target=self.handle_client, args=(con, cliente))
                t.start()

            except KeyboardInterrupt:
                print("Servidor encerrado.")
                sys.exit(0)

            except Exception as e:
                print(f"Erro ao lidar com o cliente: {e}")