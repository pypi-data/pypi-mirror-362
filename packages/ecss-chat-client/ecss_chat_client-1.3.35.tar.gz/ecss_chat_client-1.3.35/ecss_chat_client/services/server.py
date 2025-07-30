import json
from typing import Optional

from requests import Response

from ecss_chat_client.ecss_chat_client.lib import Base
from ecss_chat_client.ecss_chat_client.types.settings import \
    server_settings_type  # noqa
from ecss_chat_client.ecss_chat_client.utils.utils import decorator_service


class ServerSettings(Base):

    @decorator_service.paginate
    def server_settings_public(
            self,
            count: Optional[int] = None,
            offset: Optional[int] = None,
    ) -> Response:
        """Получение настроек сервера.

        :param offset: количество пропускаемых сообщений
        :param count: максимальное количество сообщений

        :return: requests.Response
        """
        return self._make_request(
            endpoint='settings.public',
            params={
                'offset': offset,
                'count': count,
            },
            method='get',
        )

    def get_setting_public_by_id(self, setting_id: str) -> Response:
        """Получить настройку сервера по uid.

        :param setting_id: uid настройки

        :return: requests.Response
        """
        return self._make_request(
            endpoint=f'settings.public/{setting_id}',
            method='get',
        )

    def get_hide_setting(self, setting_id: str) -> Response:
        """Получить скрытую настройку по uid.

        :param setting_id: uid настройки

        :return: requests.Response
        """
        return self._make_request(
            endpoint=f'settings/{setting_id}',
            method='GET',
        )

    def server_setting_set(
            self,
            setting_name: (
                    server_settings_type.FILES |
                    server_settings_type.MOBILE |
                    server_settings_type.MESSAGES |
                    server_settings_type.FOLDERS
            ),
            value: bool | str | int | list[str] | dict,
    ) -> Response:
        """Установка настройки сервера.

        :param setting_name: название настройки
        :param value: значение настройки

        :return: requests.Response
        """
        if type(value) is dict:
            value = json.dumps(value)
        return self._make_request(
            endpoint='settings.set',
            payload={
                'id': setting_name,
                'value': value,
            },
        )
