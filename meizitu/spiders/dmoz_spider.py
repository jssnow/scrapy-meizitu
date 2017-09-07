#encoding = utf-8
import scrapy
import os,urllib
import time
from meizitu.items import MeizituItem

next_page_link = []
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Referer': 'http://www.mzitu.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
}
def download(imgUrl,pic_name):
    file_name = pic_name

    path = 'D:\image/'
    name = os.path.join(path,file_name)
    if not os.path.exists(name):
        os.mkdir(name)

    #下载一个目录下面的所有图片
    imageName = imgUrl.split('/')[-1]
    rep = urllib.request.Request(imgUrl,headers=headers)
    data = urllib.request.urlopen(rep).read()
    path = name + '/' + imageName
    f = open(path, "wb")
    f.write(data)
    f.close()

class DmozSpider(scrapy.Spider):
    """docstring for DmozSpider"""

    name = 'dmoz'
    allowed_domains = ["www.mzitu.com"] #爬虫运行的地址,不能超出这个网站
    start_urls = [
        "http://www.mzitu.com/page/5"
    ]
	#延时
    download_delay = 2

    def parse(self, response):
        for i in response.xpath('//ul[@id = "pins"]/li/span/a/@href').extract():
            yield scrapy.Request(i,callback=self.parse_picture)
            # for num in range(1,50):
            #     if num == 1:
            #         yield scrapy.Request(i,callback=self.parse_picture)
            #     else:
            #         num = str(num)
            #         url = i + '/' + num
            #         yield scrapy.Request(url, callback=self.parse_picture)

        pages_link = response.xpath('//div[@ class="nav-links"]/span[@class="page-numbers current"]/following-sibling::a[1]/@href').extract()
        yield scrapy.Request(pages_link[0],callback=self.parse)

    def parse_picture(self,response):
        item = MeizituItem()
        item['pic_name'] = response.selector.xpath("//div[@ class='main-image']/p/a/img/@alt").extract()
        item['pic_url'] = response.selector.xpath("//div[@ class='main-image']/p/a/img/@src").extract()
        download(item['pic_url'][0],item['pic_name'][0])
        next_pic_text = response.selector.xpath("//div[@ class='pagenavi']/span[not(@class='dots')]/following-sibling::a[1]/span/text()").extract()
        if next_pic_text[0] != '下一组»':
            next_pic = response.selector.xpath("//div[@ class='pagenavi']/span[not(@class='dots')]/following-sibling::a[1]/@href").extract()
            yield scrapy.Request(next_pic[0],callback=self.parse_picture)
