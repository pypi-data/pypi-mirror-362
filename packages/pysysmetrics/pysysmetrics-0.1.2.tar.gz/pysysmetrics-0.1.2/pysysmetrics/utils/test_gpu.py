import time
import torch
import threading

GPU_HOLD_DURATION: int = 5
IDLE_DURATION: int = 5
CYCLE_INTERVAL: int = GPU_HOLD_DURATION + IDLE_DURATION
TENSOR_SIZE: int = 4096  # Adjust size to increase/decrease GPU load

def hold_gpu(duration: int) -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if device.type != "cuda":
        print("CUDA GPU not available. Exiting...")
        return

    end_time: float = time.time() + duration
    a = torch.randn((TENSOR_SIZE, TENSOR_SIZE), device=device)
    b = torch.randn((TENSOR_SIZE, TENSOR_SIZE), device=device)

    print(f"Starting GPU stress for {duration} seconds...")
    while time.time() < end_time:
        c = torch.mm(a, b)  # Matrix multiplication (loads GPU)
        # Prevent optimization by reading a value
        _ = c[0, 0].item()

    # Cleanup
    del a, b, c
    torch.cuda.empty_cache()
    print("Finished GPU stress, resources released.")

def stress_cycle() -> None:
    while True:
        gpu_thread = threading.Thread(target=hold_gpu, args=(GPU_HOLD_DURATION,))
        gpu_thread.start()
        gpu_thread.join()

        print("Idle...")
        time.sleep(IDLE_DURATION)

if __name__ == "__main__":
    print(f"Starting GPU stress cycle: every {CYCLE_INTERVAL} seconds (GPU + idle)...\n")
    stress_cycle()
