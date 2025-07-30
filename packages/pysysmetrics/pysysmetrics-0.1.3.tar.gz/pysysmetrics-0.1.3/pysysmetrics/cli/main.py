import argparse
from pysysmetrics.core import cpu, gpu

def main() -> None:
    parser = argparse.ArgumentParser(description="Monitor CPU/GPU memory usage of Python processes")
    parser.add_argument("--cpu", type=int, help="Monitor CPU memory usage every N seconds")
    parser.add_argument("--gpu", type=int, help="Monitor GPU memory usage every N seconds")
    args = parser.parse_args()

    if args.cpu:
        cpu.monitor_cpu_memory(interval=args.cpu)
    elif args.gpu:
        gpu.monitor_gpu_memory(interval=args.gpu)
    else:
        parser.print_help()
