import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

# Configurações globais
NUM_FILOSOFOS = 5
TEMPO_LIMITE = 5
TENTATIVAS_COMER = 3
EXECUCOES = 1000

def configurar_garfos():
    """Inicializa os semáforos que representam os garfos."""
    return [threading.Semaphore(1) for _ in range(NUM_FILOSOFOS)]

def pegar_garfos(filosofo_id, garfos):
    """Gerencia a aquisição dos garfos pelos filósofos."""
    if filosofo_id == NUM_FILOSOFOS - 1:
        garfos[(filosofo_id + 1) % NUM_FILOSOFOS].acquire()
        garfos[filosofo_id].acquire()
    else:
        garfos[filosofo_id].acquire()
        garfos[(filosofo_id + 1) % NUM_FILOSOFOS].acquire()

def liberar_garfos(filosofo_id, garfos):
    """Gerencia a liberação dos garfos pelos filósofos."""
    garfos[filosofo_id].release()
    garfos[(filosofo_id + 1) % NUM_FILOSOFOS].release()

def verificar_deadlock(estados, threads):
    """Verifica se houve deadlock no jantar."""
    inicio = time.time()
    while time.time() - inicio < TEMPO_LIMITE:
        if not any(estados):
            for t in threads:
                t.join()
            return False
    return True

def jantar_dos_filosofos_sem_solucao(resultados, execucao_id):
    """Simula o problema dos filósofos com possibilidade de deadlock."""
    garfos = configurar_garfos()
    estados = [False] * NUM_FILOSOFOS

    def filosofo(filosofo_id):
        for _ in range(TENTATIVAS_COMER):
            pegar_garfos(filosofo_id, garfos)
            estados[filosofo_id] = True
            time.sleep(0.1)
            estados[filosofo_id] = False
            liberar_garfos(filosofo_id, garfos)

    threads = [threading.Thread(target=filosofo, args=(i,)) for i in range(NUM_FILOSOFOS)]
    for t in threads:
        t.start()

    if verificar_deadlock(estados, threads):
        resultados[execucao_id] = "Deadlock"
    else:
        resultados[execucao_id] = "Sem Deadlock"

# Executa várias simulações
resultados = {}
with ThreadPoolExecutor(max_workers=10) as executor:
    for execucao_id in range(EXECUCOES):
        executor.submit(jantar_dos_filosofos_sem_solucao, resultados, execucao_id)

# Resumo dos resultados
contagem_resultados = Counter(resultados.values())
print(f"Execuções sem deadlock: {contagem_resultados['Sem Deadlock']}")
print(f"Execuções com deadlock: {contagem_resultados['Deadlock']}")