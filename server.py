# server
import socket
import threading
import time

clients = []
clients_lock = threading.Lock()
buffer = []

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(('localhost', 7777))
        server.listen()
        print('Aguardando conexões...')
    except:
        return print('\nNão foi possível iniciar o servidor!')

    while True:
        client, address = server.accept()
        process_name = client.recv(1024).decode('utf-8')
        clients.append({'name': process_name, 'socket': client })

        thread_messages = threading.Thread(target=messagesTreatment, args=[client, process_name])
        thread_terminal = threading.Thread(target=terminal)
        thread_cr = threading.Thread(target=enterCriticalRegion, args=[client, process_name])     

        thread_messages.start()
        thread_terminal.start()
        thread_cr.start()

def messagesTreatment(client, process_name):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            #processo solicita entrada na região crítica
            buffer.append(process_name)
            print(f'{process_name}: {message}')
        except:
            print('erro em messagesTreatment')
            break

def enterCriticalRegion(client, proccess_name):
    while True:    
        time.sleep(4)
        clients_lock.acquire()
        print(f'O processo {proccess_name} entrou na região crítica')
        sendMessage(client, "Você acessou a região crítica")
        if len(buffer) > 0:
            buffer.pop(0)
        else: 
            print("buffer está vazio")
        clients_lock.release()
        time.sleep(3)
        

def sendMessage(client, message):
    try:
        client.send(message.encode('utf-8'))
    except:
        print('Erro ao enviar mensagem')

def terminal():
    while True:
        choice = input('\n1-Imprimir a fila de pedidos\n2-Imprimir quantas vezes cada processo foi atendido\n3-Encerrar a execução\n\n')
        if choice == '1':
            for index, process in enumerate(buffer):
                print(f'{index} - {process}\n')
        if choice == '2':
            pass
        if choice == '3':
            pass

def deleteClient(client):
    with clients_lock:
        if client in clients:
            clients.remove(client)

main()
