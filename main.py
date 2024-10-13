import json
import os
from datetime import datetime

from dotenv import load_dotenv

from src.clase_2 import HeadHunterAPI
from src.clase_1 import DBManager

load_dotenv()


# def main():
#
#     # Установка соединения
#
#     dbname='your_database',
#     user='postgres',
#     password='123qweewq321',
#     host='localhost',
#     port='5432'
#
#     bd = DBManager(bd_name=dbname, user=user, password=password)
#     bd.create_tables()
#     # bd.close()


def user_interaction():

    hh_api = HeadHunterAPI()
    # Подключение к базе данных
    db = DBManager(os.getenv("DB_NAME"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD"))

    # Проверяем наличие таблиц
    # if not db.tables_exist():
    db.create_tables()
    #     print("Таблицы созданы.")

    # Загружаем компании из JSON
    db.load_companies_from_json("data/companies.json")

    with open("data/companies.json") as f:
        copas = json.load(f)
        for i in copas:
            db.load_vac_from_json(hh_api.get_company_vacancies(i.get("employer_id")))

    while True:
        print("\nДобро пожаловать в систему управления вакансиями!")
        print("Выберите действие:")
        print("1. Показать список компаний и количество вакансий у каждой")
        print("2. Показать все вакансии")
        print("3. Показать среднюю зарплату по вакансиям")
        print("4. Показать вакансии с зарплатой выше средней")
        print("5. Поиск вакансий по ключевому слову")
        print("6. Выйти")
        print("7. Вернутся")

        choice = input("Введите номер действия: ")

        if choice == "1":
            # Показать список компаний и количество вакансий
            companies_and_vacancies = db.get_companies_and_vacancies_count()
            for row in companies_and_vacancies:
                print(f"Компания: {row['name']}, Количество вакансий: {row['vacancies_count']}")

        elif choice == "2":
            # Показать все вакансии
            vacancies = db.get_all_vacancies()
            for vac in vacancies:
                print(
                    f"Компания: {vac['company_name']}, Вакансия: {vac['vacancy_title']}, "
                    f"Зарплата: от {vac['salary_min']} до {vac['salary_max']}, Ссылка: {vac['url']}"
                )

        elif choice == "3":
            # Показать среднюю зарплату
            avg_prise = db.get_avg_salary()
            print(f"Средняя зарплата по всем вакансиям: {avg_prise}")

        elif choice == "4":
            # Показать вакансии с зарплатой выше средней
            above_average = db.get_vacancies_with_higher_salary()
            for a_avg in above_average:
                print(
                    f"Компания: {a_avg['company_name']}, Вакансия: {a_avg['vacancy_title']}, "
                    f"Зарплата: от {a_avg['salary_min']} до {a_avg['salary_max']}, Ссылка: {a_avg['url']}"
                )

        elif choice == "5":
            # Поиск вкансий р=по ключевому слову
            keyword = input("Введите ключевое слова для поиска: ")
            search = db.get_vacancies_with_keyword()
            for sear in search:
                print(
                    f"Компания: {sear['company_name']}, Вакансия: {sear['vacancy_title']}, "
                    f"Зарплата: от {sear['salary_min']} до {sear['salary_max']}, Ссылка: {sear['url']}"
                )

        elif choice == "6":
            # Выйти из программы
            db.close()
            print("Программа завершена.")
            break

        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    user_interaction()
