from requests import Response

from .lib import Base


class Testing(Base):

    def new_user(
            self,
            username: str,
            name: str,
            password: str,
            domain: str,
    ) -> Response:
        """Создание тестового юзера.

        :param username: никнейм пользователя
        :param name: имя пользователя
        :param password: пароль пользователя
        :param domain: домен на который регистрируется пользователь

        :return: requests.Response
        """
        return self._make_request(
            endpoint='testing.newUser',
            payload={
                'username': username,
                'name': name,
                'password': password,
                'domain': domain,
            },
        )
