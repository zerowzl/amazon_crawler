import time
import urllib

import scrapy
from openpyxl import load_workbook


class AmazonSearchSpider(scrapy.Spider):
    name = 'amazonSearch'

    def start_requests(self):
        keys = self.getExcelSearchKeys()

        urls = [
            'http://www.amazon.com/s'
        ]

        headers = {
            "user-agent": "Mozilla/5.0"
        }

        for key in keys:
            url_key = key.replace(" ", "+")
            params = {
                "k": url_key
            }
            url = f'{urls[0]}?{urllib.parse.urlencode(params)}'
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 headers=headers,
                                 meta={"key": key})

    def parse(self, response):
        print(f"response.status: {response.status}")
        # print(response.text)
        # data-component-type="s-result-info-bar"
        # response.css("span[data-component-type=s-result-info-bar]").getall()
        # spans = response.css("div[class=a-section]").getall()

        # 获取搜索结果
        key = response.meta["key"]
        result = response.xpath('//*[@id="search"]/span/div/span/h1/div/div[1]/div/div/span[1]/text()').get()
        print(key)
        print(result)

        # 1-16 of over 10,000 results for
        # 1-16 of 148 results for

        # 解析数量
        num = result.split(" ")[-3]
        print(f"搜索结果数量:{num}")

        length = len(num)
        print(length)
        if length < 4:
            print("搜索结果小于1000")
        else:
            print("搜索结果大于1000")
            # file = open("result.json", "w")
            # file.write(key + "\n")

        # text = response.text
        # re.findall("results for")

        """
        {
        b'User-Agent': [b'Mozilla/5.0'], 
        b'Accept': [b'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'],
        b'Accept-Language': [b'en'], 
        b'Accept-Encoding': [b'gzip, deflate'], 
        b'Cookie': [b'session-id=138-1505702-2308006; session-id-time=2082787201l; i18n-prefs=USD; sp-cdn="L5Z9:CN"']
        }
        
        {
        b'User-Agent': [b'Mozilla/5.0'], 
        b'Accept': [b'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'], 
        b'Accept-Language': [b'en'], 
        b'Accept-Encoding': [b'gzip, deflate']
        }
        
        """
        # r = response.request
        # print(r.headers)

    def getExcelSearchKeys(self) -> list:
        # 加载Excel
        start_time = time.time()
        filename = "C:\\Users\\zz445\\Documents\\搜索词 - 副本.xlsx"
        wb = load_workbook(filename)
        end_time = time.time()
        print(f"完成解析Excel:{end_time - start_time}")

        # 获取第一个 Sheet
        first_sheet = wb.sheetnames[0]
        ws = wb[first_sheet]

        # 解析搜索词
        keys = []
        for row in range(3, ws.max_row + 1):
            for column in "A":
                cell_name = "{}{}".format(column, row)
                keys.append(ws[cell_name].value)

        return keys
