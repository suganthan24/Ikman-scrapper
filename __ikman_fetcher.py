import logging
import sys
from crawler import Crawler

base_url = 'https://ikman.lk/en/ads?by_paying_member=0&sort=relevance&buy_now=0&query='


def main():
    build_query = ''
    for q in sys.argv[1:]:
        if build_query == '':
            build_query = q
        else:
            build_query = build_query + '%20' + q
    if not build_query:
        build_query = 'bmw'

    fetch_url = base_url + build_query + '&page=1'
    crawl = Crawler(fetch_url)
    crawl.crawl()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='scraper.log', format='%(asctime)s %(levelname)s:%(message)s')
    main()
