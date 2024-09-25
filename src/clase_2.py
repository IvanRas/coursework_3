from abc import ABC, abstractmethod

import requests


class AbstractVacancyAPI(ABC):
    """Абстрактный класс для работы с API внешних сервисов"""

    @abstractmethod
    def fetch_vacancies(self, *args, **kwargs):
        """Абстрактный метод получения вакансий"""
        pass


class HHVacancyAPI(AbstractVacancyAPI):
    """Абстрактный класс для работы с API внешних сервисов"""

    def __init__(self):
        """Инициализация атрибутов класса."""
        self.__base_url = "https://api.hh.ru/vacancies"

    def fetch_vacancies(self, search_query: str, page: int = 0, per_page: int = 20):
        """Метод получения вакансий на сайте hh.ru
        :arg search_query - поисковый запрос,
        :arg area - название населенного пункта,
        :arg page - номер страницы,
        :arg per_page - количество элементов на странице"""

        params = {"text": f"NAME:{search_query}", "page": page, "per_page": per_page}

        response = requests.get(self.__base_url, params=params)
        if response.status_code == 200:
            return response.json()["items"]
        else:
            print("Ошибка при получении данных: ", response.status_code)
            return []
