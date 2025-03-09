# PostAPI

PostAPI to usługa REST API stworzona w oparciu o Django oraz Django REST Framework. Aplikacja umożliwia tworzenie, modyfikowanie i usuwanie postów, przy czym:

- Każdy post musi zawierać:
  - **Nazwę** – maks. 100 znaków,
  - **Opis** – maks. 1024 znaki,
  - **Słowa kluczowe** – przynajmniej 3 unikalne słowa, łączna długość maks. 500 znaków. Słowa kluczowe mogą zawierać spacje (np. "problem komiwojażera" traktowane jest jako jedno słowo kluczowe),
  - **Adres URL** – maks. 1024 znaki.  
  Nazwa posta nie może być jednym z podanych słów kluczowych.

- Aplikacja rejestruje, który adres IP oraz kiedy dodał dany post.

- Modyfikacja (aktualizacja lub usunięcie) posta jest dozwolona wyłącznie dla autora (na podstawie adresu IP).

- Każda modyfikacja posta jest zapisywana w historii, co pozwala na ręczne odtworzenie poprzedniej wersji wpisu.

- Struktura danych posta jest elastyczna i może ulegać modyfikacjom.

## Funkcje

- **Dodawanie postów:**  
  Użytkownik musi podać poprawne dane (nazwa, opis, słowa kluczowe, URL). Przy tworzeniu zapisywany jest adres IP użytkownika.

- **Modyfikacja i usuwanie:**  
  Tylko autor (adres IP) może zmieniać lub usuwać post. Każda operacja modyfikacji jest rejestrowana w historii.

- **Historia modyfikacji:**  
  Wszystkie zmiany są zapisywane, co umożliwia odtworzenie poprzedniego stanu posta.

## Wymagania

- Python 3.8+
- Django (np. wersja 3.x lub 4.x)
- Django REST Framework
- Domyślnie SQLite (można zmienić w ustawieniach)
- pytest oraz pytest-django (do testowania projektu)

## Instalacja

### 1. Klonowanie repozytorium

```bash
git clone https://github.com/Fuukss/PostAPI.git
cd postapi
```

### 2. Utworzenie i aktywacja środowiska
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Inicjalizacja zależności
```bash
pip install -r requirements.txt
```

### 4. Migracje bazy danych
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Uruchomienie aplikacji
```bash
python manage.py runserver
```

# Enpoity API
```http
GET /api/posts/
POST /api/posts/
```
* GET /api/posts/ – Pobranie listy postów.
* POST /api/posts/ – Dodanie nowego posta (wymagane dane: nazwa, opis, słowa kluczowe, URL). Przy tworzeniu zapisywany jest adres IP użytkownika.

```http
GET /api/posts/{id}/
PATCH /api/posts/{id}/
PUT /api/posts/{id}/
DELETE /api/posts/{id}/
```
* GET /api/posts/{id}/ – Pobranie szczegółów wybranego posta.
* PUT/PATCH /api/posts/{id}/ – Aktualizacja posta (dozwolona tylko dla autora – porównanie adresu IP).
* DELETE /api/posts/{id}/ – Usunięcie posta (dozwolone tylko dla autora). Każda modyfikacja (update lub delete) jest rejestrowana w historii.

# Testowanie
```bash
pytest
```
