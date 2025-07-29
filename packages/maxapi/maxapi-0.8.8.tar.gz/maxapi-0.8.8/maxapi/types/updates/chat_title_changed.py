from typing import TYPE_CHECKING, Any, Optional

from .update import Update

from ...types.users import User

if TYPE_CHECKING:
    from ...bot import Bot
    

class ChatTitleChanged(Update):
    
    """
    Обновление, сигнализирующее об изменении названия чата.

    Attributes:
        chat_id (Optional[int]): Идентификатор чата.
        user (User): Пользователь, совершивший изменение.
        title (Optional[str]): Новое название чата.
    """
    
    chat_id: Optional[int] = None
    user: User
    title: Optional[str] = None
    
    if TYPE_CHECKING:
        bot: Optional[Bot]

    def get_ids(self):
        return (self.chat_id, self.user.user_id)