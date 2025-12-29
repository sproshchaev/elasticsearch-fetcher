import re
import os

def extract_unique_templates_by_first_pattern(input_filename, output_filename):
    """
    Извлекает уникальные шаблоны из файла с rowSalary.
    Уникальность определяется по структуре шаблона (числа заменяются на X).
    Сохраняется только первый оригинальный вариант строки с такой структурой.
    """
    seen_templates = set()  # Для отслеживания уникальных шаблонов (с X)
    unique_lines = []       # Для хранения оригинальных строк, соответствующих уникальным шаблонам

    # Проверяем, существует ли входной файл
    if not os.path.exists(input_filename):
        print(f"⚠️ Файл {input_filename} не найден. Пропускаю.")
        return

    with open(input_filename, 'r', encoding='utf-8') as f:
        for line in f:
            original_line = line.strip()  # Сохраняем оригинальную строку
            if not original_line:
                continue  # Пропускаем пустые строки

            # Создаём шаблон, заменяя числа на X
            template = re.sub(r'\d+', 'X', original_line)

            # Проверяем, видели ли мы такой шаблон раньше
            if template not in seen_templates:
                seen_templates.add(template)  # Добавляем шаблон в "уже виденные"
                unique_lines.append(original_line)  # Сохраняем оригинальную строку
            # Если шаблон уже был, просто игнорируем строку

    # Записываем уникальные оригинальные строки в новый файл
    with open(output_filename, 'w', encoding='utf-8') as f:
        for line in unique_lines:
            f.write(line + '\n')

    print(f"  ✅ Найдено {len(unique_lines)} уникальных оригинальных шаблонов для {input_filename}.")
    print(f"  📄 Результат сохранён в {output_filename}")


def main():
    # Страны
    # COUNTRIES = ["PK", "MY", "ZA", "PE", "PH", "ID", "US", "QA", "TH", "SA"]
    # COUNTRIES = ["QA", "SA", "TH"]
    COUNTRIES = ["US"]


    for country in COUNTRIES:
        print(f"\n🚀 Обработка страны: {country}")
        input_file = f"rowSalaries_{country}.txt"
        output_file = f"unique_templates_{country}.txt"
        extract_unique_templates_by_first_pattern(input_file, output_file)

    print("\n🎉 Обработка всех стран завершена.")


if __name__ == "__main__":
    main()