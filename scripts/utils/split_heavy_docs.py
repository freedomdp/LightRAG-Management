import os
import json
import shutil
from pathlib import Path

# Конфигурация
DOCS_DIR = Path("docs/notebook_content")
BACKUP_DIR = Path("docs/heavy_backup")
SIZE_THRESHOLD = 20 * 1024  # 20 KB
CHUNK_CHAR_LIMIT = 8000     # Лимит символов на один новый файл

def split_file(file_path):
    print(f"📦 Обработка тяжелого файла: {file_path.name}")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            content = data.get("content", "")
            title = data.get("title", file_path.stem)
            source_type = data.get("source_type", "split_doc")
    except (json.JSONDecodeError, KeyError):
        # Если это не JSON, читаем как обычный текст
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            title = file_path.stem
            source_type = "text"

    if not content:
        print(f"⚠️ Файл {file_path.name} пуст или не содержит контента.")
        return []

    # Дробление
    parts = []
    for i in range(0, len(content), CHUNK_CHAR_LIMIT):
        part_content = content[i : i + CHUNK_CHAR_LIMIT]
        part_name = f"{file_path.stem}_part{len(parts)+1}.md"
        part_path = DOCS_DIR / part_name
        
        # Создаем новый JSON-совместимый файл (чтобы API понимал формат)
        part_data = {
            "title": f"{title} (Часть {len(parts)+1})",
            "content": part_content,
            "source_type": source_type
        }
        
        with open(part_path, "w", encoding="utf-8") as f:
            json.dump(part_data, f, ensure_ascii=False, indent=2)
        
        parts.append(part_path)
        print(f"   ✅ Создана часть: {part_name} ({len(part_content)} симв.)")

    # Бекап оригинала
    BACKUP_DIR.mkdir(exist_ok=True)
    shutil.move(file_path, BACKUP_DIR / file_path.name)
    print(f"   🚚 Оригинал перемещен в {BACKUP_DIR}")
    
    return parts

def main():
    if not DOCS_DIR.exists():
        print("❌ Директория с документами не найдена.")
        return

    heavy_files = [
        f for f in DOCS_DIR.glob("*.md") 
        if f.stat().st_size > SIZE_THRESHOLD and "_part" not in f.name
    ]

    if not heavy_files:
        print("✨ Тяжелых файлов для дробления не найдено.")
        return

    print(f"🔍 Найдено {len(heavy_files)} тяжелых файлов.")
    
    all_new_parts = []
    for f_path in heavy_files:
        new_parts = split_file(f_path)
        all_new_parts.extend(new_parts)

    print("\n🚀 Все файлы успешно раздроблены.")
    print("Теперь необходимо запустить скрипт загрузки, чтобы добавить новые части в очередь.")

if __name__ == "__main__":
    main()
