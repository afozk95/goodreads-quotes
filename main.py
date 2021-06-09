from typing import Any, Dict, List, Union
import json
import bs4
import requests


def get_full_url(relative_url: str) -> str:
    BASE_URL = "https://www.goodreads.com"
    if not relative_url.startswith("/"):
        relative_url = "/" + relative_url
    return BASE_URL + relative_url


def parse_quote(quote: bs4.element.Tag) -> Dict[str, Any]:
    quote_dict = {}

    text = quote.find("div", attrs={"class": "quoteText"}).text.split("―")[0].strip()
    quote_dict["text"] = text

    author = quote.find("span", attrs={"class": "authorOrTitle"}).text.strip()
    if author[-1] == ",":
        author = author[:-1]
    quote_dict["author"] = author

    title_element = quote.find("a", attrs={"class": "authorOrTitle"})
    if title_element is not None:
        title = title_element.text.strip()
        title_url = get_full_url(title_element["href"])
        quote_dict["title"] = title
        quote_dict["title_url"] = title_url

    like_count_element = quote.find("a", attrs={"class": "smallText"})
    like_count = int(like_count_element.text.split(" ")[0])
    quote_dict["like_count"] = like_count
    quote_url = get_full_url(like_count_element["href"])
    quote_dict["quote_url"] = quote_url

    tags_container_element = quote.find("div", attrs={"class": "smallText"})
    if tags_container_element is not None:
        tags = [e.text for e in tags_container_element.find_all("a")]
        quote_dict["tags"] = tags

    return quote_dict


def parse_quotes(quotes: List[bs4.element.Tag]) -> List[Dict[str, Any]]:
    return [parse_quote(quote) for quote in quotes]


def parse_page(page: Union[int, str]) -> List[Dict[str, Any]]:
    if isinstance(page, str):
        page = int(page)

    url = f"https://www.goodreads.com/quotes?page={page}"

    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.content, "html.parser")
    quotes = soup.find_all("div", attrs={"class": "quote"})

    return parse_quotes(quotes)


def parse_all_pages(verbose: bool = False) -> List[Dict[str, Any]]:
    PAGE_START = 1
    PAGE_END = 100
    all_parsed_quotes = []
    for page in range(PAGE_START, PAGE_END + 1):
        if verbose:
            print(f"parsing page {page}")
        parsed_quotes = parse_page(page)
        all_parsed_quotes.extend(parsed_quotes)
    return all_parsed_quotes


def write_to_json(path: str, data: List[Dict[str, Any]]) -> None:
    with open(path, "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    quotes = parse_all_pages(verbose=True)
    write_to_json("all_popular_quotes.json", quotes)
