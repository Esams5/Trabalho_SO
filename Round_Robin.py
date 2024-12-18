import numpy as np

def round_robin(processes, burst_times, quantum, context_switch_time=1):
    n = len(processes)

    # Inicialização das estruturas de controle
    remaining_burst = burst_times[:]
    waiting_times = [0] * n
    turnaround_times = [0] * n
    current_time = 0
    sequence = []

    # Criação de uma fila para os processos
    queue = [(i, burst_times[i]) for i in range(n)]

    while queue:
        process, burst = queue.pop(0)

        # Executa o processo por "quantum" ou pelo restante do burst time
        execution_time = min(quantum, burst)
        current_time += execution_time

        # Adiciona ao log de sequência de execução
        sequence.append((processes[process], current_time))

        # Atualiza o burst restante
        remaining_burst[process] -= execution_time

        # Se o processo ainda não terminou, adiciona à fila
        if remaining_burst[process] > 0:
            queue.append((process, remaining_burst[process]))
            current_time += context_switch_time  # Tempo de mudança de contexto
        else:
            # Calcula turnaround time e waiting time
            turnaround_times[process] = current_time
            waiting_times[process] = turnaround_times[process] - burst_times[process]

    # Métricas
    avg_waiting_time = np.mean(waiting_times)
    std_waiting_time = np.std(waiting_times)

    avg_turnaround_time = np.mean(turnaround_times)
    std_turnaround_time = np.std(turnaround_times)

    throughput = n / current_time

    return sequence, avg_waiting_time, std_waiting_time, avg_turnaround_time, std_turnaround_time, throughput

# Função principal para executar a simulação
def main():
    processes = ["P1", "P2", "P3", "P4"]
    burst_times = [8, 4, 9, 5]  # Burst time de cada processo
    quantum_values = [2, 4, 6]  # Diferentes valores de quantum

    print("Simulação do Algoritmo Round Robin\n")
    for quantum in quantum_values:
        print(f"Quantum: {quantum}\n")
        sequence, avg_waiting_time, std_waiting_time, avg_turnaround_time, std_turnaround_time, throughput = round_robin(
            processes, burst_times, quantum
        )

        print("Sequência de execução:")
        for p, t in sequence:
            print(f"{p} até {t}")

        print(f"\nTempo médio de espera: {avg_waiting_time:.2f} (+/- {std_waiting_time:.2f})")
        print(f"Tempo médio de retorno: {avg_turnaround_time:.2f} (+/- {std_turnaround_time:.2f})")
        print(f"Vazão: {throughput:.2f} processos/unidade de tempo\n")
        print("-" * 50)

if __name__ == "__main__":
    main()
