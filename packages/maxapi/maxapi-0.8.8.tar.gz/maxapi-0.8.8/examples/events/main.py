import asyncio
import logging

from maxapi import Bot, Dispatcher
from maxapi.types import (
    BotStarted, 
    Command, 
    MessageCreated, 
    CallbackButton, 
    MessageCallback, 
    BotAdded, 
    ChatTitleChanged, 
    MessageEdited, 
    MessageRemoved, 
    UserAdded, 
    UserRemoved
)
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

logging.basicConfig(level=logging.INFO)

bot = Bot('тут_ваш_токен')
dp = Dispatcher()


@dp.message_created(Command('start'))
async def hello(event: MessageCreated):
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(
            text='Кнопка 1',
            payload='btn_1'
        ),
        CallbackButton(
            text='Кнопка 2',
            payload='btn_2',
        )
    )
    builder.add(
        CallbackButton(
            text='Кнопка 3',
            payload='btn_3',
        )
    )

    await event.message.answer(
        text='Привет!', 
        attachments=[
            builder.as_markup(),
        ]                               # Для MAX клавиатура это вложение, 
    )                                       # поэтому она в списке вложений


@dp.bot_added()
async def bot_added(event: BotAdded):
    await event.bot.send_message(
        chat_id=event.chat.id,
        text=f'Привет чат {event.chat.title}!'
    )
    
    
@dp.message_removed()
async def message_removed(event: MessageRemoved):
    await event.bot.send_message(
        chat_id=event.chat_id,
        text='Я всё видел!'
    )
    
    
@dp.bot_started()
async def bot_started(event: BotStarted):
    await event.bot.send_message(
        chat_id=event.chat_id,
        text='Привет! Отправь мне /start'
    )
    
    
@dp.chat_title_changed()
async def chat_title_changed(event: ChatTitleChanged):
    await event.bot.send_message(
        chat_id=event.chat_id,
        text=f'Крутое новое название "{event.chat.title}!"'
    )
    
    
@dp.message_callback()
async def message_callback(event: MessageCallback):
    await event.answer(
        new_text=f'Вы нажали на кнопку {event.callback.payload}!'
    )
    

@dp.message_edited()
async def message_edited(event: MessageEdited):
    await event.message.answer(
        text='Вы отредактировали сообщение!'
    )
    
    
@dp.user_removed()
async def user_removed(event: UserRemoved):
    await event.bot.send_message(
        chat_id=event.chat_id,
        text=f'{event.from_user.first_name} кикнул {event.user.first_name} 😢'
    )
    
    
@dp.user_added()
async def user_added(event: UserAdded):
    await event.bot.send_message(
        chat_id=event.chat_id,
        text=f'Чат "{event.chat.title}" приветствует вас, {event.user.first_name}!'
    )


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())