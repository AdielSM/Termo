# GET start
Solicita um novo jogo ao servidor e cria uma thread para lidar com usuário

## Resposta:
200 <span style="color:lightblue"> (Jogo Iniciado) </span>
```json
{
    "message": "200"
}
```

400  <span style="color:lightblue"> (Jogo já iniciado) </span>
```json
{
    "message": "400"
}
```


# GET exit
Solicita que o jogo atual se encerre

## Resposta:
201 <span style="color:lightblue"> (Jogo Encerrado) </span>
```json
{
    "message": "201"
}
```

401  <span style="color:lightblue"> (Jogo não iniciado) </span>
```json
{
    "message": "401"
}
```


# POST check-word
Envia uma palavra para validação no lado do servidor (checando se acertou)

## Requisição:
```json
{
    "word": "palavra"
}
```

## Resposta:
202 <span style="color:lightblue"> (Palavra Correta) </span>
```json
{
    "message": "202"
    "attempts": "quantidade de tentativas restantes"
}
```

203 <span style="color:lightblue"> (Palavra Incorreta) </span>

### Código das cores:
#### - 0: cinza 
#### - 1: amarelo
#### - 2: verde

```json
{
    "message": "203",


    "feedback": [
        {
            "index": 0,
            "modification": "2" // verde,
        },
        {
            "index": 1,
            "modification": "1" // amarelo,
        },
        {
            "index": 2,
            "modification": "1" // amarelo,
        },
        {
            "index": 4,
            "modification": "0" // cinza,
        }
    ],


    "remaining_attempts": "quantidade de tentativas restantes"

}
```

401  <span style="color:lightblue"> (Jogo não iniciado) </span>
```json
{
    "message": 401 // "Jogo não iniciado.
}
```

402 <span style="color:lightblue"> (Necessário Parâmetro) </span>
```json
{
    "message": 402 // "Necessário Parâmetro.
    "remaining_attempts": "quantidade de tentativas restantes"
}
```

403  <span style="color:lightblue"> (Tamanho Incorreto) </span>
```json
{
    "message": 403 // "Tamanho Incorreto.
    "remaining_attempts": "quantidade de tentativas restantes"
}
```

404  <span style="color:lightblue"> (Palavra Inexistente) </span>
```json
{
    "message": 404 // "Palavra Inexistente.
    "remaining_attempts": "quantidade de tentativas restantes"
}
```

405  <span style="color:lightblue"> (Palavra Repetida) </span>
```json
{
    "message": 405 // "Palavra Repetida.
    "remaining_attempts": "quantidade de tentativas restantes"
}
```

# GET list_words

## Resposta:

204 <span style="color:lightblue"> (Lista de Palavras já Digitadas) </span>

```json

{
    "message": "204" // "Lista de Palavras já digitadas.
}

```

# BAD REQUEST

499  <span style="color:lightblue"> (Requisição Inválida) </span>
```json
{
    "message": 499 // "Requisição Inválida.
    "remaining_attempts": "quantidade de tentativas restantes"
}
```