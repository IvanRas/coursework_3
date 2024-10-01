from abc import ABC, abstractmethod

import psycopg2
import requests


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
    conn = psycopg2.connect(
        host="localhost", # тип подключения
        database="mydatabase", # База данных к которой подключаемся
        user="postgres", # ???
        password="12345" # пароль для входа в БД
    )

    # Создание курсора
    cur = conn.cursor()

    def get_companies_and_vacancies_count(self, *args, **kwargs):
        """Метод получения списока всех компаний и количество вакансий у каждой компании."""
        conn = psycopg2.connect(
            host="localhost",
            database="mydatabase",
            user="postgres",
            password="12345"
        )

        # Создание курсора
        cur = conn.cursor()

        # Создание соединения
        cur.execute("SELECT * from user_account")
        rows = cur.fetchall()
        for row in rows:
            print(row)

        # Закрытие курсора и соединения
        cur.close()
        conn.close()

    def get_avg_salary(self, *args, **kwargs):
        """Метод получения списока всех вакансий с указанием названия компании, названия вакансии и
        зарплаты и ссылки на вакансию."""
        conn = psycopg2.connect(
            host="localhost",
            database="mydatabase",
            user="postgres",
            password="12345"
        )
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT company_name, vacancies_naim, unit_price, vacancies_url from bd")
        finally:
            conn.close()

        pass

    def get_all_vacancies(self, *args, **kwargs):
        """Метод получения средней зарплатs по вакансиям."""
        conn = psycopg2.connect(
            host="localhost",
            database="mydatabase",
            user="postgres",
            password="12345"
        )
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT AVG(unit_price) from bd")
        finally:
            conn.close()

        pass

    def get_vacancies_with_higher_salary(self, *args, **kwargs):
        """Метод получения  списока всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        conn = psycopg2.connect(
            host="localhost",
            database="mydatabase",
            user="postgres",
            password="12345"
        )
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * from bd"
                                "WHERE unit_price > AVG(unit_price)"
                                "ORDER BY unit_price")
        finally:
            conn.close()
        pass

    def get_vacancies_with_keyword(self, *args, **kwargs):
        """Метод получения списока всех вакансий, в названии которых содержатся переданные в метод слова,
        например python"""
        conn = psycopg2.connect(
            host="localhost",
            database="mydatabase",
            user="postgres",
            password="12345"
        )
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * from bd"
                                "WHERE company_name LIKE "
                                "'P%'"
                                "ORDER BY company_name")
        finally:
            conn.close()

        pass
