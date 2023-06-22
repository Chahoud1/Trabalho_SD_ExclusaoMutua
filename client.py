#client
import socket
import threading
import time
import random

# numero de processos
num_of_procs = 4
# numero de requisicoes de cada processo
num_of_reqs = 1
# sera num_of_procs*num_of_reqs, ou seja, o número total de solicitações ao servidor
total_of_reqs = []

# criacao do client
# AF_INET: IPv4 // SOCKDGRAM: UDP
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# endereco do servidor, tem que ser o mesmo para haver a conexao
server_address = ('localhost', 7777)

def main(process_n):

    # thread para receber as mensagens do servidor
    threadR = threading.Thread(target=receiveMessage, args=[])
    # thread para enviar as mensagens ao servidor
    threadS = threading.Thread(target=sendMessage, args=[process_n])

    threadS.start()
    threadR.start()
# envio de dados para o servidor
def sendMessage(process_n):
    for i in range(num_of_reqs):
            time.sleep(4)
            try:
                # tipo mensagem(1 para request)|numero do processo|complemento - mensagem
                message = f'1|{process_n}|000000 - Preciso de acesso a regiao critica'
                # envia bytes ao servidor
                client.sendto(message.encode('utf-8'), server_address)
                print(f'Messagem enviada para o servidor pelo processo {process_n}')
            except:
                print('erro em sendMessage')
    return
            
# recebendo a resposta do servidor
def receiveMessage():
    while True:
        time.sleep(2)
        try:
            # resposta do servidor
            response, address = client.recvfrom(1024)
            print(f"Resposta do servidor: {response.decode('utf-8')} \n")
        except Exception as e:
            print(f'\nSem resposta para receber do servidor')

# inicia os processos
for process_n in range(num_of_procs):
    for req in range(num_of_reqs):
        total_of_reqs.append(process_n)

# coloca as solicitacoes dos processos em ordem aleatoria
shuffled_total_of_reqs = random.sample(total_of_reqs, len(total_of_reqs))

# começa a lancar as solicitacoes do lado do client com ordem aleatoria de processo
for request in shuffled_total_of_reqs:
    time.sleep(1)
    main(request)