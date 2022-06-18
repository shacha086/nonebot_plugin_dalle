import traceback
from typing import List

import httpx
import nonebot
from httpx import AsyncClient
from nonebot.adapters.onebot.v11 import MessageSegment, Bot, GroupMessageEvent


async def get_images(keyword: str) -> list:
    nonebot.logger.debug('开始下载…')
    async with httpx.AsyncClient() as client:
        client: AsyncClient
        try:
            resp = await client.post(
                url="https://bf.dallemini.ai/generate",
                json={'prompt': keyword},
                timeout=61658,
                headers={'Accept': 'application/json',
                         'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                         'Cache-Control': 'no-cache',
                         'Pragma': 'no-cache',
                         'Connection': 'keep-alive',
                         'Content-Type': 'application/json',
                         'Accept-Encoding': 'gzip, deflate, br',
                         'Host': 'bf.dallemini.ai',
                         'Origin': 'https://hf.space',
                         'Referer': 'https://hf.space',
                         'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Microsoft Edge";v="102"',
                         'sec-ch-ua-mobile': '?0',
                         "sec-ch-ua-platform": '"Windows"',
                         'Sec-Fetch-Dest': 'empty',
                         'Sec-Fetch-Mode': 'cors',
                         'Sec-Fetch-Site': 'cross-site',
                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
                          Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.41'
                         }
            )
        except Exception as e:
            traceback.print_exception(e)
        image_list = resp.json()['images']
    nonebot.logger.debug('下载完成')
    return await normalize_b64(image_list)


async def normalize_b64(list_: List[str]) -> list:
    return [_.replace('\\n', '').replace('\n', '') for _ in list_]


def node_custom(
        user_id: int, name: str, content: MessageSegment
) -> "MessageSegment":
    return MessageSegment(
        "node", {"uin": str(user_id), "name": name, "content": content}
    )


async def send_group_forward_msg(
        bot: Bot,
        event: GroupMessageEvent,
        msgs: List[MessageSegment],
):
    await bot.call_api(
        "send_group_forward_msg", group_id=event.group_id, messages=msgs
    )
#
#
# async def send_group_forward_images(bot: Bot, event: GroupMessageEvent, list_: List[str]):
#     forward_msg = []
#     for image in list_:
#         forward_msg.append(node_custom(
#             content=MessageSegment.image(f'base64://{image}'),
#             user_id=int(bot.self_id),
#             name='河童'
#         ))
#     await send_group_forward_msg(bot, event, forward_msg)


async def send_replied_group_forward_msg(
        bot: Bot,
        event: GroupMessageEvent,
        msgs: List[MessageSegment],
):
    await bot.call_api(
        "send_group_forward_msg", group_id=event.group_id, messages=msgs
    )


async def send_replied_group_forward_images_with_reply(bot: Bot, event: GroupMessageEvent, list_: List[str]):
    # forward_msg = []
    forward_msg = [
        event.message
    ]
    for image in list_:
        forward_msg.append(node_custom(
            content=MessageSegment.image(f'base64://{image}'),
            user_id=int(bot.self_id),
            name='河童'
        ))
    await send_replied_group_forward_msg(bot, event, forward_msg)
