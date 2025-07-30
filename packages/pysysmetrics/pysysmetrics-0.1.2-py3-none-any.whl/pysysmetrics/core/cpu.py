import os
import sys
import time
import psutil
import platform
import argparse
from datetime import datetime

def get_python_processes() -> list[dict]:
    python_processes = []
    for process in psutil.process_iter(['pid', 'name', 'memory_info', 'cmdline']):
        try:
            name = process.info['name'].lower()
            cmdline = process.info.get('cmdline', [])
            if 'python' in name or (cmdline and 'python' in cmdline[0].lower()):
                python_processes.append(process.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return python_processes


def convert_bytes_to_megabytes(bytes_size: int) -> float:
    return bytes_size / (1024 ** 2)


def get_script_name_from_cmdline(cmdline: list[str]) -> str:
    for arg in cmdline:
        if arg.endswith('.py'):
            return os.path.basename(arg)
    return "N/A"


def print_python_processes_info(python_processes: list[dict]) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n========================= Refresh @ {timestamp} =========================")
    if not python_processes:
        print("No active Python processes found.")
        return

    print(f"{'PID':<10}{'Script Name':<25}{'CPU %':<10}{'#Threads':<10}{'Memory (MB)':<15}")
    print("-" * 80)

    for process_info in python_processes:
        try:
            proc = psutil.Process(process_info['pid'])
            cpu_percent = proc.cpu_percent(interval=0.1)  # sample usage
            num_threads = proc.num_threads()
            memory_rss = process_info['memory_info'].rss
            mb = convert_bytes_to_megabytes(memory_rss)
            script_name = get_script_name_from_cmdline(process_info.get('cmdline', []))

            print(f"{process_info['pid']:<10}{script_name:<25}{cpu_percent:<10.1f}{num_threads:<10}{mb:<15.2f}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

def print_system_info() -> None:
    os_info = f"{platform.system()} {platform.release()}"
    cpu_model = platform.processor()
    cpu_cores = psutil.cpu_count(logical=True)
    total_ram_gb = psutil.virtual_memory().total / (1024 ** 3)

    print("-" * 70)
    print("System Information:")
    print(f"Operating System : {os_info}")
    print("-" * 70)
    print("CPU Information:")
    print(f"CPU Model        : {cpu_model}")
    print(f"CPU Cores        : {cpu_cores}")
    print(f"Total RAM        : {total_ram_gb:.2f} GB")
    print("-" * 70)


def main():
    parser = argparse.ArgumentParser(description="Monitor running Python processes and memory usage.")
    parser.add_argument("interval", type=int, help="Refresh interval in seconds (positive integer)")
    args = parser.parse_args()

    if args.interval <= 0:
        print("Error: Interval must be a positive integer.")
        sys.exit(1)

    print_system_info()

    while True:
        python_processes = get_python_processes()
        print_python_processes_info(python_processes)
        print("=" * 70)
        time.sleep(args.interval)

def monitor_cpu_memory(interval: int) -> None:
    if interval <= 0:
        print("Error: Interval must be a positive integer.")
        sys.exit(1)

    print_system_info()

    while True:
        python_processes = get_python_processes()
        print_python_processes_info(python_processes)
        print("=" * 70)
        time.sleep(interval)

if __name__ == "__main__":
    main()
