Необходимо установить библиотеку requests

1. Извлечение данных из Elasticsearch:  
- [fetch_salaries.py](fetch_salaries.py)       - до 1 млн. документов
- [fetch_salaries_v2.py](fetch_salaries_v2.py) - до 1 млн. документов 
- [fetch_salaries_v3.py](fetch_salaries_v3.py) - если более 1 млн документов 

2. Формирование уникальных шаблонов по извлеченным данным п.1


В Terminal в PyCharm:
```bash
pip install requests
```
Пример:
```txt
(.venv) sergeyproshchaev@Mac-mini-Sergey elasticsearch-fetcher % pip install requests
Collecting requests
  Using cached requests-2.32.5-py3-none-any.whl.metadata (4.9 kB)
Collecting charset_normalizer<4,>=2 (from requests)
  Using cached charset_normalizer-3.4.4-cp312-cp312-macosx_10_13_universal2.whl.metadata (37 kB)
Collecting idna<4,>=2.5 (from requests)
  Using cached idna-3.11-py3-none-any.whl.metadata (8.4 kB)
Collecting urllib3<3,>=1.21.1 (from requests)
  Using cached urllib3-2.5.0-py3-none-any.whl.metadata (6.5 kB)
Collecting certifi>=2017.4.17 (from requests)
  Using cached certifi-2025.10.5-py3-none-any.whl.metadata (2.5 kB)
Using cached requests-2.32.5-py3-none-any.whl (64 kB)
Using cached charset_normalizer-3.4.4-cp312-cp312-macosx_10_13_universal2.whl (208 kB)
Using cached idna-3.11-py3-none-any.whl (71 kB)
Using cached urllib3-2.5.0-py3-none-any.whl (129 kB)
Using cached certifi-2025.10.5-py3-none-any.whl (163 kB)
Installing collected packages: urllib3, idna, charset_normalizer, certifi, requests
Successfully installed certifi-2025.10.5 charset_normalizer-3.4.4 idna-3.11 requests-2.32.5 urllib3-2.5.0

[notice] A new release of pip is available: 25.1.1 -> 25.2
[notice] To update, run: pip install --upgrade pip
```