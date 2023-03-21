from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
from django.core.exceptions import ObjectDoesNotExist

from amedia_tracker.models import Title, Episode

BASE_URL = "https://amedia.online/"
LOGIN = ""  # credentials
PASSWORD = ""  # credentials


class Parser:
    def __init__(self):
        self.session = requests.Session()
        self.session.post(
            BASE_URL,
            {
                "login_name": LOGIN,
                "login_password": PASSWORD,
                "login": "submit",
            },
        )

    def _get_page_soup(self, page_url: str) -> BeautifulSoup:
        response = self.session.get(page_url).content
        return BeautifulSoup(response, "html.parser")

    def get_single_episode(self, episode_url: str):
        page_soup = self._get_page_soup(episode_url)
        return page_soup.select_one("iframe")["src"]

    def get_all_episodes(self, title_url, title: Title):
        title_soup = self._get_page_soup(title_url)
        episodes_soup = title_soup.select(".playlist-episodes > a")
        for episode in episodes_soup[:-1]:
            Episode.objects.update_or_create(
                number=int(episode.text.split()[0]),
                url=self.get_single_episode(episode["href"]),
                title=title,
            )

    def get_single_title_data(self, title_url: str) -> dict:
        title_soup = self._get_page_soup(title_url)
        return {
            "name": title_soup.select_one(
                "meta[property='og:title']"
            )["content"],
            "total_episodes": title_soup.select(
                ".info > span"
            )[1].text.split()[0],
         }

    def get_titles_from_single_page(self, page_soup: BeautifulSoup):
        titles_tags = page_soup.select(".newserz")
        titles_qs = Title.objects.all()
        for title in titles_tags:
            url = title.select_one(".animetitlez > a")["href"]
            title_available_episode = int(
                title.select_one(".newseriya1").text.split()[0]
                )
            try:
                title_info = titles_qs.get(url=url)
                title_qs = titles_qs.filter(url=url)
                if title_available_episode != title_info.last_available_episode:
                    title_qs.update(
                        last_available_episode=title_available_episode,
                        **self.get_single_title_data(url)
                    )
                    self.get_all_episodes(url, title_qs[0])
            except ObjectDoesNotExist:
                title = Title.objects.create(
                    url=url,
                    last_available_episode=title_available_episode,
                    **self.get_single_title_data(url)
                )
                self.get_all_episodes(url, title)

    def get_all_titles(self):
        page_soup = self._get_page_soup(urljoin(BASE_URL, "mylists/watching"))
        self.get_titles_from_single_page(page_soup)
        if page_soup.select(".pnext"):
            while page_soup.select(".pnext > a"):
                next_page_url = page_soup.select_one(".pnext > a")["href"]
                page_soup = self._get_page_soup(next_page_url)
                self.get_titles_from_single_page(page_soup)


if __name__ == "__main__":
    parser = Parser()
    parser.get_all_titles()
