# 🧩Termo

![TERMO](./img/Termo.png)

Projeto desenvolvido para simular o jogo de palavras Termo, onde o jogador deve advinhar a palavra proposta pelo jogo.

## 🔑 Índices

- [Página de Regras do Jogo](https://adielsm.github.io/Termo/)
- [Protocolo da Aplicação](./protocol.md)
- [Descrição do Problema e Funcionalidades](#-descrição-do-problema-e-funcionalidades)
- [Instalação](#-instalação)
- [Tecnologias](#-tecnologias)
- [Autores](#-autores)
- [Disciplinas](#-disciplinas)
- [Arquivos do Projeto](#-arquivos-do-projeto)
- [Próximos passos](#-próximos-passos)

## ⚙️ Descrição do Problema e Funcionalidades
- [x] O jogo sorteia uma palavra aleatória de um arquivo e recebe palavras do usuário até que haja tentativas disponíveis.
- [x] O jogo possui um sistema de pontuação que é calculado com base no número de tentativas restantes e no tempo gasto na rodada.
- [x] O jogo possui um servidor que pode ser acessado por múltiplos clientes que estejam na mesma rede.
- [x] O cliente pode se conectar ao servidor que desejar, desde que esteja na mesma rede.

  
## 💻 Instalação
### 📕 Bibliotecas Utilizadas
- prettytable==3.9.0: Facilita a criação de tabelas bem formatadas em texto. Ela fornece uma maneira simples de organizar dados em colunas e linhas, tornando a exibição de informações tabulares mais legível e esteticamente agradável. Usado para menu e ranking do jogador.

- wcwidth==0.2.12: Essa biblioteca é usada para calcular a largura de caracteres Unicode em uma string. Ela é útil quando precisa lidar com texto que contém caracteres de largura variável, como caracteres de largura dupla usados em alguns idiomas asiáticos, sendo usada para menu e ranking do jogador.

- zeroconf==0.131.0: Essa biblioteca implementa o protocolo Zeroconf, que permite a descoberta automática de serviços em uma rede local. Ela facilita a comunicação entre dispositivos em uma rede sem a necessidade de configuração manual. É utilizada para o servidor anuncia a cada período de tempo que está disponível na rede local, permitindo que o cliente saiba da sua atividade e liste para o usuário final.

- psutil==5.9.7: Fornece uma interface para acessar informações sobre o sistema operacional em que o código está sendo executado. Ela permite que você obtenha informações sobre o uso da CPU, memória, disco, rede e outros recursos do sistema, sendo usada junto com iifaddr para o servidor retornar seu endereço IP privado.

- iifaddr==0.2.0: Útil quando precisa descobrir quais interfaces de rede estão ativas e quais endereços IP estão associados a elas, sendo usada para o servidor retornar seu endereço IP privado.

### Passo a Passo

Para iniciar o jogo, é necessário ter o [Python](https://www.python.org/downloads/) instalado em sua máquina. A versão utilizada deve ser a 3.11.6 ou superior.

Após a instalação do Python, instale o [Git](https://git-scm.com/downloads) para clonar o repositório do jogo. Concluido isto, execute o seguinte comando no terminal do seu sistema operacional:

```bash
git clone https://github.com/AdielSM/Termo
cd Termo
code .
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

## 🚀 Tecnologias

As seguintes tecnologias foram utilizadas no desenvolvimento do projeto:

- [Python](https://www.python.org/)
- [Socket](https://docs.python.org/3/library/socket.html)
- [Threading](https://docs.python.org/3/library/threading.html)
- [Json](https://docs.python.org/3/library/json.html)
- [Zeroconf](https://pypi.org/project/zeroconf/)


## 👨‍💻 Autores


| <img src="./img/adielPerfilGithub.jpg" width="100" height="100"> | <img src="./img/caioPerfilGithub.png" width="100" height="100"> | <img src="./img/carlosPerfilGithub.jpg" width="100" height="100"> |
|:---:|:---:|:---:|
| [![LinkedIn](https://img.shields.io/badge/LinkedIn-Adiel-blue)](https://www.linkedin.com/in/adiel-melo-073009273/) [![GitHub](https://img.shields.io/badge/GitHub-AdielSM-black)](https://github.com/AdielSM) | [![LinkedIn](https://img.shields.io/badge/LinkedIn-Caio-blue)](https://www.linkedin.com/in/caio-soares-8b8a81251) [![GitHub](https://img.shields.io/badge/GitHub-Caio1-black)](https://github.com/caiosoares1) | [![LinkedIn](https://img.shields.io/badge/LinkedIn-Carlos-blue)](https://www.linkedin.com/in/jovemcarlos/) [![GitHub](https://img.shields.io/badge/GitHub-CarlosTI-black)](https://github.com/JovemCarlosTI) |

## 📚 Disciplinas

- Estruturas de Dados (Alex Sandro Rêgo)
- Sistemas Operacionais (Gustavo Wagner)
- Protocolos de Interconexão de Redes de Computadores (Leonidas Lima)

## 📂 Arquivos do Projeto

| Pasta/Arquivo | Descrição |
|:------------------|:------------------|
| 📂Client/ | Pasta que contém os arquivos do Cliente. |
| ㄴ 📄__init__.py | Arquivo de inicialização que importa a Classe Client. |
| ㄴ 📄client.py | Arquivo que possui a responsabilidade de gerenciar o funcionamento do Cliente. |
| 📂Server/ | Pasta que contém os arquivos do Servidor. |
| ㄴ 📄__init__.py | Arquivo de inicialização para o Servidor. |
| ㄴ 📄AVLtree.py | Arquivo que contém a Árvore AVL. |
| ㄴ 📄classes_exceptions.py | Arquivo de exceções personalizadas utilizadas no Projeto. |
| ㄴ 📄player.py | Arquivo que possui a Classe que representa um jogador do jogo. |
| ㄴ 📄server.py | Arquivo que possui a responsabilidade de gerenciar o funcionamento do Servidor. |
| ㄴ 📄termo.py | Arquivo que possui a responsabilidade de gerenciar o funcionamento do Jogo Termo. |
| ㄴ 📄termo_words_loader.py | Arquivo para carregar a palavra secreta que será sorteada e utilizada em cada jogo. |
| ㄴ 📄words_loader.py | Arquivo que carrega palavras para verificar se a tentativa de jogador é válida. |
| 📂docs/ | Pasta que contém os arquivos de imagens e página de regras |
| ㄴ 📄index.html | Arquivo de regras gerais do jogo Termo. |
| ㄴ 📂img/ | Pasta que contém os arquivos de imagens utilizadas na página de Regras. |
| 📂img/ | Pasta que contém os arquivos de imagens utilizadas no README. |
| 📂utils/ | Pasta que contém os arquivos utilitários, como configurações de Servidor e sumário de Protocolo. |
| ㄴ 📄__init__.py | Arquivo que importa a Lista e o sumário de Protocolo. |
| ㄴ 📄LinkedStack.py | Pilha encadeada em python. |
| ㄴ 📄server_config.py | Arquivo que retorna as configurações do Servidor. |
| ㄴ 📄server_config.txt | Arquivo que contém as configurações do Servidor (TAM_MSG e PORT). |
| ㄴ 📄summary_protocol.py | Retorna um dicionário com as informações do protocolo. |
| ㄴ 📄summary_protocol.txt | Sumário de Protocolo que contém as mensagens enviadas e seu respectivo código de status. |
| 📂words_bank/ | Pasta que contém os arquivos txt das palavras para o funcionamento do Termo. |
| ㄴ 📄bd.txt | Arquivo que contém um banco de palavras para testar se a tentativa do jogador é válida. |
| ㄴ 📄bd_termo.txt | Arquivo que contém um banco de palavras que serão utilizadas no jogo Termo. |
| 📄.gitIgnore | Arquivo de configuração usado pelo Git para especificar quais arquivos e diretórios devem ser ignorados. |
| 📄README | Arquivo README. |
| 📄protocol.md | Arquivo que contém os comandos do protocolo e o status code retornado. |
| 📄requirements.txt | Arquivo que contém as dependências necessárias para poder iniciar o Termo. |
| 📄run_client.py | Arquivo para rodar o cliente. |
| 📄run_server.py | Arquivo para rodar o servidor. |

## 👟 Próximos passos

- [ ] Estabelecer um banco de dados para armazenar os dados dos jogadores para conseguir fazer um ranking com todos os participantes.

- [ ] Implementar um sistema de party para que os jogadores possam jogar em salas com seus amigos.

- [ ] Implementar um sistema de dicas que possa ser utilizado pelo jogador durante a partida.

- [ ] Produzir uma interface gráfica para o jogo.
