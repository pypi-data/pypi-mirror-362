from typing import Literal, Optional

from requests import Response

from ecss_chat_client.ecss_chat_client.lib import Base
from ecss_chat_client.ecss_chat_client.utils.utils import decorator_service


class Users(Base):

    def get_user_info(self, username: str) -> Response:
        """Информация о пользователе по username.

        :param username: никнейм пользователя

        :return: requests.Response
        """
        return self._make_request(
            endpoint='users.info',
            params={
                'username': username,
            },
            method='get',
        )

    @decorator_service.paginate
    def search_for_room_mention(
            self,
            room_id: str,
            query: str = '',
            members_only: Optional[Literal[1, 0]] = 1,
            count: Optional[int] = None,
            offset: Optional[int] = None,
    ) -> Response:
        """Поиск пользователей для упоминания или приглашения в комнату.

        :param room_id: uid комнаты
        :param query: строка для фильтрации
        :param members_only: поиск среди комнаты(1) или всего домена(0)
          :param offset: количество пропускаемых сообщений
        :param count: максимальное количество сообщений

        :return: requests.Response
        """
        return self._make_request(
            'users.searchForRoomMention',
            params={
                'roomId': room_id,
                'query': query,
                'count': count,
                'offset': offset,
                'searchInMembersOnly': members_only,
            },
            method='get',
        )

    def current_user_info(self) -> Response:
        """Получение информации о текущем юзере.

        :return: requests.Response
        """
        return self._make_request(endpoint='me', method='get')
