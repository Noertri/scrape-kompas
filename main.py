import httpx
from bs4 import BeautifulSoup


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

        
def request_news_index(session: httpx.Client):
    for i in range(1, 301):
        url = f"https://indeks.kompas.com/?page={i}"
        response = session.get(url, headers=headers)

        if response.status_code < 400:
            yield response


def get_article_urls(source_page: str):
    soup = BeautifulSoup(source_page, "html.parser")
    a_tags = soup.select("a.article-link")

    for tag in a_tags:
        post_date = tag.select_one("div.articlePost-date").get_text(separator=" ", strip=True)
        title = tag.select_one("h2").get_text(separator=" ", strip=True)
        yield post_date, title, tag.get("href", "")


def request_article_content(session: httpx.Client, url: str):
    params = {
        'page': 'all',
    }

    response = session.get(url, headers=headers, params=params)

    if response.status_code < 400:
        return response


def get_article_content(source_page: str):
    soup = BeautifulSoup(source_page, "html.parser")
    p_tags = soup.select("div.read__content p")
    content = "\n".join([tag.get_text(strip=True, separator=" ") for tag in p_tags])
    return content


def scraper():
    with httpx.Client(follow_redirects=True, timeout=10.) as session:
        for page in request_news_index(session):
            for post_date, title, link in get_article_urls(page.text):
                response = request_article_content(session, link)
                if response:
                    content = get_article_content(response.text)

                    result = {
                        "tanggal": post_date,
                        "judul": title,
                        "narasi": content,
                        "url": link
                    }

                    yield result


if __name__ == "__main__":
    scraper()