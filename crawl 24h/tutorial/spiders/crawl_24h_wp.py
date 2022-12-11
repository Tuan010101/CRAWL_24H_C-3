import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tutorial.items import QuoteItem
import re
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import media, posts
from wordpress_xmlrpc.compat import xmlrpc_client
import urllib
import os
import requests
import shutil
from PIL import Image

wp = Client('http://localhost/wordpress/xmlrpc.php', 'tuan', 'f4w#Z84)znvNP(kI$#jsk3O&')
wp.call(GetPosts())
wp.call(GetUserInfo())

def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele
    return str1


def strip_value(value):
    m = re.search("http[^\s]+(\s)*h?(http[^\s>]+)(\s)*", value)
    if m:
        # print m.group(2).encode('UTF-8')
        return m.group(2)
    else:
        # print value.encode('UTF-8')
        return value

class QuotesSpider(CrawlSpider):
    name = "24h"
    allowed_domains = ['24h.com.vn']
    start_urls = [
            'https://www.24h.com.vn/cong-nghe-thong-tin-c55.html/',
            'https://www.24h.com.vn/game-c69.html',
            'https://www.24h.com.vn/phan-mem-ngoai-c302.html',
            'https://www.24h.com.vn/khoa-hoc-c782.html',
            'https://www.24h.com.vn/mang-xa-hoi-c889.html'
    ]
    rules = (

        Rule(LinkExtractor(allow='',
                           deny=['/abc/'],
                           process_value=strip_value,
                           restrict_xpaths=["//a[@class='d-flex align-items-center justify-content-center']"]), follow=True, process_links=None),
        Rule(LinkExtractor(allow='',
                           deny=['/abc/'],
                           process_value=strip_value,
                           restrict_xpaths=["//article[@class='cate-24h-car-news-rand__box d-flex margin-bottom-30']//a"]), follow=False, callback='parse_item',
             process_links=None)
    )
# //article[@class='cate-24h-car-news-rand__box d-flex margin-bottom-30']//a link 2
    def parse_item(self, response):
        print('Parse Item>>>>>>>>>>>>>>>>>>>>>')
        item = QuoteItem()
        item['category'] = response.xpath("//a[@class='active']/text()").get().strip()
        item['title'] = response.xpath("//h1[@id='article_title']/text()").get().strip()
        item['image'] = response.xpath("//div[@class='container']//img/@src").get()
        list_p = response.xpath("//article[@class='cate-24h-foot-arti-deta-info']/p").getall()
        item['content'] = listToString(list_p)
        item['date'] = response.xpath("//time[@class='cate-24h-foot-arti-deta-cre-post']/text()").get().strip().replace("-", "")
        item['url'] = response.request.url
        post = WordPressPost()
        post.title = item['title']
        post.content = item['content']
        post.post_status = 'publish'
        post.terms_names = {
            'post_tag': ['24h'],
            'category': [item['category']]
        }

        r = requests.get(item['image'])
        with open(f"{item['title']}.png",'wb') as f:
             f.write(r.content)
        filename = f"C:\\Users\\Admin\\crawl 24h\\tutorial\\{item['title']}.png"
        data = {    
            'name': f'{item["title"]}.jpg',
            'type': 'image/jpeg',
        }
        with open(filename, 'rb') as img:
            data['bits'] = xmlrpc_client.Binary(img.read())
        response = wp.call(media.UploadFile(data))
        attachment_id = response['id']
        post.thumbnail = attachment_id
        os.remove(f"{item['title']}.png")

        wp.call(NewPost(post))
        return  item