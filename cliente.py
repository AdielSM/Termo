import sockets

# Cria um socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta o socket à porta onde o servidor está escutando
server_address = ('localhost', 10000)
print('Conectando a {} porta {}'.format(*server_address))
sock.connect(server_address)

try:
    # Envia dados
    message = 'Este é o meu dado. Ele será repetido.'
    print('Enviando {!r}'.format(message))
    sock.sendall(message.encode())

    # Olha a resposta
    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print('Recebido {!r}'.format(data.decode()))

finally:
    print('Fechando socket')
    sock.close()
    
