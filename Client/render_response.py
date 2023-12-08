from time import sleep
from utils import PilhaSequencial

pilhaPalavras = PilhaSequencial()

def render_response(data, format_output = None, **kwargs):
    """
    Função responsável por renderizar a resposta do servidor.

    Parâmetros:
    - data: O código de resposta do servidor.
    - format_output: A saída formatada a ser exibida.
    - **kwargs: Argumentos adicionais.

    Retorna:
    Nenhum valor de retorno.
    """
    
    remaining_attemps = kwargs.get("remaining_attemps")
    if remaining_attemps:
        remaining_attemps = "Tentativas Restantes: " + str(remaining_attemps) + "\n"
    else:
        remaining_attemps = ''
    
    match data:
        case 200:
            print("Jogo Iniciado com Sucesso")
            print(remaining_attemps)
            
        case 201:
            print("Jogo Encerrado com Sucesso")
            print(remaining_attemps)
            
        case 202:
            #toDo melhorar resposta de palavra correta
            print("🏆 Parabéns! Palavra Correta! 😎")
            print("Lista de Palavras Anteriores:")
            print(pilhaPalavras)
            print(remaining_attemps)
            
        case 203:
            pilhaPalavras.empilha(format_output)
            print('')
            print("Palavra Incorreta!")
            
            print(format_output)
            print('')
            print(remaining_attemps)


            if kwargs["remaining_attemps"] == 0:
                print('')
                secret_word_animation(kwargs["secret_word"])
                
        case 204:
            print("Lista de Palavras:")
            print(pilhaPalavras)
            print(remaining_attemps)
            
        case 205:
            print('Jogo Reiniciado com Sucesso')
            print(remaining_attemps)
            
        case 206:
            player_name = kwargs['player_name']
            print(f'Jogo Continuado com Sucesso, Boa Sorte na Próxima Rodada {player_name} !')
            
        case 400:
            print("Jogo já iniciado")
            print(remaining_attemps)
            
        case 401:
            print("Jogo não iniciado")
            print(remaining_attemps)
            
            
        case 402:
            print("Necessário Forcener uma Palavra")
            print(remaining_attemps)

            
        case 403:
            print("A palavra deve conter 5 letras")
            print(remaining_attemps)

            
        case 404:
            print("Palavra inexiste no dicionário")
            print(remaining_attemps)

            
        case 405:
            print("Palavra já utilizada")
            print(remaining_attemps)
            
        case 499:
            print("Comando Inválido")
            print(remaining_attemps)
            

def secret_word_animation(palavra) -> None:
    palavra_transformada = ['_' for _ in palavra]
    
    print('Você não conseguiu adivinhar a palavra secreta!')
    print('A palavra era:')
    
    for i in range(len(palavra)):
        palavra_transformada[i] = palavra[i]
        print(''.join(palavra_transformada))
        sleep(1)