import asyncio

import httpx
import requests
import bs4
from colorama import Fore

import syncify


def main():
    number = syncify.run(get_title_range())
    syncify.run(get_title_range_queued())
    print(f"Done {number}.")


async def get_html(episode_number: int) -> str:
    print(Fore.YELLOW + f"Getting HTML for episode {episode_number}", flush=True)

    url = f'https://talkpython.fm/{episode_number}'
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, follow_redirects=True)
        resp.raise_for_status()

    return resp.text


async def get_html_queue(episode_number: int, results: asyncio.Queue):
    print(Fore.YELLOW + f"Getting HTML for episode {episode_number}", flush=True)

    url = f'https://talkpython.fm/{episode_number}'
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, follow_redirects=True)
        resp.raise_for_status()

    await results.put((episode_number, resp.text))


def get_title(html: str, episode_number: int) -> str:
    print(Fore.CYAN + f"Getting TITLE for episode {episode_number}", flush=True)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    header = soup.select_one('h1')
    if not header:
        return "MISSING"

    return header.text.strip()


# async def get_title_range():
#     # Please keep this range pretty small to not DDoS my site. ;)
#     for n in range(350, 368):
#         html = await get_html(n)
#         title = get_title(html, n)
#         print(Fore.WHITE + f"Title found: {title}", flush=True)

async def get_title_range():
    # Please keep this range pretty small to not DDoS my site. ;)
    work = []
    for n in range(350, 368):
        item = (asyncio.create_task(get_html(n)), n)
        work.append(item)

    for task, number in work:
        html = await task
        title = get_title(html, number)
        print(Fore.WHITE + f"Title found: {title}", flush=True)

    return 42


async def get_title_range_queued():
    # Please keep this range pretty small to not DDoS my site. ;)
    work = []
    results = asyncio.Queue()
    for n in range(350, 368):
        item = (asyncio.create_task(get_html_queue(n, results)), n)
        work.append(item)

    number = 0
    while number < 367:
        number, html = await results.get()
        title = get_title(html, number)
        print(Fore.WHITE + f"Title found: {title}", flush=True)


if __name__ == '__main__':
    main()
