from typing import TYPE_CHECKING, List

from .types.added_admin_chat import AddedListAdminChat
from ..types.users import ChatAdmin

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath

from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class AddAdminChat(BaseConnection):
    
    """
    Класс для добавления списка администраторов в чат через API.

    Args:
        bot (Bot): Экземпляр бота, через который выполняется запрос.
        chat_id (int): Идентификатор чата.
        admins (List[ChatAdmin]): Список администраторов для добавления.
        marker (int, optional): Маркер для пагинации или дополнительных настроек. По умолчанию None.
    """

    def __init__(
            self, 
            bot: 'Bot',
            chat_id: int,
            admins: List[ChatAdmin],
            marker: int = None
        ):
        self.bot = bot
        self.chat_id = chat_id
        self.admins = admins
        self.marker = marker

    async def request(self) -> AddedListAdminChat:
        
        """
        Выполняет HTTP POST запрос для добавления администраторов в чат.

        Формирует JSON с данными администраторов и отправляет запрос на соответствующий API-эндпоинт.

        Returns:
            AddedListAdminChat: Результат операции с информацией об успешности.
        """
        
        json = {}

        json['admins'] = [admin.model_dump() for admin in self.admins]
        json['marker'] = self.marker

        return await super().request(
            method=HTTPMethod.POST, 
            path=ApiPath.CHATS.value + '/' + str(self.chat_id) + ApiPath.MEMBERS + ApiPath.ADMINS,
            model=AddedListAdminChat,
            params=self.bot.params,
            json=json
        )