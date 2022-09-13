from urllib import parse

from nonebot import on_command
from nonebot.rule import to_me
from src.config.settings import tts_api

from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Event, MessageSegment, GroupMessageEvent

from nonebot.permission import Bot, SUPERUSER
from src.services.log import logger

say = on_command("say", rule=to_me(), aliases={"跟我学"}, priority=5, permission=SUPERUSER)


# 大概效果就是 通过上面几个指令
# 用AI语音合成发送出来，实现在qq群里装逼的效果
@say.handle()
async def _say(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip()
    if msg:
        msg = msg.split()
        result = MessageSegment.record(tts_api + parse.quote(msg[1].encode('utf-8')))
        await say.send(result)
    logger.info(
        f"USER {event.get_user_id()} GROUP "
        f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'} say： {msg}"
    )
