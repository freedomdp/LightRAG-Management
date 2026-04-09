#!/bin/bash
# Скрипт-обертка для запуска MCP с логированием
LOG_FILE="/Users/sergej/StudioProjects/LightRAG/docs/experience/mcp_wrapper.log"

echo "--- MCP Wrapper Start: $(date) ---" >> "$LOG_FILE"
echo "User: $(whoami)" >> "$LOG_FILE"
echo "Path: $PATH" >> "$LOG_FILE"

# Запуск основного скрипта
/usr/local/bin/python3 "/Users/sergej/StudioProjects/LightRAG/scripts/mcp_lightrag.py" 2>> "$LOG_FILE"
