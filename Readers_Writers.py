import threading
import time
import random

# Variáveis globais
read_count = 0           # Contador de leitores
mutex = threading.Lock()  # Lock para o contador de leitores
wrt = threading.Lock()    # Lock para escritores
fair_lock = threading.Lock()  # Lock extra para evitar starvation
turn = threading.Condition()  # Condição para o acesso justo
total_accesses = 5         # Quantidade de acessos para cada leitor/escritor

# Solução 1: Prioridade para Leitores
def reader_priority(reader_id):
    global read_count
    for _ in range(total_accesses):
        # Entrada da região crítica
        mutex.acquire()
        read_count += 1
        if read_count == 1:  # Primeiro leitor bloqueia os escritores
            wrt.acquire()
        mutex.release()

        # Leitura
        print(f"Leitor {reader_id} (Prioridade Leitores) está lendo.")
        time.sleep(random.uniform(0.1, 0.3))

        # Saída
        mutex.acquire()
        read_count -= 1
        if read_count == 0:  # Último leitor libera a região crítica
            wrt.release()
        mutex.release()

def writer_priority(writer_id):
    for _ in range(total_accesses):
        # Escritores esperam indefinidamente se houver leitores
        wrt.acquire()
        print(f"Escritor {writer_id} (Prioridade Leitores) está escrevendo.")
        time.sleep(random.uniform(0.2, 0.4))
        wrt.release()

# Solução 2: Acesso Justo - Resolvido para evitar starvation
def fair_reader(reader_id):
    global read_count
    for _ in range(total_accesses):
        with fair_lock:  # Escritores têm chance de adquirir o lock
            mutex.acquire()
            read_count += 1
            if read_count == 1:
                wrt.acquire()
            mutex.release()

        # Leitura
        print(f"Leitor {reader_id} (Acesso Justo) está lendo.")
        time.sleep(random.uniform(0.1, 0.3))

        # Saída
        mutex.acquire()
        read_count -= 1
        if read_count == 0:
            wrt.release()
        mutex.release()

def fair_writer(writer_id):
    for _ in range(total_accesses):
        with fair_lock:  # Escritores aguardam "justamente" na fila
            wrt.acquire()
            print(f"Escritor {writer_id} (Acesso Justo) está escrevendo.")
            time.sleep(random.uniform(0.2, 0.4))
            wrt.release()

# Função principal para comparar as soluções
def main():
    num_readers = 5
    num_writers = 3

    # Solução 1: Prioridade para Leitores
    print("\n=== Solução 1: Prioridade para Leitores ===")
    threads1 = []
    for i in range(num_readers):
        threads1.append(threading.Thread(target=reader_priority, args=(i + 1,)))
    for i in range(num_writers):
        threads1.append(threading.Thread(target=writer_priority, args=(i + 1,)))

    # Executa as threads da solução 1
    for t in threads1:
        t.start()
    for t in threads1:
        t.join()

    # Solução 2: Acesso Justo para Evitar Starvation
    print("\n=== Solução 2: Acesso Justo para Evitar Starvation ===")
    threads2 = []
    for i in range(num_readers):
        threads2.append(threading.Thread(target=fair_reader, args=(i + 1,)))
    for i in range(num_writers):
        threads2.append(threading.Thread(target=fair_writer, args=(i + 1,)))

    # Executa as threads da solução 2
    for t in threads2:
        t.start()
    for t in threads2:
        t.join()

    print("\n=== Fim da Comparação ===")

if __name__ == "__main__":
    main()