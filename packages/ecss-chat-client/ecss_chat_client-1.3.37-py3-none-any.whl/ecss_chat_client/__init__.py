"""ECSS Chat Client - Python клиент для ECSS Chat."""
from .services.auth import Auth
from .services.avatar import Avatar
from .services.config import Settings
from .services.directs import Directs
from .services.folders import Folders
from .services.groups import Groups
from .services.info import ApiInfo
from .services.messages import Messages
from .services.polls import Polls
from .services.preferences import UserPreferences
from .services.rooms import Rooms
from .services.spotlight import Spotlight
from .services.supergroups import SuperGroups
from .services.testing import Testing
from .services.threads import Threads
from .services.tus import TusService
from .services.users import Users
from .services.websocket_client import WebsocketClient


class Client:
    def __init__(
            self,
            server,
            username,
            password,
            port='3443',
            proto='https',
            verify=True,
    ):
        self.username = username
        self.password = password
        self.port = port
        self.proto = proto
        self.verify = verify
        self.server = server
        self.base_url = f'{proto}://{server}:{port}/api/v1'
        self.short_url = f'{proto}://{server}:{port}/api'
        self.__websocket_url = f'wss://{server}:{port}/websocket'

        self.settings = Settings(
            server, config_file='settings.ini',
        )

        self.session = Auth.session(
            username,
            password,
            server,
            proto,
            port,
            verify,
        )
        self.websocket = WebsocketClient(
            self.__websocket_url,
            username=self.username,
            session=self.session,
        )
        self.avatar = Avatar(self)
        self.directs = Directs(self)
        self.groups = Groups(self)
        self.polls = Polls(self)
        self.rooms = Rooms(self)
        self.supergroups = SuperGroups(self)
        self.folders = Folders(self)
        self.users = Users(self)
        self.preferences = UserPreferences(self)
        self.messages = Messages(self)
        self.threds = Threads(self)
        self.testing = Testing(self)
        self.spotlight = Spotlight(self)
        self.tus = TusService(self)
        self.api_info = ApiInfo(self)


__all__ = ['Client']
__version__ = '1.3.37'
__author__ = 'Eltex SC VoIP'
__description__ = 'ElphChat API Client Library'
