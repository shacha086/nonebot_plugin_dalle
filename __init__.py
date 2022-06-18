import asyncio
from asyncio import Task
from typing import List

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, GroupMessageEvent, Message
from nonebot.params import CommandArg

from .utils import normalize_b64, node_custom, send_group_forward_msg, get_images, \
    send_replied_group_forward_msg, send_replied_group_forward_images_with_reply

task_list: List[Task] = []

matcher = on_command('河图')


@matcher.handle()
async def _(
        bot: Bot,
        event: GroupMessageEvent,
        arg: Message = CommandArg()
):
    if not arg:
        await matcher.finish("你要画啥？🤔")

    await matcher.send(MessageSegment.reply(event.message_id) + "别急，河童画图中")

    get_images_and_send_later(bot, event, arg.extract_plain_text())

    return


def get_images_and_send_later(bot: Bot, event: GroupMessageEvent, keyword: str):
    global task_list

    async def get_images_and_send():
        images = await get_images(keyword)
        await send_replied_group_forward_images_with_reply(bot, event, images)
    task_list.append(asyncio.create_task(get_images_and_send(), name=f'download{task_list.__sizeof__()}'))
