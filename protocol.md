****GET_GAME** ** – Solicita um novo jogo ao servidor e cria uma thread para lidar com usuário

+OK
primeira letra (ex: “s”)

+ERRO

Ex:
**GET_GAME** 
“a”
 
**EXIT_GAME** - Solicita que o jogo atual se encerre

+OK - O jogo é encerrado.

****CHECK_WORD**** palavra - Envia uma palavra para validação no lado do servidor (checando se acertou)

+ACERTOU
quantidades de tentativas anteriores

Ex: Palavra correta = buscar
**CHECK_WORD** buscar
+ACERTOU
3

+ERROU
devolve palavra com feedback visual (letras verdes se há aquela letra naquela posição, letras amarelas se há aquela letra em outra posição)
quantidade de tentativas restantes

Ex: Palavra correta = buscar
**CHECK_WORD** banana
+ERROU
“\033[92mb\033[93ma\033[0mnana” (visualmente: “banana”)
2

+SEM_TENTATIVAS

Ex: Palavra correta = buscar
**CHECK_WORD** banana
+SEM_TENTATIVAS

+ERRO
mensagem de erro

Ex: Palavra correta = buscar
**CHECK_WORD** pamonha
+ERRO
“Palavra deve conter 6 letras”

Ex: Palavra correta = buscar
**CHECK_WORD** asdasddwqd
+ERRO
“Essa palavra não é aceita”