import time
import threading

CPU_HOLD_DURATION: int = 5
RAM_HOLD_DURATION: int = 5
IDLE_DURATION: int = 5
CYCLE_INTERVAL: int = CPU_HOLD_DURATION + RAM_HOLD_DURATION + IDLE_DURATION
RAM_ALLOCATION_MB: int = 500  # approx RAM usage per cycle

def hold_cpu(duration: int) -> None:
    end_time: float = time.time() + duration
    while time.time() < end_time:
        pass  # Busy-wait to consume CPU

def hold_ram(size_mb: int, duration: int) -> None:
    block: list[bytes] = [b'x' * 1024 * 1024 for _ in range(size_mb)]  # Allocate RAM
    time.sleep(duration)
    del block  # Release RAM

def stress_cycle() -> None:
    while True:
        print("Starting CPU stress...")
        cpu_thread: threading.Thread = threading.Thread(target=hold_cpu, args=(CPU_HOLD_DURATION,))
        cpu_thread.start()

        print(f"Allocating {RAM_ALLOCATION_MB}MB RAM...")
        hold_ram(RAM_ALLOCATION_MB, RAM_HOLD_DURATION)

        cpu_thread.join()
        print("Releasing resources, going idle...\n")
        time.sleep(IDLE_DURATION)

if __name__ == "__main__":
    print(f"Starting stress cycle: every {CYCLE_INTERVAL} seconds (CPU + RAM + idle)...\n")
    stress_cycle()


# from concurrent.futures import ProcessPoolExecutor
# import time

# def cpu_task(duration: int):
#     end = time.time() + duration
#     while time.time() < end:
#         pass

# def simulate_parallel_service(duration: int, num_tasks: int):
#     print(f"Simulating service with {num_tasks} parallel tasks...")
#     with ProcessPoolExecutor(max_workers=num_tasks) as executor:
#         futures = [executor.submit(cpu_task, duration) for _ in range(num_tasks)]
#         for future in futures:
#             future.result()
#     print("Service tasks complete.\n")

# if __name__ == "__main__":
#     while True:
#         simulate_parallel_service(5, 8)  # 8 cores
#         print("Service going idle...\n")
#         time.sleep(5)
