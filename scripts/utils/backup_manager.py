import os
import shutil
import time
import subprocess
from datetime import datetime

# Настройки путей
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BACKUP_DIR = os.path.join(PROJECT_ROOT, "backups")
FOLDERS_TO_BACKUP = [
    "rag_storage",
    "neo4j_data",
    "qdrant_data",
    ".env"
]

def create_backup():
    """Создает резервную копию основных данных проекта."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    
    print(f"[*] Начинаю резервное копирование в {backup_name}...")
    
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        
    try:
        # Создаем временную папку для сбора данных
        os.makedirs(backup_path)
        
        for folder in FOLDERS_TO_BACKUP:
            src = os.path.join(PROJECT_ROOT, folder)
            dst = os.path.join(backup_path, folder)
            
            if os.path.exists(src):
                print(f"    - Копирование {folder}...")
                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)
            else:
                print(f"    [!] Предупреждение: {folder} не найден, пропускаю.")
        
        # Архивируем
        archive_path = shutil.make_archive(backup_path, 'zip', backup_path)
        
        # Удаляем временную папку
        shutil.rmtree(backup_path)
        
        print(f"[+] Резервное копирование успешно завершено!")
        print(f"[+] Файл: {archive_path}")
        return archive_path
        
    except Exception as e:
        print(f"[-] Ошибка при создании бэкапа: {str(e)}")
        if os.path.exists(backup_path):
            shutil.rmtree(backup_path)
        return None

if __name__ == "__main__":
    create_backup()
