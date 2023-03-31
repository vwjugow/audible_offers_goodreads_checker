import requests
import re
from bs4 import BeautifulSoup

def _get_sale_page(page_number):
    url = f"https://www.audible.com/special-promo/2for1/cat?creativeId=ad13e9b6-ce52-4507-bc19-1434efe782b3&creativeId=19a002a1-f739-4ef1-ac45-a57d33654752&loginAttempt=true&node=96706886011&pageLoadId=ZdXhE5mlGyQVKwOw&pageLoadId=lf6V7GS9JpqJlyiZ&ref=a_special-p_c4_pageNum_1&pf_rd_p=e1ab1d91-96b3-4a0b-b0cf-1c06993c52ea&pf_rd_r=68KT5XTWJ07T1HWDT3BQ&pageLoadId=PD13iQsJiowNhtT5&creativeId=19a002a1-f739-4ef1-ac45-a57d33654752&pageSize=50&page={page_number}"
    cookie = 'userType=amzn; at_check=true; AMCVS_165958B4533AEE5B0A490D45@AdobeOrg=1; s_cc=true; isFirstVisit=false; originalSourceCode="AUDOR6280306239X49_03/13/2023 12:22"; adobeujs-optin={"aam":true,"adcloud":true,"aa":true,"campaign":true,"ecid":true,"livefyre":true,"target":true,"mediaaa":true}; RoktRecogniser=33d5fd61-8aa1-41f5-afcd-9f17d7f3f2ec; ubid-main=134-1530726-5422500; session-id=140-7619135-7615827; x-main="e4YLhh8y@4ZeXOn@TzM2A89rWTLA4Kicp0?i94FtlEgmKMtJ1CIsHI?3N@EoI1bR"; at-main=Atza|IwEBIPm6T8GHWyhuTpI1_hZHgDlkQd2bEb8fVry0bGpEnmkueAwXmwsRq3L4cmMDJaPPLTs6Lu4O99n_W4cBUHABSXYWI-9ZJstKgdbnREWKZD-roH2jJ_1gOfxyHNgMI3m5ebE7C3MIFV8OgWPqz6d9l-XvINW3a9SPiicwdUw5H8RwJibHGhwydDL0eNmc6maNda60CYJKHb3_hax6SrfxapxR; sess-at-main="PcDjDVXlNr+6ykD7lX52TftcUqQnd6Zp4o4xUfNWKsw="; session-id-time=2082787201l; currentSourceCode="ANONAUDW0378WS010202_03/31/2023 11:28"; s_gpv=2for1-cat; s_inv=3814; session-token=VQ03BEZxUEuiW7YeQZen4SkeZ3l+t8fSdzincvyn95cKcJVviqKph4t6gkCdFP38Y67zCXK6AeTJPgrxa5wEUqGAb2FB5LyCAjn89x3652L7vFJV+/KasXrq315tZRWMJLQKGstLg6UrAhSIZ2TrZRug1h+W1K5ipoeVJTFBMqwKhIlnST8LBwMagsvz9h6baDnvKpRSPtpeVx7N5qMXr7yVbob2ZMJDwKCkBefCb/I=; s_ips=947; s_plt=4.58; s_pltp=2for1-cat; mbox=PC#ed6df4207f27476ba38b860a498abd74.34_0#1743514308|session#0fcd52be091042f68e1f002aa334fcac#1680271368; csm-hit=adb:adblk_no&t:1680270033188&tb:NPATPFG91EGP6ECTSWG0+s-7Y82A2E1GNHTJG7MDJ4J|1680270033188; s_nr30=1680270035334-Repeat; s_tslv=1680270035334; AMCV_165958B4533AEE5B0A490D45@AdobeOrg=359503849|MCIDTS|19448|MCMID|14016188145344356641146955511388677887|MCAID|NONE|MCOPTOUT-1680277235s|NONE|vVersion|5.0.1; s_tp=14722; s_ppv=2for1-cat,39,6,5795,6,15'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'cookie': cookie
    }
    return requests.get(url, headers=headers)

def get_books(page_number):
    page = _get_sale_page(page_number)
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

def main():
    for i in range(3):
        books = get_books(i+1)
        if books:
            top_books = []
            for b in books:
                score, ratings = get_gd_score(b)
                if score >= 4.0 and ratings > 400:
                    extension = {"score": score, "ratings": ratings}
                    top_books.append(dict(b, **extension))
            for i,x in enumerate(top_books):
                print (i, x)
            print(" ================================= ")
        else:
            print("no books found...")

if __name__ == "__main__":
    main()
