# Справочник настроек нод (Price Monitor V14.0 - SIMPLE PARALLEL)

Этот документ описывает упрощенную архитектуру воркфлоу с параллельной обработкой 10 магазинов одновременно. Система фокусируется исключительно на сборе цен.

---

## 🏗 Общая архитектура (10-Batch Pricing)
- **Concurrency**: Мы обрабатываем по 10 задач одновременно, что дает 10-кратное ускорение.
- **Data Integrity**: Метаданные (shop, product) передаются через всю цепочку, гарантируя запись цены в правильную ячейку.

---

## 1. Read URLs (Google Sheets)
- **Node Type**: `n8n-nodes-base.googleSheets`
- **Operation**: `Read`
- **Document ID**: `1W0LEztgC8mm3xTXbcA4JsYvlbG64QmHAMHegamKcLmk`
- **Sheet Name**: `Посилання`
- **Options**: `Range` (A1:Z500)
- **Purpose**: Извлекает ссылки и селекторы цен.

---

## 2. Unpivot Matrix (Interleaved)
- **Node Type**: `n8n-nodes-base.code`
- **Mode**: `Run Once for All Items`
- **JavaScript Code**:
```javascript
const items = $input.all();
const output = [];

if (items.length === 0) return [];

const allKeys = new Set();
items.forEach(item => Object.keys(item.json).forEach(key => allKeys.add(key)));

const isServiceKey = (k) => {
    const s = k.toLowerCase().trim();
    return s.includes('магазин') || s.includes('селектор') || s.includes('shop') || s.includes('selector') || s === 'id' || s === 'row_number';
};

const productColumns = Array.from(allKeys).filter(k => !isServiceKey(k));

for (const product of productColumns) {
    for (const row of items) {
        const d = row.json;
        const url = (d[product] || '').toString().trim();
        
        const selectorKey = Object.keys(d).find(k => {
            const lowKey = k.toLowerCase().trim();
            return lowKey.includes('селектор') || lowKey.includes('selector');
        });
        
        const selector = selectorKey ? (d[selectorKey] || '').toString().trim() : '';
        const shopKey = Object.keys(d).find(k => k.toLowerCase().includes('магазин') || k.toLowerCase().includes('shop'));

        if (url.startsWith('http') && selector.length > 0) {
            output.push({
                json: {
                    shop: (d[shopKey] || 'Unknown').toString().trim(),
                    selector: selector,
                    product: product.trim(),
                    url: url
                }
            });
        }
    }
}
return output;
```

---

## 3. Loop (Stealth Parallel)
- **Node Type**: `n8n-nodes-base.splitInBatches`
- **Batch Size**: `10`
- **Purpose**: Обработка пачками по 10 магазинов.

---

## 4. Scrape Price (HTTP Request)
- **Method**: `POST`
- **URL**: `http://browserless:3000/scrape`
- **Body Content Type**: `JSON`
- **Body Settings**:
```json
{
  "url": "={{ $json.url }}",
  "elements": [{ "selector": "={{ $json.selector }}" }],
  "gotoOptions": { "waitUntil": "networkidle2" }
}
```
- **Options (КРИТИЧЕСКИ ВАЖНО)**:
    - **Put Response in Field**: `true` (Включить, чтобы не потерять название магазина!)
    - **Response Data FieldName**: `scrapeData`
    - **Timeout**: `90000`
- **Retry on Fail**: `On` (перезапуск при сбоях)

---

## 5. Wait (Random Batch)
- **Wait Time**: `={{ Math.floor(Math.random() * (75 - 5 + 1)) + 5 }}`
- **Description**: Пауза после каждой пачки из 10 запросов.

---

## 6. Process & Pivot (Zero-Filter)
- **Node Type**: `n8n-nodes-base.code`
- **Mode**: `Run Once for All Items`
- **Описание логики агрегации**:
    В n8n ноды внутри цикла (`Split In Batches`) хранят свои данные в разных «прогонах» (iterations). Чтобы собрать данные со всех 100 товаров после завершения цикла, мы используем следующий алгоритм:
    1. **Цикл по итерациям**: Мы узнаем количество батчей через `$(loopNode).runIndex`.
    2. **Сбор (Collection)**: Для каждого батча мы явно запрашиваем массив элементов из ноды `Wait (Random)`.
    3. **Группировка (Grouping)**: Создаем объект `groupedByShop`, где ключом является название магазина. Это позволяет «схлопнуть» 100 товаров в 10 строк (по одной на магазин).
    4. **Парсинг цены**: Берем текст до слова "грн", чтобы исключить вторую валюту, и преобразуем в число.

- **JavaScript Code**:
```javascript
// 1. Получаем 100 оригинальных записей с магазинами и моделями из самого начала цепочки
const originals = $("Unpivot Matrix (Interleaved)").all();

// 2. Получаем 100 спарсенных ответов, которые выдал цикл прямо на вход (ветка Done)
const allScraped = $input.all();

const groupedByShop = {};

for (let i = 0; i < originals.length; i++) {
  const shop = (originals[i].json.shop || "Unknown").toString().trim();
  const product = (originals[i].json.product || "Unknown").toString().trim();
  
  if (shop === "Unknown") continue;
  
  // 1. Название магазина - одна коллекция элементов
  if (!groupedByShop[shop]) {
    groupedByShop[shop] = { "Магазин": shop };
  }

  // Если ответа по какой-то причине нет
  if (!allScraped[i] || !allScraped[i].json) continue;
  
  const scrapeJson = allScraped[i].json;
  const dataArray = scrapeJson.data || [];
  let foundPrice = null;
  
  // Глубокий поиск цены внутри массивов results
  for (const element of dataArray) {
    if (!element.results) continue;
    for (const res of element.results) {
      if (res.text && res.text.trim().length > 0) {
        const raw = res.text.trim();
        // Замена и очистка: отрезает ₴, грн, $ и удаляет пробелы
        const cleanText = raw.split(/грн|\$|₴|€/i)[0];
        const val = parseInt(cleanText.replace(/[^\d]/g, ''));
        
        if (val > 0) {
          foundPrice = val;
          break;
        }
      }
    }
    if (foundPrice) break;
  }

  // 2. Название модели служит ключом для колонки
  // 3. Цена - вставляется значением
  if (foundPrice) {
    groupedByShop[shop][product] = foundPrice;
  }
}

return Object.values(groupedByShop);
```

---

## 7. Диагностика (Troubleshooting)

Если в таблице **пустые строки**:
1. **Проверьте Scrape Price**: В истории выполнения (Execution Log) посмотрите, есть ли в объекте поле `shop`. Если его нет — значит вы не включили **Put Response in Field**.
2. **Проверьте Selector**: Если в `scrapeData -> data[0] -> results` пусто — значит селектор на сайте изменился или не подходит.
3. **Логи**: Код в `Process & Pivot` теперь более устойчив. Если он не находит цену, он просто пропустит ячейку, но не всю строку.


---

## 7. Update Matrix Row (Google Sheets)
- **Sheet**: `Ціни`
- **Operation**: `Append or Update Row`
- **Match on**: `Магазин`
- **Mapping**: `autoMap`
