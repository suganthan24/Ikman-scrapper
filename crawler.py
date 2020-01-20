import json
import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class Crawler(object):

    def __init__(self, url):
        self.base_url = url
        self.site_url = 'https://ikman.lk'

    def crawl(self):
        ads_list = self.get_ads_list()
        logger.info(f'Total number of ads crawled: {len(ads_list)}')
        ads_detail_json = self.get_ads_detail_json(ads_list)
        with open('ads.json', 'w') as json_file:
            json.dump(ads_detail_json, json_file, indent=4)

    def get_ads_list(self):
        r = requests.get(self.base_url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            first_ad = soup.find_all('li', attrs={"class": "normal--2QYVk gtm-normal-ad first-add--1u5Mw"})
            ads = soup.find_all('li', attrs={"class": "normal--2QYVk gtm-normal-ad"})
            return first_ad + ads
        else:
            logger.warn(f"request fails for '{url}'")

    def get_ads_detail_json(self, ad_list):
        ad_detail_list = []
        for ad in ad_list:
            title = ad.find('span', attrs={"class": "title--3yncE"}).text
            short_description = ad.find('div', attrs={"class": "description--2-ez3"}).text
            url = self.site_url + ad.find('a')['href']
            price = ad.find('div', attrs={"class": "price--3SnqI color--t0tGX"}).span.text
            ad_detail = self.fetch_ad_detail(url)
            ad_detail_list.append({
                'title': title,
                'date': ad_detail['date'],
                'short_description': short_description,
                'category': ad_detail['category'],
                'url': url,
                'details': {
                    'full_description': ad_detail['description'],
                    'image_urls': ad_detail['image_urls'],
                    'price': price,
                    'contact': ad_detail['contact']
                }
            })
        return ad_detail_list

    def fetch_ad_detail(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            title = soup.find('div', attrs={"class": "ui-panel-content ui-panel-block"}).h1.text
            try:
                date = soup.find("span", attrs={"class": "date"}).text
            except Exception:
                logger.warn(f"Date is not there in '{title}' ad")
                date = ''

            try:
                description = soup.find("div", attrs={"class": "item-description"}).p.text
            except Exception:
                logger.warn(f"description is not there in '{title}' ad")
                description = ''

            try:
                image_urls = []
                imgs = (soup.find('div', attrs={"class": "gallery-nav"})).find_all('a')
                for img in imgs:
                    img_url = img.img['src'][2:]
                    image_urls.append(img_url)
            except Exception:
                logger.warn(f"image_urls is not there in '{title}' ad")
                image_urls = []

            try:
                contact = soup.find("span", attrs={"class": "h3"}).text
            except Exception:
                logger.warn(f"contact is not there in '{title}' ad")
                contact = ''

            try:
                category = (soup.find('nav', attrs={"class": "ui-crumbs"})).find_all('li')[5].a.span.text
            except Exception:
                logger.warn(f"category is not there in '{title}' ad")
                category = ''

            return {
                'date': date,
                'description': description,
                'image_urls': image_urls,
                'contact': contact,
                'category': category
            }
        else:
            logger.warn(f"request fails for '{url}'")
