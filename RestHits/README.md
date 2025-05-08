# RestHits 🎵

Aplikacja REST API do zarządzania listą hitów radiowych. Wykonana w Django + DRF + PostgreSQL.

## 📦 Technologie

- Python 3.6+
- Django 3.0+
- Django REST Framework
- PostgreSQL 13+
- Pytest (testy jednostkowe)

---

## 📚 Funkcjonalność API

| Metoda  | Endpoint                     | Opis                                                       |
|---------|------------------------------|------------------------------------------------------------|
| GET     | `/api/v1/hits`               | Zwraca listę 20 najnowszych hitów                          |
| GET     | `/api/v1/hits/{title_url}`   | Zwraca szczegóły pojedynczego hitu                         |
| POST    | `/api/v1/hits`               | Tworzy nowy hit (`title`, `artist_id`)                     |
| PUT     | `/api/v1/hits/{title_url}`   | Aktualizuje hit (np. `title`, `artist_id`)                 |
| DELETE  | `/api/v1/hits/{title_url}`   | Usuwa podany hit                                           |

---

## ✅ Kody odpowiedzi HTTP

| Kod | Znaczenie                     |
|-----|-------------------------------|
| 200 | Sukces                        |
| 201 | Utworzono zasób               |
| 204 | Sukces, brak zawartości       |
| 400 | Błędne dane wejściowe         |
| 404 | Nie znaleziono zasobu         |

---

## 🚀 Uruchomienie projektu

1. Zainstaluj wymagane biblioteki:
   ```bash
   pip install -r requirements.txt
   
2. Skonfiguruj dane do bazy danych plik: .env
   ```bash
   DB_NAME=resthits_db
   DB_USER=postgres
   DB_PASSWORD=insert_your_password  # Podaj swoje hasło do bazy danych
   DB_HOST=localhost
   DB_PORT=5432
   
3. Dokonaj migracji bazy danych
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   
4. Załaduj dane początkowe
   ```bash
   python manage.py load_data
   
5. Uruchom server
   ```bash
   python manage.py runserver
   
6. Wykonaj testy
   ```bash
   pytest -s
