# GET /game/start
Solicita um novo jogo ao servidor e cria uma thread para lidar com usuário

## Resposta:
200 OK
```json
{
    "message": "Jogo iniciado"
}
```

400 Bad Request
```json
{
    "error": "mensagem de erro"
}
```

# GET /game/exit
Solicita que o jogo atual se encerre

## Resposta:
200 OK
```json
{
    "message": "O jogo é encerrado."
}
```

# POST /game/check-word
Envia uma palavra para validação no lado do servidor (checando se acertou)

## Requisição:
```json
{
    "word": "palavra"
}
```

## Resposta:
200 OK
```json
{
    "status": "+ACERTOU",
    "attempts": "quantidades de tentativas anteriores"
}
```

200 OK
```json
{
    "status": "+ERROU",
    "feedback": [
        {
            "index": 0,
            "modification": "green",
        },
        {
            "index": 1,
            "modification": "yellow",
        },
        {
            "index": 2,
            "modification": "yellow",
        },
        {
            "index": 4,
            "modification": "green",
        }
    ],
    "remaining_attempts": "quantidade de tentativas restantes"

}
```

200 OK
```json
{
    "status": "+SEM_TENTATIVAS"
}
```

### Mensagem de erro:
Serve para indicar que o usuário tentou enviar uma palavra inválida (não é uma palavra, já foi enviada, etc)

400 Bad Request
```json
{   
    "status": 400
    "error": "mensagem de erro"
    "remaining_attempts": "quantidade de tentativas restantes
}
```