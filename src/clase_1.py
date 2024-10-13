import json
from abc import ABC, abstractmethod

from psycopg2 import Error
import psycopg2


class AbstracDBManager(ABC):
    """Абстрактный класс для работы с BD внешних сервисов"""

    @abstractmethod
    def get_companies_and_vacancies_count(self, *args, **kwargs):
        """Абстрактный метод получения списка всех компаний и количество вакансий у каждой компании."""
        pass

    @abstractmethod
    def get_avg_salary(self, *args, **kwargs):
        """Абстрактный метод получения списка всех вакансий с указанием названия компании, названия вакансии и
        зарплаты и ссылки на вакансию."""
        pass

    @abstractmethod
    def get_all_vacancies(self, *args, **kwargs):
        """Абстрактный метод получения средней зарплатs по вакансиям."""
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self, *args, **kwargs):
        """Абстрактный метод получения  списка всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self, *args, **kwargs):
        """Абстрактный метод получения списка всех вакансий, в названии которых содержатся переданные в метод слова,
        например python"""
        pass


class DBManager(AbstracDBManager):
    # Создание подключение
    def __init__(self, bd_name, user, password, host="localhost", port="5432"):
        try:
            self.connection = psycopg2.connect(dbname=bd_name, user=user, password=password, host=host, port=port)

            self.connection.autocommit = True
        except Error as e:
            print("Ошибка при подключении:", e)

    def tables_exist(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'companies')")
            companies_exist = cursor.fetchone()[0]
            cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'vacancies')")
            vacancies_exist = cursor.fetchone()[0]
            return companies_exist and vacancies_exist

    def create_tables(self):
        """
        Создает таблицы companies и vacancies.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS companies (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    employer_id INTEGER UNIQUE NOT NULL
                );
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS vacancies (
                    id SERIAL PRIMARY KEY,
                    company_id INTEGER REFERENCES companies(id),
                    title VARCHAR(255),
                    salary_min INTEGER,
                    salary_max INTEGER,
                    url VARCHAR(255),
                    description TEXT,
                    published_at TIMESTAMP
                );
            """
            )

    def get_companies_and_vacancies_count(self, *args, **kwargs):
        """Метод получения списока всех компаний и количество вакансий у каждой компании."""

        # Создание соединения
        conn = psycopg2.connect(host="localhost", database="test", user="postgres", password="123qweewq321")
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * from user_account")
        finally:
            conn.close()

    def get_avg_salary(self, *args, **kwargs):
        """Метод получения списока всех вакансий с указанием названия компании, названия вакансии и
        зарплаты и ссылки на вакансию."""
        conn = psycopg2.connect(host="localhost", database="test", user="postgres", password="123qweewq321")
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT company_name, vacancies_naim, unit_price, vacancies_url from bd")
        finally:
            conn.close()

    def get_all_vacancies(self, *args, **kwargs):
        """Метод получения средней зарплатs по вакансиям."""
        conn = psycopg2.connect(host="localhost", database="mydatabase", user="postgres", password="12345")
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT AVG(unit_price) from bd")
        finally:
            conn.close()

    def get_vacancies_with_higher_salary(self, *args, **kwargs):
        """Метод получения  списока всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        conn = psycopg2.connect(host="localhost", database="mydatabase", user="postgres", password="12345")
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * from bd" "WHERE unit_price > AVG(unit_price)" "ORDER BY unit_price")
        finally:
            conn.close()

    def get_vacancies_with_keyword(self, *args, **kwargs):
        """Метод получения списока всех вакансий, в названии которых содержатся переданные в метод слова,
        например python"""
        conn = psycopg2.connect(host="localhost", database="mydatabase", user="postgres", password="12345")
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * from bd" "WHERE company_name LIKE " "'P%'" "ORDER BY company_name")
        finally:
            conn.close()

    def close(self):
        """Закрывает соединение с базой данных."""
        self.connection.close()

    def load_companies_from_json(self, file_path):
        """
        Загружает данные о компаниях из JSON-файла и вставляет их в таблицу companies.

        Параметры:
        ----------
        file_path : str
            Путь до файла с данными компаний.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            companies = json.load(file)

        for company in companies:
            name = company["name"]
            employer_id = company["employer_id"]
            self.insert_company(name, employer_id)

    def insert_company(self, name, employer_id):
        """
        Вставляет новую компанию в таблицу companies.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO companies (name, employer_id) VALUES (%s, %s) ON CONFLICT (employer_id) DO NOTHING;",
                (name, employer_id),
            )

    def load_vac_from_json(self, json_data):
        """
        Загружает данные о компаниях из JSON-файла и вставляет их в таблицу vacancies.

        Параметры:
        ----------
        file_path : str
            Путь до файла с данными вакансий.
        """

        for vac in json_data.get("items"):
            title = vac["name"],
            salary_min = vac["salary_min"],
            salary_max = vac["salary_max"],
            url = vac["url"],
            description = vac["description"],
            published_at = vac["published_at"]
            self.insert_vac(title, salary_min, salary_max, url, description, published_at)

    def insert_vac(self, title, salary_min, salary_max, url, description, published_at):
        """
        Вставляет новую компанию в таблицу vacancies.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO vacancies (title, salary_min, salary_max, url, description, published_at) VALUES (%s, %s, %s, %s, %s, %s);",
                (title, salary_min, salary_max, url, description, published_at),
            )
