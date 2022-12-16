from urllib import parse

import requests
from nonebot import on_command
from nonebot.rule import to_me
from src.config.settings import chat_api

from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Event, MessageSegment, GroupMessageEvent

from nonebot.permission import Bot, SUPERUSER
from src.services.log import logger

chat = on_command("chat", rule=to_me(), aliases={"GPT"}, priority=5, permission=SUPERUSER)


@chat.handle()
async def _say(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip()
    if msg:
        msg = msg.split()
        url_tts = chat_api + parse.quote(msg[1].encode('utf-8'))
        result = await get_random_img(url_tts)
        await chat.send(result)
    logger.info(
        f"USER {event.get_user_id()} GROUP "
        f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'} chat： {msg}"
    )

async def get_random_img(url_tts):
    data = requests.get(url_tts)
    return data.url