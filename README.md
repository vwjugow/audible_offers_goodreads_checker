# Audible offer pages analyzer
A scrapper that takes titles from an audible offer pages and checks if the score and amount of reviews in goodreads surpass a certain threshold.

## Installation
`pip install -r requirements.txt`

## How to use
```
AUDIBLE_OFFER_PAGE='https://www.audible.com/special-promo/2for1/cat?node=113614718011&pf_rd_p=254c7158-fcbc-44f6-8ed8-d81a71a16044&pf_rd_r=GFPHH5TSKD3JZ3K4DH94&pageLoadId=lAZD38cXtDGFiyLQ&creativeId=c575bd23-7306-4539-b129-567f29798b1d'
AUDIBLE_COOKIE='userType=amzn; at_check=true; AMCVS_165958B4533AEE5B0A490D45@AdobeOrg=1; s_cc=true; isFirstVisit=false; ubid-main=134-1530726-5422500; session-id=140-7619135-7615827; session-token=[..........]'
python scrapper.py -u ${AUDIBLE_OFFER_PAGE} -p 2 -c ${AUDIBLE_COOKIE} -s 4.04 -r 404
```
