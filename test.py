import unittest
from crawler import Crawler
import os
import requests
from bs4 import BeautifulSoup


class IkmanScrapper(unittest.TestCase):
    base_url = "https://ikman.lk/en/ads?by_paying_member=0&sort=relevance&buy_now=0&query="

    def __init__(self, testname, build_query):
        super().__init__(testname)
        self.build_query = build_query
        self.url = self.base_url + self.build_query + '&page='

    def setUp(self):
        self.url = 'https://ikman.lk/en/ads?by_paying_member=0&sort=relevance&buy_now=0&query=bmw&page=1'
        r = requests.get(self.url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            self.ads_list = soup.find_all('li', attrs={"class": "normal--2QYVk gtm-normal-ad"})
        self.ad_url = 'https://ikman.lk/en/ad/bmw-x1-x-line-2018-for-sale-colombo-39'

    def test_crawl(self):
        f = open('ads.json', 'w')
        f.close()
        os.remove(f.name)
        crawl = Crawler(self.url)
        crawl.crawl()
        f = open('ads.json', 'w')
        self.assertIsNotNone(f)

    def test_get_ads_list(self):
        crawl = Crawler(self.url)
        output = crawl.get_ads_list()
        self.assertIsNotNone(output)
        self.assertTrue(isinstance(output, list))

    def test_get_ads_detail_json(self):
        crawl = Crawler(self.url)
        output = crawl.get_ads_detail_json(self.ads_list)
        self.assertIsNotNone(output)
        self.assertTrue(isinstance(output, list))

    def test_fetch_ad_detail(self):
        crawl = Crawler(self.url)
        output = crawl.fetch_ad_detail(self.ad_url)
        self.assertIsNotNone(output)
        self.assertTrue(isinstance(output, dict))


if __name__ == '__main__':
    import sys
    build_query = ''
    for q in sys.argv[1:]:
        if build_query == '':
            build_query = q
        else:
            build_query = build_query + '%20' + q

    if not build_query:
        build_query = 'bmw'

    test_loader = unittest.TestLoader()
    test_names = test_loader.getTestCaseNames(IkmanScrapper)

    suite = unittest.TestSuite()
    for test_name in test_names:
        suite.addTest(IkmanScrapper(test_name, build_query))

    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())


