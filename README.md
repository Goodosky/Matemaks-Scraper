# Matemaks Scraper

Czyli prosty scraper do matemaks.pl z obsługą logowania do matemaks.pl i pobierania danych dostępnych tylko po zalogowaniu.

## Wymagania

#### - Python 3

#### - biblioteka Selenium

- Dokumentacja: https://selenium-python.readthedocs.io/index.html
- Instalacja: `pip install -U selenium`

  Do działania Selenium potrzebny jest też sterownik. Obecna wersja tego scrapera obsługuje domyślnie przeglądarkę Google Chrome, dla której sterowniki znajdziesz [tutaj](https://sites.google.com/a/chromium.org/chromedriver/downloads).

  Jeżeli chcesz odpalić scraper na Firefox, wystarczy w matemaks_scraper.py zamienić linię:

  ```python
  self.browser = webdriver.Chrome()
  ```

  na

  ```python
  self.browser = webdriver.Firefox()
  ```

  oczywiście musisz też mieć wtedy sterownik dla Firefox

## Jak korzystać

#### Zaimportuj scraper

```python
   # Importuje scraper
   from matemaks_scraper import MatemaksScraper

   # Importuje funcje pozwalające wyeksportować dane (opcjonalne)
   from export_functions import *
```

#### Zainicjuj scraper

```python
   # Tworzy nową instancję scrapera
   scraper = MatemaksScraper()

   # Jeżeli nie podano danych logowania do matemaks.pl w config.py
   # to należy podać je podczas inicjalizacji klasy MatemaksScraper
   scraper = MatemaksScraper("login", "haslo")
```

#### Korzystaj z metod

Korzystaj z metod udostępnionych w ramach tego scraper'a.

Dostępne metody:

- [scraper.get_basic_matura_course()](#get_basic_matura_coursekwags)
- [scraper.get_extended_matura_course()](#get_extended_matura_coursekwags)
- [scraper.get_all_matura_course()](#get_all_matura_coursekwargs)
- [scraper.get_all_matura_questions()](#get_all_matura_questionsonly_video_idsfalse)
- [scraper.get_lessons_data(url)](#get_lessons_dataurl-kwargs)
- [scraper.get_questions(url)](#get_questionsurl-only_video_idsfalse)
- [scraper.generate_data_for_matemaks_extension()](#generate_data_for_matemaks_extension)

#### Zamknij otwartą przez scraper przeglądarkę

```python
   # Zamyka przeglądarkę
   scraper.close_browser()

   # Można też tak :)
   del scraper
```

#### Wyeksportuj dane (opcjonalne)

Korzystaj z funkcji pozwalających zapisać uzyskane dane lub utwórz swoje własne rozwiązania.

Dostępne funkcje eksportujące:

- [export_to_json(data)](#export_to_jsondata-file_pathdefault_output_file_path)

#### Uzupełnij dane logowania w config.py (opcjonalne)

Dla łatwiejszego stosowania scraper'a można podać dane logowania do matemaks.pl w pliku config.py:

```python
LOGIN = "[YOUR_LOGIN_TO_MATEMAKS_PL]"
PASSWORD = "[YOUR_PASSWORD_TO_MATEMAKS_PL]"
```

## Metody klasy MatemaksScraper

### get_questions(url, only_video_ids=False)

Zwraca słownik z wszystkimi pytaniami występującymi pod podanym adresem `url`.

Domyślnie zwracane są dane w następującej strukturze:

```javascript
"id": { // id pytania
    "yt": string, // id flimu z odpowiedzią na youtube
    "ans": string, // odpowiedź do pytania (pusty string, string, html lub MathJax)
    "pts": string, // ilość punktów za pytanie
    "data": string, // data
}
```

`only_video_ids` == True spowoduje, że zwrócone dane będą wyglądać następująco:

```javascript
// id pytania: id flimu z odpowiedzią na youtube
"id": "yt"
```

### get_lessons_data(url, \*\*kwargs)

Zwraca słownik z informacjami o lekcjach występujących pod podanym adresem `url`.

Domyślnie zwracane są dane w następującej strukturze:

```javascript
{
    "number of lesson": { // numer lekcji
        "lvl": number, // poziom (1 dla matury podstawowej i 2 dla matury rozszerzonej),
        "yt": string, // id flimu z lekcją na youtube,
        "lesson_url": string, // url z ćwiczeniami do lekcji
        "questions": { // obiekt z pytaniami do lekcji
            "id": { // id pytania
                "yt": string, // id flimu z odpowiedzią na youtube
                "ans": string, // odpowiedź do pytania (pusty string, string, html lub MathJax)
                "pts": string, // ilość punktów za pytanie
                "data": string, // data
            }
            ...
        }
    }
    ...
}
```

`only_questions` == True spowoduje zwrócenie tylko pytań dla każdej lekcji:

```javascript
{
    "number of lesson": { // numer lekcji
        "id": { // id pytania
            "yt": string, // id flimu z odpowiedzią na youtube
            "ans": string, // odpowiedź do pytania (pusty string, string, html lub MathJax)
            "pts": string, // ilość punktów za pytanie
            "data": string, // data
        }
        ...
    }
    ...
}
```

`only_video_ids` == True spowoduje, że zwrócone dane będą wyglądać następująco:

```javascript
    {
    "numer lekcji": "id flimu z lekcją na youtube"
    ...
    }
```

### get_basic_matura_course(\*\*kwags)

Metoda pomocnicza, wywołuje [get_lessons_data()](#get_lessons_dataurl-kwargs) z url strony zawierającej kurs maturalny na poziomie podstawowym.
Adres url tej strony jest zapisany w config.py w stałej `BASIC_MATURA_COURSE_URL`.

Zwraca więc wszystkie informacje o lekcjach z kursu podstawowego. Metoda ta obsługuje flagi dostępne dla [get_lessons_data()](#get_lessons_dataurl-kwargs) (czyli `only_questions` i `only_video_ids`).

### get_extended_matura_course(\*\*kwags)

Metoda pomocnicza, wywołuje [get_lessons_data()](#get_lessons_dataurl-kwargs) z url strony zawierającej kurs maturalny na poziomie rozszerzonym.
Adres url tej strony jest zapisany w config.py w stałej `EXTENDED_MATURA_COURSE_URL`.

Zwraca więc wszystkie informacje o lekcjach z kursu rozszerzonego. Metoda ta obsługuje flagi dostępne dla [get_lessons_data()](#get_lessons_dataurl-kwargs) (czyli `only_questions` i `only_video_ids`).

### get_all_matura_course(\*\*kwargs)

Wywołuje [get_basic_matura_course()](#get_basic_matura_coursekwags) oraz [get_extended_matura_course()](#get_extended_matura_coursekwags)

Wygląda to w ten sposób:

```javascript
return {
    "basic_matura": get_basic_matura_course(**kwargs),
    "extended_matura": get_extended_matura_course(**kwargs)
}
```

### get_all_matura_questions(only_video_ids=False)

1. Pobiera wszytskie pytania z zestawmi pytań (url do zestawów pobiera z config.py ze stałej `QUESTIONS_COLLECTIONS_URLS`)
2. Następnie pobiera wszystkie pytania występujące w lekcjach zarówno w kursie podstawowym, jak i rozszerzonym (wywołuje `get_all_matura_course(only_questions=True)`)
3. Łączy pytania i zwraca w następującym układzie:

   ```javascript
   {
       "id": { // id pytania
           "yt": string, // id flimu z odpowiedzią na youtube
           "ans": string, // odpowiedź do pytania (pusty string, string, html lub MathJax)
           "pts": string, // ilość punktów za pytanie
           "data": string, // data
       }
       ...
   }
   ```

   Jeżeli zaś `only_video_ids` zostanie ustawione na `True`, to dane będą zwracane w następujący sposób:

   ```javascript
   {
    "id": "yt" // id pytania: id flimu z odpowiedzią na youtube
    ...
   }
   ```

### close_browser()

Zamyka przeglądarkę otwartą w czasie inicjalizacji klasy MatemaksScraper.

### generate_data_for_matemaks_extension()

Generuje dane potrzebne dla wtyczki Matemaks Extension

## Funkcje exportujące

### export_to_json(data, file_path=DEFAULT_OUTPUT_FILE_PATH)

Zapisuje `data` do pliku .json w ścieżce podanej jako drugi argument (domyślnie plik generuje się do ścieżki podanej w config.py w stałej `DEFAULT_OUTPUT_FILE_PATH`)
