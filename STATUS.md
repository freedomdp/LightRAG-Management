# 📊 Живой Статус LightRAG (V15.7 "Honest & Clean")
Обновлено: `2026-04-11 00:20:43` (Авто-обновление: 60 сек)

## 🕹️ Панель Управления
- **ПАУЗА (Безопасная)**: `./scripts/pause.sh`
- **ПРОДОЛЖИТЬ**: `./scripts/resume.sh`

## ⚡ Статус Индексации: ⌛ Завершение (Ждем высвобождения GPU...)
- **Реальная обработка (Neo4j)**: `[241/442]` (54.52%)
- **Активность LLM (GPU/Ollama)**: 💤 LLM простаивает

### 🖥️ Системные ресурсы (Docker & Mac)
| Компонент / Контейнер | Нагрузка (CPU %) | RAM / Mem | Статус |
| :--- | :--- | :--- | :--- |
| **Ollama (Metal GPU)** | 5.3% | N/A | ✅ Active |
| **LightRAG API** | 0.58% | 485.7MiB | ✅ Online |
| **Neo4j DB** | 2.28% | 975.2MiB | ✅ Online |
| **Qdrant DB** | 13.14% | 267MiB | ✅ Online |

---

## 📜 Недавняя активность (Самые новые - сверху)
```text
[00:06:21] INFO - [SYSTEM] >>> PAUSE REQUESTED BY USER
[22:29:04] INFO - [SYSTEM] ||| SOFT PAUSE ACHIEVED. SAFE TO SLEEP. Stopping ingestion loop.
[22:29:03] INFO - [SYSTEM] >>> PAUSE REQUESTED BY USER
[22:29:03] INFO - Processing: docs/notebook_content/new_1f797b28_e789_434e_ab70_95a3ca29d610_part3.md
[22:29:02] INFO - Processing: docs/notebook_content/new_1f797b28_e789_434e_ab70_95a3ca29d610_part2.md
[22:29:01] INFO - Processing: docs/notebook_content/new_1f797b28_e789_434e_ab70_95a3ca29d610_part1.md
[22:29:00] INFO - Processing: docs/notebook_content/new_1a7fb0c0_b383_4edf_abbe_04901e60fe13_part4.md
[22:28:59] INFO - Processing: docs/notebook_content/new_1a7fb0c0_b383_4edf_abbe_04901e60fe13_part3.md
[22:28:58] INFO - Processing: docs/notebook_content/new_1a7fb0c0_b383_4edf_abbe_04901e60fe13_part2.md
[22:28:57] INFO - Processing: docs/notebook_content/new_1a7fb0c0_b383_4edf_abbe_04901e60fe13_part1.md
[22:28:56] INFO - Processing: docs/notebook_content/new_100_hours_of_AntiGravity_lessons_in_47_minutes_part8.md
[22:28:55] INFO - Processing: docs/notebook_content/new_100_hours_of_AntiGravity_lessons_in_47_minutes_part7.md
[22:28:54] INFO - Processing: docs/notebook_content/new_100_hours_of_AntiGravity_lessons_in_47_minutes_part6.md
[22:28:53] INFO - Processing: docs/notebook_content/new_100_hours_of_AntiGravity_lessons_in_47_minutes_part5.md
[22:28:52] INFO - Processing: docs/notebook_content/new_100_hours_of_AntiGravity_lessons_in_47_minutes_part4.md
[22:28:51] INFO - Processing: docs/notebook_content/new_100_hours_of_AntiGravity_lessons_in_47_minutes_part3.md
[22:28:50] INFO - Processing: docs/notebook_content/new_100_hours_of_AntiGravity_lessons_in_47_minutes_part2.md
[22:28:49] INFO - Processing: docs/notebook_content/new_100_hours_of_AntiGravity_lessons_in_47_minutes_part1.md
[22:28:48] INFO - Processing: docs/notebook_content/new_05f1ac8e_be1e_424b_b453_bdbae9b7dc9b.md
[22:28:47] INFO - Processing: docs/notebook_content/new_05b3ab0c_130d_43d1_bbb6_4cab6471bfa9_part3.md
[22:28:46] INFO - Processing: docs/notebook_content/new_05b3ab0c_130d_43d1_bbb6_4cab6471bfa9_part2.md
[22:28:45] INFO - Processing: docs/notebook_content/new_05b3ab0c_130d_43d1_bbb6_4cab6471bfa9_part1.md
```

> [!TIP]
> Статус "На Паузе" появится только когда GPU физически остынет. Новые события в логах теперь отображаются мгновенно в начале списка.
