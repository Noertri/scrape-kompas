from dataclasses import dataclass, asdict
from datetime import datetime as dt
import httpx
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from sqlalchemy.dialects.sqlite import insert
from database import create_db
from models import ArticlesDB
from cacher import cached
from custom_logger import logger


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=0, i',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}


@dataclass
class Result:
    tanggal: str = ""
    judul: str = ""
    narasi: str = ""
    url: str = ""

    def __init__(self, *, tanggal, judul, narasi, url):
        self.tanggal = dt.strptime(tanggal, "%d/%M/%Y").strftime("%Y-%M-%d")
        self.judul = judul
        self.narasi = narasi
        self.url = url

        
def request_news_index(session: httpx.Client):
    for i in range(1, 301):
        url = f"https://indeks.kompas.com/?page={i}"

        try:
            response = session.get(url, headers=headers)
            yield response
        except (httpx.HTTPError, httpx.HTTPStatusError, httpx.TimeoutException) as req_error:
            logger.error(f"{i: 3d}:[{request_news_index.__name__}] {req_error} => {url}")
            yield None


def get_article_urls(source_page: str):
    soup = BeautifulSoup(source_page, "html.parser")
    a_tags = soup.select("a.article-link")

    for tag in a_tags:
        post_date = tag.select_one("div.articlePost-date").get_text(separator=" ", strip=True)
        title = tag.select_one("h2").get_text(separator=" ", strip=True)
        yield post_date, title, tag.get("href", "")


@cached
def request_article_content(session: httpx.Client, url: str):
    params = {
        'page': 'all',
    }

    try:
        response = session.get(url, headers=headers, params=params)
        return response
    except (httpx.HTTPError, httpx.TimeoutException, httpx.HTTPStatusError) as request_error:
        raise Exception("[{0}] {1} => {2}".format(request_article_content.__name__, request_error, url))


def get_article_content(source_page: str):
    soup = BeautifulSoup(source_page, "html.parser")
    tag = soup.select_one("div.read__content")
    content = tag.get_text(strip=True, separator=" ")
    return content


def scraper():
    with httpx.Client(follow_redirects=True, timeout=10.) as session:
        for page in request_news_index(session):
            if page:
                for post_date, title, link in get_article_urls(page.text):
                    response = request_article_content(session, url=link)
                    if response:
                        content = get_article_content(response.text)

                        result = Result(
                            tanggal=post_date,
                            judul=title,
                            narasi=content,
                            url=link
                        )

                        yield result


def insert_records(session: Session, records: dict[str, str]):
    stmt = insert(ArticlesDB)
    on_conflict_stmt = stmt.on_conflict_do_nothing(index_elements=[ArticlesDB.url])
    session.execute(on_conflict_stmt, records)


def main():
    db_session = create_db()
    with db_session.begin() as session:
        for result in scraper():
            if result:
                insert_records(session, asdict(result))


if __name__ == "__main__":
    main()
