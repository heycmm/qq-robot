from src.config.settings import IMAGE_PATH
from nonebot import on_command
from nonebot.typing import T_State
from src.utils import image
from src.services.log import logger
from nonebot.adapters.onebot.v11 import Event, GroupMessageEvent
from src.utils import CreateImg
from nonebot.permission import Bot

luxun = on_command("鲁迅说过", aliases={"鲁迅说"}, priority=5, block=True)

luxun_author = CreateImg(0, 0, plain_text="--鲁迅", font_size=30, font='msyh.ttf', font_color=(255, 255, 255))


@luxun.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    args = ''.join(str(event.get_message()))
    if args:
        state["content"] = args if args else "烦了，不说了"


@luxun.got("content", prompt="你让鲁迅说点啥?")
async def handle_event(bot: Bot, event: Event, state: T_State):
    content = state["content"]
    content = str(content).split()[1]
    A = CreateImg(0, 0, font_size=37, background=f'{IMAGE_PATH}/other/luxun.jpg', font='msyh.ttf')
    x = ""
    if len(content) > 40:
        await luxun.finish('太长了，鲁迅说不完...')
    while A.getsize(content)[0] > A.w - 50:
        n = int(len(content) / 2)
        x += content[:n] + '\n'
        content = content[n:]
    x += content
    if len(x.split('\n')) > 2:
        await luxun.finish('太长了，鲁迅说不完...')
    A.text((int((480 - A.getsize(x.split("\n")[0])[0]) / 2), 300), x, (255, 255, 255))
    A.paste(luxun_author, (320, 400), True)
    await luxun.send(image(b64=A.pic2bs4()))
    logger.info(
        f"USER {event.get_user_id()} GROUP "
        f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'} 鲁迅说过 {content}"
    )
