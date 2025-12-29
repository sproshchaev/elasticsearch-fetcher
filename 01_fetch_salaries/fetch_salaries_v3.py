# Оптимизирован под "US" - "doc_count" : 103 482 311
"""
Скрипт для выгрузки значений поля 'rowSalary' из Elasticsearch по заданным странам.

Особенности:
- Использует один агрегационный запрос для получения точного количества документов для каждой страны.
- Затем делает серию запросов с 'search_after' для получения всех данных.
- Сохраняет данные в файлы в формате 'rowSalaries_<country_code>.txt', добавляя порции (append).
- Использует логирование в файл 'fetch_salaries.log' и вывод в консоль.
- Обрабатывает таймауты и ошибки с повторными попытками.
- Показывает прогресс в формате 'Обработано X из Y (Z%) для XX'.
- Использует небольшой размер порции (BATCH_SIZE) для снижения нагрузки на Elasticsearch.
"""

import requests
import json
import time
import os
import logging

# Настройки
ES_URL = "http://10.0.5.41:9200"
INDEX = "indeed_job_page"
BATCH_SIZE = 200
# COUNTRIES = ["PK", "MY", "ZA", "PE", "PH", "ID", "US", "QA", "TH", "SA"]
COUNTRIES = ["US"]

# Таймауты (в секундах)
REQUEST_TIMEOUT = (10, 30)
MAX_RETRIES = 3
RETRY_DELAY = 2

# --- Настройка логирования ---
LOG_FILE = "fetch_salaries.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# --- Получаем точные количества для всех стран за один запрос ---
def get_total_counts_for_countries():
    """
    Выполняет один агрегационный запрос и возвращает словарь:
    { "PK": 348321, "MY": 220006, ... }
    """
    query_body = {
        "size": 0,
        "query": {
            "bool": {
                "must": [
                    {
                        "exists": {
                            "field": "rowSalary"
                        }
                    },
                    {
                        "terms": {
                            "loc.country_code.keyword": COUNTRIES
                        }
                    }
                ]
            }
        },
        "aggs": {
            "by_country": {
                "terms": {
                    "field": "loc.country_code.keyword",
                    "size": len(COUNTRIES)
                }
            }
        }
    }

    for attempt in range(MAX_RETRIES + 1):
        try:
            response = requests.post(
                f"{ES_URL}/{INDEX}/_search",
                headers={"Content-Type": "application/json"},
                data=json.dumps(query_body),
                timeout=REQUEST_TIMEOUT
            )
            break
        except requests.exceptions.RequestException as e:
            logger.warning(f"Ошибка при получении общего количества (попытка {attempt + 1}): {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY * (2 ** attempt))
                continue
            else:
                logger.error(f"Не удалось получить общее количество: {e}")
                return {}

    if response.status_code != 200:
        logger.error(f"Ошибка HTTP при получении общего количества: {response.status_code}, {response.text}")
        return {}

    result = response.json()
    buckets = result.get("aggregations", {}).get("by_country", {}).get("buckets", [])

    # Формируем словарь: страна -> doc_count
    counts = {bucket["key"]: bucket["doc_count"] for bucket in buckets}
    logger.info(f"Получены точные количества: {counts}")
    return counts


def fetch_all_salaries_by_country(country_code, total_counts):
    """
    Получает все значения rowSalary для указанной страны и сохраняет их в файл по мере получения.
    """
    filename = f"rowSalaries_{country_code}.txt"

    if os.path.exists(filename):
        os.remove(filename)
        logger.info(f"Старый файл {filename} удалён.")

    total_count = total_counts.get(country_code, 0)
    if total_count == 0:
        logger.warning(f"Не удалось получить общее количество для {country_code}, пропускаем.")
        return

    logger.info(f"Начинаем обработку {country_code}. Всего записей: {total_count}")

    all_salaries_count = 0
    search_after = None

    while True:
        query_body = {
            "_source": ["rowSalary"],
            "query": {
                "bool": {
                    "filter": [
                        {
                            "term": {
                                "loc.country_code.keyword": country_code
                            }
                        },
                        {
                            "exists": {
                                "field": "rowSalary"
                            }
                        }
                    ]
                }
            },
            "sort": [
                {
                    "id.keyword": {
                        "order": "asc"
                    }
                }
            ],
            "size": BATCH_SIZE
        }

        if search_after:
            query_body["search_after"] = search_after

        response = None
        for attempt in range(MAX_RETRIES + 1):
            try:
                response = requests.post(
                    f"{ES_URL}/{INDEX}/_search",
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(query_body),
                    timeout=REQUEST_TIMEOUT
                )
                break
            except requests.exceptions.ConnectTimeout:
                logger.warning(f"Таймаут подключения при запросе для {country_code} (попытка {attempt + 1})")
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY * (2 ** attempt))
                    continue
                else:
                    logger.error(f"Превышено количество попыток подключения для {country_code}")
                    return
            except requests.exceptions.ReadTimeout:
                logger.warning(f"Таймаут чтения при запросе для {country_code} (попытка {attempt + 1})")
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY * (2 ** attempt))
                    continue
                else:
                    logger.error(f"Превышено количество попыток чтения для {country_code}")
                    return
            except requests.exceptions.RequestException as e:
                logger.warning(f"Ошибка запроса для {country_code} (попытка {attempt + 1}): {e}")
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY * (2 ** attempt))
                    continue
                else:
                    logger.error(f"Превышено количество попыток для {country_code}: {e}")
                    return

        if response is None:
            logger.error(f"Не удалось получить ответ для {country_code}.")
            break

        if response.status_code != 200:
            logger.error(f"Ошибка HTTP при запросе для {country_code}: {response.status_code}, {response.text}")
            break

        result = response.json()

        hits = result.get("hits", {}).get("hits", [])
        if not hits:
            logger.info(f"Больше нет результатов для {country_code}. Завершаем.")
            break

        new_salaries_count = 0
        with open(filename, "a", encoding="utf-8") as f:
            for hit in hits:
                source = hit.get("_source", {})
                salary = source.get("rowSalary")
                if salary:
                    f.write(salary + "\n")
                    new_salaries_count += 1
                    all_salaries_count += 1

        # --- Выводим прогресс ---
        progress_percent = (all_salaries_count / total_count) * 100 if total_count > 0 else 0
        message = f"Обработано {all_salaries_count} из {total_count} ({progress_percent:.2f}%) для {country_code}"
        print(message)
        logger.info(message)

        last_hit = hits[-1]
        search_after = last_hit.get("sort")

    logger.info(f"Итого сохранено {all_salaries_count} записей в {filename}")


def main():
    logger.info("=== Начало выполнения скрипта ===")

    # Получаем точные количества для всех стран
    total_counts = get_total_counts_for_countries()
    if not total_counts:
        logger.error("Не удалось получить общие количества. Завершаем работу.")
        return

    for country in COUNTRIES:
        logger.info(f"--- Обработка страны: {country} ---")
        print(f"\n--- Обработка страны: {country} ---")
        try:
            fetch_all_salaries_by_country(country, total_counts)
        except Exception as e:
            logger.error(f"Критическая ошибка при обработке страны {country}: {e}")
            print(f"Критическая ошибка при обработке страны {country}: {e}")

    logger.info("=== Завершение выполнения скрипта ===")


if __name__ == "__main__":
    main()