import requests
from bs4 import BeautifulSoup


def parse_quote(quote):
    text = quote.find("div", attrs={"class": "quoteText"}).text.split("―")[0].strip()
    author_or_title = quote.find("span", attrs={"class": "authorOrTitle"}).text.strip()
    dict = {
        "text": text,
        "author_or_title": author_or_title,
    }
    return dict


def parse_quotes(quotes):
    parsed_quotes = []
    for quote in quotes:
        parsed_quotes.append(parse_quote(quote))
    return parsed_quotes


def parse_page(page):
    BASE_URL = "https://www.goodreads.com/quotes?page="
    url = BASE_URL + str(page)
    
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    quotes = soup.find_all("div", attrs={"class": "quote"})

    parsed_quotes = parse_quotes(quotes)
    return parsed_quotes


print(parse_page(100))