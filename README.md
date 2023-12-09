# 🧩Termo

![TERMO](./img/Termo.png)

Projeto desenvolvido para simular o jogo de palavras Termo, onde o jogador deve advinhar a palavra proposta pelo jogo.

## 🔑 Índices

- [Funcionalidades](#-funcionalidades)
- [Instalação](#-instalação)
- [Como jogar](#-como-jogar)
- [Tecnologias](#-tecnologias)
- [Autores](#-autores)
- [Próximos passos](#-próximos-passos)	

## ⚙️ Funcionalidades
- [x] O jogo sorteia uma palavra aleatória de um arquivo e recebe palavras do usuário até que haja tentativas disponíveis.
- [x] O jogo possui um sistema de pontuação que é calculado com base no número de tentativas restantes e no tempo gasto na rodada.
- [x] O jogo possui um servidor que pode ser acessado por múltiplos clientes que estejam na mesma rede.
- [x] O jogo possui um sistema de salas que permite que os jogadores criem party's para jogar com seus amigos.
  
## 💻 Instalação

Para iniciar o jogo, é necessário ter o [Python](https://www.python.org/downloads/) instalado em sua máquina. A versão utilizada deve ser a 3.11.6 ou superior.

Após a instalação do Python, instale o [Git](https://git-scm.com/downloads) para clonar o repositório do jogo. Concluido isto, execute o seguinte comando no terminal:

```bash
git clone https://github.com/AdielSM/Termo
cd Termo
```

Feito isso, é necessário iniciar um ambiente virtual para instalar as dependências do jogo. Para isso, execute o seguinte comando no terminal:


```bash
python -m venv venv

# No Windows
venv\Scripts\activate

# No Linux ou MacOS
source venv/bin/activate
```

No windows, pode haver um erro ao executar o comando acima. Caso isso ocorra, execute o seguinte comando no powershell:

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

caso o erro persista, execute o seguinte comando:

```bash
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
```

Note que o comando que não possui o parâmetro RemoteSigned permite a execução de scripts não assinados. Para mais informações, acesse [este link](https://docs.microsoft.com/pt-br/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.1).

Depois da ativação do ambiente virtual, execute o seguinte comando para instalar as dependências do jogo:

```bash
pip install -r requirements.txt
```

Após a instalação das dependências, é necessário iniciar o servidor do jogo. Para isso, execute o seguinte comando:

```bash
python run_server.py
```

Após a inicialização do servidor, é necessário iniciar o cliente do jogo. Para isso, execute o seguinte comando:

```bash
python run_client.py
```

## 🎮 Como jogar

## 🚀 Tecnologias

As seguintes tecnologias foram utilizadas no desenvolvimento do projeto:

- [Python](https://www.python.org/)
- [Socket](https://docs.python.org/3/library/socket.html)
- [Threading](https://docs.python.org/3/library/threading.html)
- [Json](https://docs.python.org/3/library/json.html)
- [Numpy](https://numpy.org/)

## 👨‍💻 Autores


| <img src="./img/adielPerfilGithub.jpg" width="100" height="100"> | <img src="./img/caioPerfilGithub.png" width="100" height="100"> | <img src="./img/carlosPerfilGithub.jpg" width="100" height="100"> |
|:---:|:---:|:---:|
| [![LinkedIn](https://img.shields.io/badge/LinkedIn-Adiel-blue)](https://www.linkedin.com/in/adiel-melo-073009273/) [![GitHub](https://img.shields.io/badge/GitHub-AdielSM-black)](https://github.com/AdielSM) | [![LinkedIn](https://img.shields.io/badge/LinkedIn-Caio-blue)](https://www.linkedin.com/in/caio-soares-8b8a81251) [![GitHub](https://img.shields.io/badge/GitHub-Caio1-black)](https://github.com/caiosoares1) | [![LinkedIn](https://img.shields.io/badge/LinkedIn-Carlos-blue)](https://www.linkedin.com/in/jovemcarlos/) [![GitHub](https://img.shields.io/badge/GitHub-CarlosTI-black)](https://github.com/JovemCarlosTI) |




## 👟 Próximos passos

- [ ] Estabelecer um banco de dados para armazenar os dados dos jogadores para conseguir fazer um ranking com todos os participantes.

- [ ] Implementar um sistema de chat para que os jogadores possam conversar entre si entre as rodadas de uma party.

- [ ] Implementar um sistema de dicas que possa ser utilizado pelo jogador durante a partida.

- [ ] Produzir uma interface gráfica para o jogo.