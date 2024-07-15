import configparser
import subprocess
from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live
from time import sleep
import os

bootloader_ver = "Alpha 1.0.1.5"

console = Console()

spinner_styles = [
    "bouncingBar"
]

for style in spinner_styles:
    spinner = Spinner(style, text=f"Loading Bootloader...")
    with Live(spinner, console=console, refresh_per_second=10):
        sleep(5)

console.clear()
console.print(f"Bootloader Version: {bootloader_ver}")
console.print("==============================")

Load_status_complete = "Load_Complete_✅"
Load_status_Error = "Load_Error_❌"
Script_Status_Stopped = "Script_Stopped_⚠️"

def load_scripts(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    processes = {}
    if 'Scripts' in config:
        scripts = config['Scripts']
        for name, value in scripts.items():
            parts = value.split(',')
            path = parts[0].strip().strip('"')  # Получаем путь к скрипту
            auto_r = parts[1].strip().strip('"') if len(parts) > 1 else "auto_r:n"  # Получаем параметр auto_r, если он есть, иначе по умолчанию "auto_r:n"
            absolute_path = os.path.abspath(path)
            auto_r_flag = auto_r.lower() == 'auto_r:y'
            display_name = os.path.basename(absolute_path)  # Получаем только имя файла

            # Проверяем расширение файла
            if not absolute_path.lower().endswith('.py'):
                console.print(f"{display_name} {Load_status_Error}: Not a Python script.")
                continue

            console.print(f"Loading {display_name}")
            try:
                process = subprocess.Popen(["python", absolute_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
                processes[process.pid] = (process, name, absolute_path, auto_r_flag)
                console.print(f"{Load_status_complete}")
            except Exception as e:
                console.print(f"{display_name} {Load_status_Error}: {str(e)}")
                processes[process.pid] = (None, name, absolute_path, auto_r_flag)  # Добавляем пустой кортеж в список

    else:
        console.print("No scripts found in the configuration file.")
    return processes

def monitor_processes(processes):
    while True:
        try:
            if not processes:  # Если список процессов пустой
                console.print("No more scripts to run. Exiting Bootloader in 10 seconds...")
                sleep(10)
                break
            
            for pid, (process, name, path, auto_r) in list(processes.items()):
                if process is not None:
                    retcode = process.poll()
                    if retcode is not None:  # Process has finished.
                        del processes[pid]
                        if retcode == 0:  # Завершено успешно
                            console.print(f"{os.path.basename(path)} {Load_status_complete}")
                            if auto_r:
                                console.print(f"Restarting {os.path.basename(path)} in 5 seconds...")
                                sleep(5)
                                console.print(f"Restarting {os.path.basename(path)} now...")
                                try:
                                    new_process = subprocess.Popen(["python", path], creationflags=subprocess.CREATE_NEW_CONSOLE)
                                    processes[new_process.pid] = (new_process, name, path, auto_r)
                                    console.print(f"{Load_status_complete}")
                                except Exception as e:
                                    console.print(f"{os.path.basename(path)} {Load_status_Error}: {str(e)}")
                            else:
                                console.print(f"{os.path.basename(path)} {Script_Status_Stopped}")
                        else:  # Процесс завершился с ошибкой или остановился
                            console.print(f"{os.path.basename(path)} {Script_Status_Stopped}")
                            if auto_r:
                                console.print(f"Restarting {os.path.basename(path)} in 5 seconds...")
                                sleep(5)
                                console.print(f"Restarting {os.path.basename(path)} now...")
                                try:
                                    new_process = subprocess.Popen(["python", path], creationflags=subprocess.CREATE_NEW_CONSOLE)
                                    processes[new_process.pid] = (new_process, name, path, auto_r)
                                    console.print(f"{Load_status_complete}")
                                except Exception as e:
                                    console.print(f"{os.path.basename(path)} {Load_status_Error}: {str(e)}")
                else:
                    console.print(f"{os.path.basename(path)} {Load_status_Error}: Failed to start the process.")
                    del processes[pid]  # Удаляем процесс из списка, если не удалось его запустить

            sleep(10)
        except KeyboardInterrupt:
            console.print("Exiting Bootloader.")
            break

processes = load_scripts("Config.cfg")
monitor_processes(processes)
