import socket
import json
import sys
from threading import Thread, Lock
from Server import Termo, Jogador
from utils import sumario_protocolo, server_config

class JogadorFactory:
    @staticmethod
    def criarJogadorAtivo(cliente, con) -> Jogador:
        jogador = Jogador(cliente, con)
        jogador.jogo = Termo()           
        return jogador

class Server:
    
    _instance = None
    
    def __init__(self):
        if Server._instance != None:
            raise Exception("Esta classe é um singleton!")
        
        else:
            Server._instance = self
            self.__HOST = '0.0.0.0'
            self.__TAM_MSG, self.__PORT = server_config()
            self.__protocolo = sumario_protocolo()
            self.__jogadoresAtivos = []
            self.__jogadoresAtivos_lock = Lock()
            # self.__parties = []
            # self.__parties_lock = Lock()
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.__sock.bind((self.__HOST, self.__PORT))
            except OSError:
                print("Não foi possível iniciar o servidor. Verifique se a porta está disponível.")
                sys.exit(1)
            self.__sock.listen(10)
            
    @classmethod
    def get_instance(cls):
        if cls._instance == None:
            cls._instance = Server()
        return cls._instance

    def __criarJogadorAtivo(self, cliente, con) -> Jogador:
        jogador = JogadorFactory.criarJogadorAtivo(cliente, con)
        
        with self.__jogadoresAtivos_lock: 
            self.__jogadoresAtivos.append(jogador)

        return jogador

    def __removerJogadorAtivo(self, cliente):
        for jogador in self.__jogadoresAtivos:
            if jogador.cliente == cliente:
                with self.__jogadoresAtivos_lock: 
                    self.__jogadoresAtivos.remove(jogador)
                return
            
        raise Exception()


    def __get_jogador_atual(self, cliente):
        for jogador in self.__jogadoresAtivos:
            if jogador.cliente == cliente:
                return jogador
        return None
    
    
    def __start_game(self, jogadorAtual, cliente, con):
        
        if jogadorAtual:  
            return {
                "code_status": self.__protocolo['JOGO_JA_INICIADO']
            }
        
        else:
            # Iniciar jogador
            jogadorAtual = self.__criarJogadorAtivo(cliente, con)
            return {
                "code_status": self.__protocolo['JOGO_INICIADO']
            }

    def __restart_game(self, cliente, con):
        try:
            self.__removerJogadorAtivo(cliente)     
            self.__criarJogadorAtivo(cliente, con)

            return {
                "code_status" : self.__protocolo['JOGO_REINICIADO'],
            }
        except Exception:
            return {
                "code_status" : self.__protocolo['JOGO_NAO_INICIADO'],
            }
            
    def __continue_game(self, jogadorAtual):
        if not jogadorAtual:
            return {
                "code_status" : self.__protocolo['JOGO_NAO_INICIADO'],
            }
        else:
            jogadorAtual.jogo.iniciarJogo()
            return {
                "code_status" : self.__protocolo['JOGO_CONTINUADO'],
            }
            
    def __exit_game(self, cliente):
        try:
            self.__removerJogadorAtivo(cliente)                            
            return {
                "code_status" : self.__protocolo['JOGO_ENCERRADO'],
            }
        except Exception:
            return {
                "code_status" : self.__protocolo['JOGO_NAO_INICIADO'],
            }
    
    def __check_word(self, jogadorAtual, parametro):
        if not jogadorAtual:
            return {
                "code_status" : self.__protocolo['JOGO_NAO_INICIADO'],
            }
        elif not parametro:
            return {
                "code_status" : self.__protocolo['NECESSARIO_PARAMETRO'],
            }
        else:
            feedback = jogadorAtual.jogo.checkWord(parametro)
            print(feedback)
            
            if isinstance(feedback,int):
                
                if feedback == 202:
                    jogadorAtual.addPontuacao()
                    return {
                        "code_status" : self.__protocolo['PALAVRA_CORRETA'],
                        "remaining_attempts" : jogadorAtual.jogo.qtdTentativasRestantes
                    
                    }
                
                else:
                    return {
                        "code_status" : feedback,
                        "remaining_attempts" : jogadorAtual.jogo.qtdTentativasRestantes
                    }
                    
            else:
                
                if jogadorAtual.jogo.qtdTentativasRestantes != 0: 
                
                    return {
                        "code_status" : self.__protocolo['PALAVRA_INCORRETA'],
                        "word_encoded" : feedback,
                        "remaining_attempts" : jogadorAtual.jogo.qtdTentativasRestantes
                    }
                    
                else:
                    
                    
                    return {
                        "code_status" : self.__protocolo['PALAVRA_INCORRETA'],
                        "word_encoded" : feedback,
                        "remaining_attempts" : jogadorAtual.jogo.qtdTentativasRestantes,
                        "secret_word" : jogadorAtual.jogo.palavra
                    }
                
    def __list_words(self, jogadorAtual):
        if not jogadorAtual:
            return {
                "code_status" : self.__protocolo['JOGO_NAO_INICIADO'],
            }
        else:
            return {
                "code_status" : self.__protocolo['LISTAR_PALAVRAS'],
            }
            
    def __comando_invalido(self, jogadorAtual):
        if jogadorAtual:
            return {
                "code_status" : self.__protocolo['COMANDO_INVALIDO'],
                "remaining_attempts" : jogadorAtual.jogo.qtdTentativasRestantes
            }
        else:
            return {
                "code_status" : self.__protocolo['COMANDO_INVALIDO'],
            }
        
    
    def processa_msg_cliente(self, msg, con, cliente):
        try:
            data = json.loads(msg.decode())  
            print(f'Conectei com',cliente, data)
            
            comando = data.get('comando').lower()
            parametro = data.get('parametro')

            jogadorAtual = self.__get_jogador_atual(cliente)

            match comando:
                case "start_game":
                    data = self.__start_game(jogadorAtual, cliente, con)
                
                case "restart_game":
                    data = self.__restart_game(cliente, con)
                    
                case "continue_game":
                    data = self.__continue_game(jogadorAtual)
                    
                case "exit_game":
                    data = self.__exit_game(cliente)
                    
                case "check_word":
                    data = self.__check_word(jogadorAtual, parametro)
                    
                case "list_words":
                    data = self.__list_words(jogadorAtual)
                    
                case _:
                    data = self.__comando_invalido(jogadorAtual)
            
            response = json.dumps(data)
            con.sendall(response.encode())
            
        except Exception as e:
            print(f"Erro ao processar mensagem do cliente: {e}")

    def handle_client(self, con, cliente):
        while True:
            try:
                msg = con.recv(self.__TAM_MSG)
                if not msg: break
                self.processa_msg_cliente(msg, con, cliente)
            except Exception as e:
                print(f"Erro ao lidar com o cliente: {e}")
                break
        con.close()
        
        
    def run(self):
        while True:
            try:
                con, cliente = self.__sock.accept()
                t = Thread(target=self.handle_client, args=(con, cliente))
                t.start()
            except Exception as e:
                print(f"Erro ao lidar com o cliente: {e}")