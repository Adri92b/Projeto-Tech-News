import requests
import time
from parsel import Selector
from .database import create_news


# Requisito 1
def fetch(url):
    try:
        result = requests.get(
            url,
            headers={"user-agent": "Fake user-agent"},
            timeout=3)
        time.sleep(1)
        if result.status_code == 200:
            return result.text
        else:
            return None
    except requests.ReadTimeout:
        return None


# Requisito 2
def scrape_novidades(html_content):
    selector = Selector(html_content)
    lista_links = []
    for card in selector.css(".cs-overlay-link"):
        links = card.css("a::attr(href)").get()
        lista_links.append(links)
    return lista_links


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(html_content)
    next_page_url = selector.css(".next::attr(href)").get()
    if not next_page_url:
        None
    return next_page_url


# Requisito 4
def scrape_noticia(html_content):
    selector = Selector(html_content)
    result = {
        "url": selector.css('link[rel="canonical"]::attr(href)').get(),
        "title": selector.css('.entry-title::text').get().strip(),
        "timestamp": selector.css('.meta-date::text').get(),
        "writer": selector.css('.meta-author .author a::text').get(),
        "comments_count": len(selector.css('div.comment-body').getall()),
        "summary": selector.xpath(
            'string(//div[@class="entry-content"]//p)').get().strip(),
        "tags": selector.css('.post-tags a[rel="tag"]::text').getall(),
        "category": selector.css('.meta-category span.label::text').get()
    }
    return result


# Requisito 5
def get_tech_news(amount):
    request_fetch = fetch("https://blog.betrybe.com")
    selector_scrape = scrape_novidades(request_fetch)
    news = []
    while len(selector_scrape) < amount:
        link_next_page = scrape_next_page_link(request_fetch)
        request_fetch = fetch(link_next_page)
        selector_scrape.extend(scrape_novidades(request_fetch))

    for link in selector_scrape[:amount]:
        new_request_fetch = fetch(link)
        get_data = scrape_noticia(new_request_fetch)
        news.append(get_data)

    create_news(news)
    return news
