import threading
import time
import random

# Solução 1: Escritores esperam indefinidamente enquanto há leitores
class ReadersWritersSolution1:
    def __init__(self):
        self.read_count = 0
        self.read_count_lock = threading.Lock()
        self.resource_lock = threading.Lock()

    def reader(self, reader_id):
        while True:
            # Entrada na seção crítica
            with self.read_count_lock:
                self.read_count += 1
                if self.read_count == 1:
                    self.resource_lock.acquire()

            # Região crítica de leitura
            print(f"Reader {reader_id} is reading.")
            time.sleep(random.uniform(0.1, 0.5))

            # Saída da seção crítica
            with self.read_count_lock:
                self.read_count -= 1
                if self.read_count == 0:
                    self.resource_lock.release()

            time.sleep(random.uniform(0.1, 0.5))

    def writer(self, writer_id):
        while True:
            # Escritor espera até que não haja leitores
            self.resource_lock.acquire()

            # Região crítica de escrita
            print(f"Writer {writer_id} is writing.")
            time.sleep(random.uniform(0.2, 0.6))

            self.resource_lock.release()
            time.sleep(random.uniform(0.2, 0.6))

# Solução 2: Evita espera indefinida para escritores
class ReadersWritersSolution2:
    def __init__(self):
        self.read_count = 0
        self.read_count_lock = threading.Lock()
        self.resource_lock = threading.Lock()
        self.writer_priority_lock = threading.Lock()

    def reader(self, reader_id):
        while True:
            with self.writer_priority_lock:
                with self.read_count_lock:
                    self.read_count += 1
                    if self.read_count == 1:
                        self.resource_lock.acquire()

            print(f"Reader {reader_id} is reading.")
            time.sleep(random.uniform(0.1, 0.5))

            with self.read_count_lock:
                self.read_count -= 1
                if self.read_count == 0:
                    self.resource_lock.release()

            time.sleep(random.uniform(0.1, 0.5))

    def writer(self, writer_id):
        while True:
            self.writer_priority_lock.acquire()
            self.resource_lock.acquire()

            print(f"Writer {writer_id} is writing.")
            time.sleep(random.uniform(0.2, 0.6))

            self.resource_lock.release()
            self.writer_priority_lock.release()
            time.sleep(random.uniform(0.2, 0.6))

# Função principal para simulação
def simulate_readers_writers(solution_class, num_readers=5, num_writers=2, duration=10):
    solution = solution_class()

    threads = []
    for i in range(num_readers):
        t = threading.Thread(target=solution.reader, args=(i + 1,))
        threads.append(t)
        t.start()

    for i in range(num_writers):
        t = threading.Thread(target=solution.writer, args=(i + 1,))
        threads.append(t)
        t.start()

    time.sleep(duration)
    print("Simulation complete. Terminating threads...")

if __name__ == "__main__":
    print("Running Readers-Writers Solution 1 (Writers may wait indefinitely)...")
    simulate_readers_writers(ReadersWritersSolution1, duration=10)

    print("\nRunning Readers-Writers Solution 2 (Writers avoid indefinite waiting)...")
    simulate_readers_writers(ReadersWritersSolution2, duration=10)
