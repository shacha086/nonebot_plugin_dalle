from typing import List

import httpx


async def get_images(keyword: str) -> list:
    image_list: List[str] = httpx.post(
        url="https://bf.dallemini.ai/generate",
        json={'prompt': keyword},
        verify=False,
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
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.41'
                 }
    ).json()['images']
    return await normalize_b64(image_list)


async def normalize_b64(list_: List[str]) -> list:
    return [_.replace('\\n', '') for _ in list_]
