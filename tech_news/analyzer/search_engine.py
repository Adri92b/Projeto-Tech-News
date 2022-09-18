from tech_news.database import search_news
from datetime import datetime


# Requisito 6
def search_by_title(title):
    search = {'title': {"$regex": title, "$options": 'i'}}
    title_search = search_news(search)
    result = [(new['title'], new['url']) for new in title_search]
    return result


# Requisito 7
def search_by_date(date):
    try:
        date = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
        search = search_news({'timestamp': date})
        result_date = [(new['title'], new['url']) for new in search]
        return result_date
    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
def search_by_tag(tag):
    search = search_news(
        {"tags": {"$elemMatch": {"$regex": f"{tag}", "$options": "i"}}}
    )
    search_list = []
    for news in search:
        search_list.append((news["title"], news["url"]))
    return search_list


# Requisito 9
def search_by_category(category):
    search = search_news({"category": {"$regex": category, "$options": "i"}})
    search_list = []
    for news in search:
        search_list.append((news["title"], news["url"]))
    return search_list
