#encoding = utf-8
import scrapy
import os,urllib
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

    path = 'D:\download/'
    name = os.path.join(path,file_name)
    try:
        if not os.path.exists(name):
            os.mkdir(name)
    except:
        print ("Failed to create directory in %s" % name)
        exit()
    #下载一个目录下面的所有图片
    for image in imgUrl:
        imageName = image.split('/')[-1]
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
        "http://www.mzitu.com"
    ]
    download_delay = 1

    def parse(self, response):
        for i in response.xpath('//ul[@id = "pins"]/li/span/a/@href').extract():
            yield scrapy.Request(i,callback=self.parse_picture)

        pages_link = response.xpath('//div[@ class="nav-links"]/a[@class="page-numbers"]/@href').extract()
        if pages_link not in next_page_link:
            yield scrapy.Request(pages_link,callback=self.parse)
        else:
            print('I cant')

    def parse_picture(self,response):
        item = MeizituItem()
        item['pic_name'] = response.selector.xpath("//h2/text()").extract()
        item['pic_url'] = response.selector.xpath("//div[@ class='main-image']/p/a/img/@src").extract()

        first = response.selector.xpath("//div[@ class='pagenavi']/a[2]/span/text()").extract()
        last_num = response.selector.xpath("//div[@ class='pagenavi']/a[5]/span/text()").extract()
        num = int(last_num[0]) + 1

        for i in range(2,num):
            i = str(i)
            url = first[0] + '/' + i

            img_url = scrapy.Request(url,callback=self.getImage)

            item['pic_url'].append(img_url[0])

        download(item['pic_url'],item['pic_name'][0])

    def getImage(self,response):
        return response.selector.xpath("//div[@ class='main-image']/p/a/img/@src").extract()