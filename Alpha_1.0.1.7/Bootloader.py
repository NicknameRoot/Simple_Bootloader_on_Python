import configparser
import subprocess
from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live
from time import sleep
import os
import logging
from datetime import datetime

# Версия загрузчика
bootloader_ver = "Alpha 1.0.1.7"

# Настройка логирования
current_dir = os.path.dirname(os.path.abspath(__file__))  # Директория с .py файлом загрузчика
log_folder = os.path.join(current_dir, "Logs")
current_date = datetime.now().strftime("%d-%m-%Y")
log_dir = os.path.join(log_folder, current_date)

# Проверяем и создаем папку для логов, если она не существует
try:
    os.makedirs(log_dir, exist_ok=True)
except Exception as e:
    print(f"Error creating log directory: {e}")

log_file = os.path.join(log_dir, "debug.log")

logging.basicConfig(filename=log_file, 
                    level=logging.DEBUG, 
                    format='[%(asctime)s] %(message)s', 
                    datefmt='%d-%m-%Y %H:%M:%S')

# Логирование старта загрузчика
logging.info("Bootloader started.")

console = Console()

spinner_styles = ["bouncingBar"]

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
    
    try:
        config.read(config_file)
    except Exception as e:
        console.print(f"Error reading configuration file: {e}")
        logging.error(f"Error reading configuration file: {e}")
        return {}

    processes = {}
    
    # Проверка на наличие секции 'Scripts'
    if 'Scripts' in config:
        scripts = config.items('Scripts')
        
        if not scripts:
            console.print("No scripts found in the configuration file.")
            logging.warning("No scripts found in the configuration file.")
        else:
            for name, value in scripts:
                parts = value.split(',')
                
                # Проверяем, что в конфигурации правильно указаны все значения
                if len(parts) < 1:
                    console.print(f"Configuration error for script '{name}' - missing parameters.")
                    logging.error(f"Configuration error for script '{name}' - missing parameters.")
                    continue

                path = parts[0].strip().strip('"')
                auto_r = parts[1].strip().strip('"') if len(parts) > 1 else "auto_r:n"
                absolute_path = os.path.abspath(path)
                auto_r_flag = auto_r.lower() == 'auto_r:y'
                display_name = os.path.basename(absolute_path)

                # Проверка расширения файла
                if not absolute_path.lower().endswith('.py'):
                    console.print(f"{display_name} {Load_status_Error}: Not a Python script.")
                    logging.error(f"{display_name} failed to load: Not a Python script.")
                    console.print("Logs saved in folder [Logs]")
                    continue

                console.print(f"Loading {display_name}")
                logging.info(f"Loading {display_name}")
                try:
                    process = subprocess.Popen(["python", absolute_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
                    processes[process.pid] = (process, name, absolute_path, auto_r_flag)
                    console.print(f"{Load_status_complete}")
                    logging.info(f"{display_name} loaded successfully")
                except Exception as e:
                    console.print(f"{display_name} {Load_status_Error}: {str(e)}")
                    logging.error(f"{display_name} failed to load: {str(e)}")
                    console.print("Logs saved in folder [Logs]")
                    processes[process.pid] = (None, name, absolute_path, auto_r_flag)
    
    else:
        console.print("No 'Scripts' section found in the configuration file.")
        logging.warning("No 'Scripts' section found in the configuration file.")
    
    return processes

def monitor_processes(processes):
    while True:
        try:
            if not processes:
                console.print("No more scripts to run. Exiting Bootloader in 10 seconds...")
                logging.info("No more scripts to run. Bootloader will exit in 10 seconds.")
                sleep(10)
                logging.info("Bootloader exited.")
                break
            
            for pid, (process, name, path, auto_r) in list(processes.items()):
                if process is not None:
                    retcode = process.poll()
                    if retcode is not None:
                        del processes[pid]
                        if retcode == 0:
                            console.print(f"{os.path.basename(path)} {Load_status_complete}")
                            logging.info(f"{os.path.basename(path)} completed successfully.")
                            if auto_r:
                                console.print(f"Restarting {os.path.basename(path)} in 5 seconds...")
                                logging.info(f"Restarting {os.path.basename(path)} in 5 seconds.")
                                sleep(5)
                                try:
                                    new_process = subprocess.Popen(["python", path], creationflags=subprocess.CREATE_NEW_CONSOLE)
                                    processes[new_process.pid] = (new_process, name, path, auto_r)
                                    console.print(f"{Load_status_complete}")
                                    logging.info(f"{os.path.basename(path)} restarted successfully.")
                                except Exception as e:
                                    console.print(f"{os.path.basename(path)} {Load_status_Error}: {str(e)}")
                                    logging.error(f"{os.path.basename(path)} failed to restart: {str(e)}")
                                    console.print("Logs saved in folder [Logs]")
                            else:
                                console.print(f"{os.path.basename(path)} {Script_Status_Stopped}")
                                logging.info(f"{os.path.basename(path)} stopped.")
                        else:
                            console.print(f"{os.path.basename(path)} {Script_Status_Stopped}")
                            logging.info(f"{os.path.basename(path)} stopped with error code {retcode}.")
                            if auto_r:
                                console.print(f"Restarting {os.path.basename(path)} in 5 seconds...")
                                logging.info(f"Restarting {os.path.basename(path)} in 5 seconds.")
                                sleep(5)
                                try:
                                    new_process = subprocess.Popen(["python", path], creationflags=subprocess.CREATE_NEW_CONSOLE)
                                    processes[new_process.pid] = (new_process, name, path, auto_r)
                                    console.print(f"{Load_status_complete}")
                                    logging.info(f"{os.path.basename(path)} restarted successfully.")
                                except Exception as e:
                                    console.print(f"{os.path.basename(path)} {Load_status_Error}: {str(e)}")
                                    logging.error(f"{os.path.basename(path)} failed to restart: {str(e)}")
                                    console.print("Logs saved in folder [Logs]")
                else:
                    console.print(f"{os.path.basename(path)} {Load_status_Error}: Failed to start the process.")
                    logging.error(f"{os.path.basename(path)} failed to start.")
                    console.print("Logs saved in folder [Logs]")
                    del processes[pid]

            sleep(10)
        except KeyboardInterrupt:
            console.print("Exiting Bootloader.")
            logging.info("Bootloader interrupted and exited by user.")
            break

processes = load_scripts("Config.cfg")
monitor_processes(processes)

# Логирование завершения работы загрузчика, если не было скриптов
if not processes:
    logging.info("Bootloader exited: No scripts to load.")
