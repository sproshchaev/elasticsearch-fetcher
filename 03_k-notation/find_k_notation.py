import re


def find_k_notation_salaries(input_file, output_file):
    """
    Находит строки с k-нотацией в файле с зарплатами и сохраняет их в отдельный файл.

    Args:
        input_file: Путь к входному файлу с зарплатами
        output_file: Путь к выходному файлу для строк с k-нотацией
    """
    # Паттерн для поиска k-нотации (цифры, возможно с запятыми/точками, затем k/K)
    k_pattern = re.compile(r'\d+(?:[.,]\d+)?\s*[kK]')

    k_notation_salaries = []

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if line:  # Пропускаем пустые строки
                # Ищем k-нотацию в строке
                if k_pattern.search(line):
                    k_notation_salaries.append(line)

        # Записываем найденные строки в выходной файл
        with open(output_file, 'w', encoding='utf-8') as f:
            for salary in k_notation_salaries:
                f.write(salary + '\n')

        # Выводим статистику
        print(f"Обработано строк: {len(lines)}")
        print(f"Найдено строк с k-нотацией: {len(k_notation_salaries)}")
        print(f"Сохранено в файл: {output_file}")

        # Показываем примеры найденных строк
        if k_notation_salaries:
            print("\nПримеры найденных строк с k-нотацией:")
            for i, salary in enumerate(k_notation_salaries[:10]):  # Показываем первые 10
                print(f"  {i + 1}. {salary}")
            if len(k_notation_salaries) > 10:
                print(f"  ... и еще {len(k_notation_salaries) - 10} строк")

    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_file}' не найден.")
    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")


# Альтернативная версия с более строгим паттерном (ищет $ перед k-нотацией)
def find_k_notation_salaries_strict(input_file, output_file):
    """
    Находит строки с k-нотацией в файле с зарплатами (строгая проверка).
    Ищет паттерн типа $1k, $1.5k, $1,000k и т.д.
    """
    # Более строгий паттерн: знак валюты ($, £, € и т.д.), затем число с k/K
    strict_pattern = re.compile(r'[$£€]\d+(?:[.,]\d+)?\s*[kK]')

    k_notation_salaries = []

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if line:
                if strict_pattern.search(line):
                    k_notation_salaries.append(line)

        with open(output_file, 'w', encoding='utf-8') as f:
            for salary in k_notation_salaries:
                f.write(salary + '\n')

        print(f"Найдено строк с k-нотацией (строгий поиск): {len(k_notation_salaries)}")

    except Exception as e:
        print(f"Ошибка: {e}")


# Основная функция
def main():
    input_filename = "rowSalaries_CA.txt"
    output_filename = "k_notation_salaries.txt"

    print("=== Поиск зарплат с k-нотацией ===")

    # Используем обычную версию
    find_k_notation_salaries(input_filename, output_filename)

    # Дополнительно: строгая проверка
    print("\n=== Строгий поиск (с символом валюты) ===")
    find_k_notation_salaries_strict(input_filename, "k_notation_strict.txt")


if __name__ == "__main__":
    main()