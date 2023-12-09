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
    
    try:
        remaining_attempts = kwargs["remaining_attempts"]
        remaining_attempts = "Tentativas Restantes: " + str(remaining_attempts) + "\n"
    except KeyError:
        pass

            
    match data:
        case 200:
            print("Jogo Iniciado com Sucesso",end='\n\n')
            
        case 201:
            print("Jogo Encerrado com Sucesso",end='\n\n')
            
        case 202:
            print("🏆 Parabéns! Palavra Correta! 😎")
            print("Lista de Palavras Anteriores:")
            print(pilhaPalavras)
            pilhaPalavras.clear()
            print(remaining_attempts)
            
        case 203:
            pilhaPalavras.empilha(format_output)
            print('')
            print("Palavra Incorreta!")
            print(format_output)
            print('')
            print(remaining_attempts)

            if kwargs.get("remaining_attempts", '') == 0:
                pilhaPalavras.clear()
                secret_word_animation(kwargs.get("secret_word"))
                
        case 204:
            print("Lista de Palavras:")
            print(pilhaPalavras,end='\n\n')
            
        case 205:
            print('Jogo Reiniciado com Sucesso',end='\n\n')
            
        case 206:
            player_name = kwargs.get('player_name')
            print(f'Jogo Continuado com Sucesso, Boa Sorte na Próxima Rodada {player_name}!',end='\n\n')
            
        case 400:
            print("Jogo já iniciado",end='\n\n')
            
        case 401:
            print("Jogo não iniciado",end="\n\n")
            
        case 402:
            print("Necessário Forcener uma Palavra")
            print(remaining_attempts)

        case 403:
            print("A palavra deve conter 5 letras")
            print(remaining_attempts)

        case 404:
            print("Palavra inexiste no dicionário")
            print(remaining_attempts)

        case 405:
            print("Palavra já utilizada")
            print(remaining_attempts)
            
        case 499:
            if remaining_attempts:
                print("Comando Inválido")
                print(remaining_attempts)
            
            else:
                print("Comando Inválido")
            

def secret_word_animation(palavra) -> None:
    palavra_transformada = ['_' for _ in palavra]
    
    print('Você não conseguiu adivinhar a palavra secreta!')
    print('A palavra era:')
    
    for i in range(len(palavra)):
        palavra_transformada[i] = palavra[i]
        print(''.join(palavra_transformada))
        sleep(1)