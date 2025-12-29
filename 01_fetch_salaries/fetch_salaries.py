# Оптимально для "PE" "doc_count" : 400480
import requests
import json

# Настройки
ES_URL = "http://10.0.5.41:9200"  # URL Elasticsearch
INDEX = "indeed_job_page"         # индекс
BATCH_SIZE = 1000                 # Размер порции (size) для постраничного получения

# Страны из вашей агрегации
COUNTRIES = ["PK", "MY", "ZA", "PE", "PH", "ID", "US", "QA", "TH", "SA"]

def fetch_all_salaries_by_country(country_code):
    """
    Получает все значения rowSalary для указанной страны.
    """
    all_salaries = []
    search_after = None

    while True:
        # Формируем тело запроса
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
                        "order": "asc"  # Используем asc, чтобы корректно работал search_after
                    }
                }
            ],
            "size": BATCH_SIZE
        }

        if search_after:
            query_body["search_after"] = search_after

        # Отправляем запрос
        response = requests.post(
            f"{ES_URL}/{INDEX}/_search",
            headers={"Content-Type": "application/json"},
            data=json.dumps(query_body)
        )

        if response.status_code != 200:
            print(f"Ошибка при запросе для страны {country_code}: {response.status_code}, {response.text}")
            break

        result = response.json()

        hits = result.get("hits", {}).get("hits", [])
        if not hits:
            break

        # Извлекаем rowSalary
        for hit in hits:
            source = hit.get("_source", {})
            salary = source.get("rowSalary")
            if salary:
                all_salaries.append(salary)

        # Обновляем search_after
        last_hit = hits[-1]
        search_after = last_hit.get("sort")

    return all_salaries

def save_salaries_to_file(country_code, salaries):
    """
    Сохраняет список зарплат в файл.
    """
    filename = f"rowSalaries_{country_code}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        for salary in salaries:
            f.write(salary + "\n")
    print(f"Сохранено {len(salaries)} записей в {filename}")

def main():
    for country in COUNTRIES:
        print(f"Обработка страны: {country}")
        salaries = fetch_all_salaries_by_country(country)
        save_salaries_to_file(country, salaries)

if __name__ == "__main__":
    main()