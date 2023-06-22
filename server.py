import socket
import threading
import time
import datetime
import sys

# tempo dentro da região critica
time_delay = 5 
# list que contém os clientes que solicitaram conexão
client_buffer = []
# lock para garantir exclusão mútua no client_buffer
clients_lock = threading.Lock()

# criacao do servidor
# AF_INET: IPv4 // SOCKDGRAM: UDP
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# dominio e porta do servidor
server_address = ('localhost', 7777)

def main():
    try:
        # amarracao do servidor ao endereco criado
        server.bind(server_address)
        print('Aguardando conexões...')
    except:
        print('\nNão foi possível iniciar o servidor!')

    # thread do terminal
    thread_terminal = threading.Thread(target=terminal)
    thread_terminal.start()

    # thread da região crítica
    thread_CR = threading.Thread(target=enterCriticalRegion)
    thread_CR.start()

    # thread para receber as conexões do client
    thread_R_MSG = threading.Thread(target=receiveMessage)
    thread_R_MSG.start()

# grant do processo
def enterCriticalRegion():
    while True:
        time.sleep(2)
        if len(client_buffer) > 0:
            # trava o acesso ao client_buffer
            clients_lock.acquire()
            # tempo dentro da regiao critica
            time.sleep(time_delay)
            # horario de acesso do processo a CR para ser gravado no .txt
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            # abre a escrita do .txt
            with open("resultado.txt", "a") as file:
                file.write(f"{timestamp} - Processo {client_buffer[0]['process_n']}\n")
            # envia a resposta do processo
            sendMessage(f"(GRANT) O processo {client_buffer[0]['process_n']} acessou a região crítica", client_buffer[0]['address'])

            # tinha sido retirado por conta do loopback, mas parou de acontecer
            print(f"(GRANT) O processo {client_buffer[0]['process_n']} entrou na região crítica\n")

            # libera a escrita do client_buffer para o próximo processo
            clients_lock.release()
            # o processo e removido da lista
            deleteClient()
        else:
            print('\nNenhum processo na fila\n')

# request do processo
def receiveMessage():
    while True:
        message, address = server.recvfrom(1024)
        # mensagem binaria para string
        decoded_message = message.decode('utf-8')
        # para saber qual e o processo e o que ele solicitou
        message_parts = decoded_message.split('|')
        if len(message_parts) >= 2:
            # evitar condicao de corrida no client_buffer
            with clients_lock:
                # request do processo e armazenada no buffer
                client_buffer.append({'message': decoded_message, 'address': address, 'process_n': message_parts[1]})
                sendMessage(f"(REQUEST) solicitacao recebida de {message_parts[1]}", address)
            
                # tinha sido retirado por conta do loopback
                print(f"(REQUEST) solicitacao recebido de {message_parts[1]}")

        # se cair aqui, significa que a mensagem e a propria resposta do servidor, provavel loopback
        else:
            print("Servidor:", decoded_message)


def sendMessage(message, address):
    try:
        # envia a mensagem apenas para o processo em questao
        server.sendto(message.encode('utf-8'), ('localhost', address[1]))
    except Exception as e:
        print('Erro em sendMessage:', str(e))


# release do processo
def deleteClient():
    if len(client_buffer) > 0:
        with clients_lock:
            sendMessage(f"(RELEASE) processo {client_buffer[0]['process_n']} removido da fila", client_buffer[0]['address'])
            print(f"(RELEASE) Processo {client_buffer[0]['process_n']} removido da fila")
            client_buffer.pop(0)
    else:
        print("buffer está vazio")


def terminal():
    while True:
        choice = input('\n1-Imprimir a fila de pedidos\n2-Imprimir quantas vezes cada processo foi atendido\n3-Encerrar a execução\n')
        if choice == '1':
            print(client_buffer)

        if choice == '2':
            # Dicionário para armazenar a contagem de linhas para cada número
            contador = {}
            with open("resultado.txt", "r") as f:
                for line in f:
                    number = line.strip()[-1]  # Obtém o último caractere da linha
                    if number.isdigit():  # Verifica se é um dígito
                        if number in contador:
                            contador[number] += 1
                        else:
                            contador[number] = 1
            # Imprime o resultado
            for number, count in contador.items():
                print(f"Número {number}: {count} linhas")

        # encerra todas as execuções do servidor
        if choice == '3':
            server.shutdown(socket.SHUT_RDWR)  # Encerra leitura e escrita do socket
            server.close()  # Fecha o socket do servidor
            sys.exit(0)  # Encerra o programa com código de saída 0

main()
