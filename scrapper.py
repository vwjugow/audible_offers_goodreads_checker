import argparse
import requests
import re
from bs4 import BeautifulSoup
def _get_sale_page(url, cookie, page_number):
    url = url + f"&page={page_number}&pageSize=20"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'cookie': cookie
    }
    return requests.get(url, headers=headers)

def get_books(url, cookie, page_number):
    page = _get_sale_page(url, cookie, page_number)
    books = []
    soup = BeautifulSoup(page.content, 'html.parser')
    book_els = soup.select('ul.bc-list')
    for book in book_els:
        title = book.select('li > h3 > a')
        stitle = book.select('li.subtitle > span')
        author = book.select('li.authorLabel > span > a:first-child')
        if title:
            books.append({"name": title[0].text, "st": stitle[0].text if stitle else None, "author": author[0].text if author else None})
    return books

def _get_results_page(book):
    name = re.sub(r'[^a-zA-Z0-9 ]', '', book["name"])
    query = re.sub(r' ', '+', name)
    url=f"https://www.goodreads.com/search?utf8=%E2%9C%93&q={query}&search_type=books&search%5Bfield%5D=title"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    }
    return requests.get(url, headers=headers)

def get_gd_score(book):
    res_page = _get_results_page(book)
    soup = BeautifulSoup(res_page.content, 'html.parser')
    rating_el = soup.select('table tr:nth-child(2) span.minirating')
    num_ratings = 0
    rating = 0.0
    if rating_el:
        rating_text = rating_el[0].text.strip()
        match = re.search(r'\d+\.\d+', rating_text)
        if match:
            rating = float(match.group())
        match = re.search(r'(\d+(?:,\d+)*)\s+ratings', rating_text)
        if match:
            num_ratings = int(match.group(1).replace(",", ""))
    return rating, num_ratings

def _get_params():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-c",
        "--cookie",
        required=True,
        help="value of the cookie, used to use the same session you have on your browser.",
    )
    ap.add_argument(
        "-u",
        "--url",
        required=True,
        help="URL of the sales page you want to crawl.",
    )
    ap.add_argument(
        "-p",
        "--pages",
        choices=range(1,999),
        type=int,
        required=True,
        help="The amount of pages in the given URL with 20 items per page.",
    )
    ap.add_argument(
        "-s",
        "--score",
        type=float,
        required=False,
        default=4.0,
        help="Score to beat on Goodreads.",
    )
    ap.add_argument(
        "-r",
        "--ratings",
        type=int,
        required=False,
        default=400,
        help="Amount of ratings to beat on Goodreads.",
    )
    args = ap.parse_args()
    if args.ratings < 0:
        print("Ratings has to be a positive integer")
        sys.exit(-1)
    if args.score < 0.0 or args.score > 5.0:
        print("Score has to be a between 0.0 and 5.0")
        sys.exit(-1)
    return args.url, args.cookie, args.pages, args.score, args.ratings

def main(url, cookie, pages_amount, to_beat_score, to_beat_ratings):
    for i in range(pages_amount):
        books = get_books(url, cookie, i+1)
        if books:
            top_books = []
            for b in books:
                score, ratings = get_gd_score(b)
                if score >= to_beat_score and ratings > to_beat_ratings:
                    extension = {"score": score, "ratings": ratings}
                    top_books.append(dict(b, **extension))
            for y,x in enumerate(top_books):
                print (y, x)
            print(" ================================= ")
        else:
            print("no books found...")

if __name__ == "__main__":
    url, cookie, pages_amount, score, ratings = _get_params()
    main(url, cookie, pages_amount, score, ratings)
