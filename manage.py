#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import mysql.connector


# def main():
#     """Run administrative tasks."""
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EventManagementSystem.settings')
#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc
#     execute_from_command_line(sys.argv)

def create_database_and_tables():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'event_management'
    }
    connection = mysql.connector.connect(**db_config)

    if connection.is_connected():
        print('Połączenie z bazą danych nawiązane.')
    else:
        print('Nie udało się nawiązać połączenia z bazą danych.')

    cursor = connection.cursor()
    
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS event_management")
        cursor.execute("USE event_management")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS User (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        role ENUM('administrator', 'zwykły użytkownik') NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Event (
            event_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            start_date DATETIME NOT NULL,
            end_date DATETIME NOT NULL,
            location VARCHAR(255),
            organizer_id INT,
            parent_event_id INT,  -- Kolumna dla wydarzenia nadrzędnego
            status ENUM('zaplanowane', 'w trakcie', 'zakończone') NOT NULL,
            FOREIGN KEY (organizer_id) REFERENCES User(user_id),
            FOREIGN KEY (parent_event_id) REFERENCES Event(event_id)  -- Klucz obcy dla wydarzenia nadrzędnego
        );

        CREATE TABLE IF NOT EXISTS EventSubmission (
            submission_id INT AUTO_INCREMENT PRIMARY KEY,
            event_id INT NOT NULL,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            submitter_id INT NOT NULL,
            status ENUM('oczekujące', 'zaakceptowane', 'odrzucone') NOT NULL,
            FOREIGN KEY (event_id) REFERENCES Event(event_id),
            FOREIGN KEY (submitter_id) REFERENCES User(user_id)
        );

        CREATE TABLE IF NOT EXISTS EventRegistration (
            registration_id INT AUTO_INCREMENT PRIMARY KEY,
            event_id INT NOT NULL,
            user_id INT NOT NULL,
            registration_date DATETIME NOT NULL,
            FOREIGN KEY (event_id) REFERENCES Event(event_id),
            FOREIGN KEY (user_id) REFERENCES User(user_id)
        );

        CREATE TABLE IF NOT EXISTS Category (
            category_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );

        -- tabela EventCategory (łącznikowa dla relacji many-to-many)
        CREATE TABLE IF NOT EXISTS EventCategory (
            event_id INT,
            category_id INT,
            PRIMARY KEY (event_id, category_id),
            FOREIGN KEY (event_id) REFERENCES Event(event_id),
            FOREIGN KEY (category_id) REFERENCES Category(category_id)
        );

        -- Tworzenie tabeli Tag
        CREATE TABLE IF NOT EXISTS Tag (
            tag_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );

        -- tabela EventTag (łącznikowa dla relacji many-to-many)
        CREATE TABLE IF NOT EXISTS EventTag (
            event_id INT,
            tag_id INT,
            PRIMARY KEY (event_id, tag_id),
            FOREIGN KEY (event_id) REFERENCES Event(event_id),
            FOREIGN KEY (tag_id) REFERENCES Tag(tag_id)
        );
        """)
    except mysql.connector.Error as err:
        print("Błąd:", err)

    finally:
        cursor.close()
        connection.close()
        #connection.commit()

if __name__ == '__main__':
    #main()
    create_database_and_tables()
