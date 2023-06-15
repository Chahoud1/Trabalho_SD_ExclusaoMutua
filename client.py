import socket
import threading
import time

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('localhost', 7777))
    except:
        return print('\nNão foi possível se conectar ao servidor')

    process_name = input('Processo - ').encode('utf-8')
    client.send(process_name)

    threadR = threading.Thread(target=receiveMessage, args=[client])
    threadS = threading.Thread(target=sendMessage, args=[client, process_name])

    threadR.start()
    threadS.start()


# Envio de dados para o servidor
def sendMessage(client, process_name):
    while True:
        try:
            client.send(f'Preciso de acesso à região crítica'.encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            #print(f"Resposta do servidor: {response}\n")
            time.sleep(2)
        except:
            print('erro em sendMessage')
            pass

# Recebendo a resposta do servidor
def receiveMessage(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(f"Resposta do servidor: {message} \n")
        except:
            print('\nNão foi possível permanecer conectado no servidor')
            break

main()
