import random

from bs4 import BeautifulSoup
from core.config import worker_setting


class Parser:
    def __init__(self, aiohttp_client):
        self.client = aiohttp_client
        self.url = worker_setting.SERVICE_URL

    async def collect_topics(self):
        soup = await self.send_request_(self.url + "/compilation/mcompilation")
        topics_block = soup.find_all("div", class_="film_tags_square")[1]
        topics = topics_block.find_all("a")
        for topic in topics:
            topic_href = topic.get("href")
            yield topic_href

    async def collect_categories(self):
        async for topic in self.collect_topics():
            soup = await self.send_request_(self.url + topic)
            categories_block = soup.find("div", class_="compilation_wrapper")
            categories = categories_block.find_all("a")
            for category in categories:
                category_href = category.get("href")
                category_title = category.find("strong").text.strip()
                yield category_href, category_title

    async def collect_films(self):
        async for category, category_title in self.collect_categories():
            soup = await self.send_request_(self.url + category)
            films_block = soup.find("div", class_="film_list_block")
            films = films_block.find_all("div", class_="film_list")
            for film in films:
                film_href = film.find("a", class_="film_list_link").get("href")
                yield film_href, category_title

    async def collect_films_data(self):
        async for film, category_title in self.collect_films():
            soup = await self.send_request_(self.url + film)
            film_block = soup.find("div", class_="wrapper_movies_top_main_right")
            h1 = film_block.find("h1")
            release_year = h1.find("span").text.strip()
            title = h1.text.strip().split("(")[0]
            type = h1.text.strip().replace("(", ",").split(",")[1]
            if type == "сериал":
                type = "serial"
            elif type == "фильм":
                type = "movie"
            description = soup.find("div", class_="wrapper_movies_text")
            if description:
                description = description.text.strip()
            rating = (
                soup.find("div", class_="wrapper_movies_scores_score user_rate")
                .find("div")
                .text
            )
            data = {
                "title": title,
                "category_title": category_title,
                "rating": rating,
                "type": type,
                "release_year": release_year,
                "description": description,
            }
            yield data

    async def send_request_(self, url):
        proxy = rand_proxy()
        response = await self.client.send_request(url=url, proxy=proxy)
        soup = BeautifulSoup(response, "lxml")
        return soup


def rand_proxy():
    with open(worker_setting.PROXI_FILE_PATH) as file:
        proxy_list = "".join(file.readlines()).split("\n")
    random_proxy = random.choice(proxy_list)
    return random_proxy
