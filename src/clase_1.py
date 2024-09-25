from abc import ABC, abstractmethod

import requests


class AbstracDBManager(ABC):
    """Абстрактный класс для работы с API внешних сервисов"""

    @abstractmethod
    def get_companies_and_vacancies_count(self, *args, **kwargs):
        """Абстрактный метод получения списокf всех компаний и количество вакансий у каждой компании."""
        pass

    @abstractmethod
    def get_avg_salary(self, *args, **kwargs):
        """Абстрактный метод получения списокf всех вакансий с указанием названия компании, названия вакансии и
        зарплаты и ссылки на вакансию."""
        pass

    @abstractmethod
    def get_all_vacancies(self, *args, **kwargs):
        """Абстрактный метод получения среднtq зарплатs по вакансиям."""
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self, *args, **kwargs):
        """Абстрактный метод получения  списокd всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self, *args, **kwargs):
        """Абстрактный метод получения списокf всех вакансий, в названии которых содержатся переданные в метод слова,
        например python"""
        pass
