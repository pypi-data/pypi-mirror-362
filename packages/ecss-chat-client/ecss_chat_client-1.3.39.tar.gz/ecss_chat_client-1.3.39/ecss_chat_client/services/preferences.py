from typing import Union

from requests import Response

from .lib import Base


class UserPreferences(Base):

    def preferences_list(self) -> Response:
        """Список предпочтений пользователя.

        :return: requests.Response
        """
        return self._make_request(
            endpoint='preferences.list',
            method='get',
        )

    def preferences_set(
            self,
            preference: str,
            value: Union[int, str],
    ) -> Response:
        """Установка предпочтения пользователя.

        :param preference: ключ настройки
        :param value: значение настройки

        :return: requests.Response
        """
        return self._make_request(
            endpoint='preferences.set',
            payload={
                preference: value,
            },
        )
