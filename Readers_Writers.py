import threading
import time
import random

# Configuração inicial
NUM_READERS = 5
NUM_WRITERS = 2
READ_TIME = 2
WRITE_TIME = 2
SIMULATION_TIME = 10  # Tempo total de simulação

# Variáveis globais
read_count = 0  # Contador de leitores na região crítica
read_count_mutex = threading.Lock()  # Mutex para proteger o contador
write_mutex = threading.Lock()  # Semáforo para acesso exclusivo dos escritores
turnstile = threading.Lock()  # Controle para priorização
stop_simulation = False  # Flag para encerrar as threads

# Funções dos leitores e escritores na segunda solução (prioridade balanceada)
def reader_solution2(reader_id):
    global read_count, stop_simulation
    while not stop_simulation:
        # Entrada: Passa pelo turnstile para evitar starvation dos escritores
        with turnstile:
            pass
        with read_count_mutex:
            read_count += 1
            if read_count == 1:
                write_mutex.acquire()
        
        print(f"Leitor {reader_id} está lendo.")
        time.sleep(random.uniform(0.5, READ_TIME))  # Simula tempo de leitura
        print(f"Leitor {reader_id} terminou de ler.")

        with read_count_mutex:
            read_count -= 1
            if read_count == 0:
                write_mutex.release()

        time.sleep(random.uniform(0.5, 1.0))

def writer_solution2(writer_id):
    global stop_simulation
    while not stop_simulation:
        # Escritor passa pelo turnstile antes de escrever
        with turnstile:
            write_mutex.acquire()
            print(f"Escritor {writer_id} está escrevendo.")
            time.sleep(random.uniform(0.5, WRITE_TIME))  # Simula tempo de escrita
            print(f"Escritor {writer_id} terminou de escrever.")
            write_mutex.release()
        time.sleep(random.uniform(1.0, 2.0))


def simulate(solution=2):
    global stop_simulation
    threads = []
    print("Iniciando simulação da solução", solution)

    for i in range(NUM_READERS):
        t = threading.Thread(target=reader_solution2, args=(i,))
        threads.append(t)
    for i in range(NUM_WRITERS):
        t = threading.Thread(target=writer_solution2, args=(i,))
        threads.append(t)

    # Inicia as threads
    for t in threads:
        t.start()

    # Roda por tempo determinado
    time.sleep(SIMULATION_TIME)

    
    print("Encerrando simulação...")
    stop_simulation = True

    # Aguarda o término das threads
    for t in threads:
        t.join()

    print("Simulação finalizada.")


if __name__ == "__main__":
    simulate(solution=2)
