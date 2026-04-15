import os
import json
import zipfile
import shutil
from datetime import datetime
import argparse

# Пути проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STORAGE_DIR = os.path.join(BASE_DIR, "rag_storage")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")

def verify_integrity():
    """Проверка всех JSON файлов в хранилище на корректность структуры."""
    print("🔍 [Integrity Guard] Начинаю проверку целостности данных...")
    if not os.path.exists(STORAGE_DIR):
        print(f"❌ Ошибка: Директория хранилища {STORAGE_DIR} не найдена.")
        return False
    
    files = [f for f in os.listdir(STORAGE_DIR) if f.endswith('.json')]
    corrupted_files = []
    
    for filename in files:
        file_path = os.path.join(STORAGE_DIR, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
            # print(f"✅ {filename}: OK")
        except Exception as e:
            print(f"🚨 ПОВРЕЖДЕНИЕ: {filename} -> {e}")
            corrupted_files.append(filename)
            
    if corrupted_files:
        print(f"\n❌ Найдено поврежденных файлов: {len(corrupted_files)}")
        return False
    
    print("✅ Все файлы хранилища валидны.")
    return True

def create_snapshot(label="manual"):
    """Создание zip-архива текущего состояния хранилища."""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_name = f"rag_storage_backup_{timestamp}_{label}.zip"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    
    print(f"📦 [Backup Manager] Создаю снимок: {backup_name}...")
    
    try:
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(STORAGE_DIR):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, STORAGE_DIR)
                    zipf.write(file_path, arcname)
        print(f"✅ Бэкап успешно создан: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"❌ Ошибка при создании бэкапа: {e}")
        return None

def auto_cleanup(keep_last=7):
    """Удаление старых бэкапов, оставляя только указанное количество."""
    backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.startswith("rag_storage_backup_")], reverse=True)
    if len(backups) > keep_last:
        for old_backup in backups[keep_last:]:
            file_path = os.path.join(BACKUP_DIR, old_backup)
            try:
                os.remove(file_path)
                print(f"🗑️ Удален старый бэкап: {old_backup}")
            except Exception as e:
                print(f"⚠️ Не удалось удалить {old_backup}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Менеджер безопасности LightRAG Storage")
    parser.add_argument("--verify", action="store_true", help="Проверить целостность JSON файлов")
    parser.add_argument("--backup", action="store_true", help="Создать снимок хранилища")
    parser.add_argument("--label", type=str, default="manual", help="Метка для бэкапа")
    parser.add_argument("--cleanup", action="store_true", help="Очистить старые бэкапы")
    
    args = parser.parse_args()
    
    if args.verify:
        if not verify_integrity():
            exit(1)
            
    if args.backup:
        create_snapshot(args.label)
        if args.cleanup:
            auto_cleanup()
