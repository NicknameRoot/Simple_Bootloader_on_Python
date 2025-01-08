import configparser
import subprocess
from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live
from rich.text import Text
from time import sleep
import os
import logging
from datetime import datetime
import base64

# Логотип загрузчика
encoded_logo = (
    "CiAvJCQgICAvJCQgLyQkJCQkJCQgICAgICAgICAgICAgICAgICAgICAgLyQkICAgLyQkIC8k"
    "JCQkJCQKfCAkJCQgfCAkJHwgJCRfXyAgJCQgICAgICAgICAgICAgICAgICAgIHwgJCQgIHwg"
    "JCR8XyAgJCRfLwp8ICQkJCR8ICQkfCAkJCAgXCAkJCAgLyQkJCQkJCQgICAgICAgICAgfCAk"
    "JCAgfCAkJCAgfCAkJCAgCnwgJCQgJCQgJCR8ICQkJCQkJCQvIC8kJF9fX19fLyAgICAgICAg"
    "ICB8ICQkICB8ICQkICB8ICQkICAKfCAkJCAgJCQkJHwgJCRfXyAgJCR8ICQkICAgICAgICAg"
    "ICAgICAgIHwgJCQgIHwgJCQgIHwgJCQgIAp8ICQkXCAgJCQkfCAkJCAgXCAkJHwgJCQgICAg"
    "ICAgICAgICAgICAgfCAkJCAgfCAkJCAgfCAkJCAgCnwgJCQgXCAgJCR8ICQkICB8ICQkfCAg"
    "JCQkJCQkJCAvJCQgICAgICB8ICAkJCQkJCQvIC8kJCQkJCQKfF9fLyAgXF9fL3xfXy8gIHxf"
    "Xy8gXF9fX19fX18vfF9fLyAgICAgICBcX19fX19fLyB8X19fX19fLwo="
)
bootloader_logo = base64.b64decode(encoded_logo).decode('utf-8')


# Авторская информация

encoded_author = "Tmlja25hbWVfUm9vdA=="
encoded_company_name = "Tm9ya2FfQ29tcGFueV/wn5C+"
Author = base64.b64decode(encoded_author).decode('utf-8')
Company_name = base64.b64decode(encoded_company_name).decode('utf-8')

# Версия загрузчика
bootloader_ver = "Alpha 1.0.1.8"

# Настройка логирования
current_dir = os.path.dirname(os.path.abspath(__file__))  # Директория с .py файлом загрузчика
log_folder = os.path.join(current_dir, "Logs")
current_date = datetime.now().strftime("%m-%d-%Y")
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
                    datefmt='%m-%d-%Y %H:%M:%S')

# Логирование старта загрузчика
logging.info("Bootloader started.")

console = Console()

spinner_styles = ["bouncingBar"]

for style in spinner_styles:
    spinner = Spinner(style, text=f"Loading Bootloader...")
    with Live(spinner, console=console, refresh_per_second=10):
        sleep(5)

console.clear()
console.print("====================================================================")
console.print(bootloader_logo)
console.print("====================================================================")
console.print(f"Bootloader Version: {bootloader_ver}")
console.print(f"\nAuthor: [bold #FF0000]{Author}[/bold #FF0000] \nCompany: [bold #FFA500]{Company_name}[/bold #FFA500]")
console.print("====================================================================")

Load_status_complete = "Load_Complete_✅"
Load_status_Error = "Load_Error_❌"
Script_Status_Stopped = "Script_Stopped_⚠️"

def load_scripts(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    processes = {}
    if 'Scripts' in config:
        scripts = config['Scripts']
        if not scripts:
            console.print("No scripts found in the configuration file.")
            logging.warning("No scripts found in the configuration file.")
        for name, value in scripts.items():
            parts = value.split(',')
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
        console.print("No scripts found in the configuration file.")
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
