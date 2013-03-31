import httplib
from bs4 import BeautifulSoup
import re
import urllib
import sys


class Crawler():
    def __init__(self):
        self.query_term = sys.argv[1]
        self.base = "www.google.co.uk"
        search = "/search?tbm=isch&q="+self.query_term
        self.connection = httplib.HTTPConnection(self.base)
        page = self.get_query(search)
        pic_link = self.get_pic(page)
        print pic_link
        urllib.urlretrieve(pic_link, self.query_term+'.jpg')
        self.write_html()

    def get_page(self, path):
        self.connection.request("GET", path)
        return self.connection.getresponse()

    def get_query(self, path):
        response = self.get_page(path)
        return response.read()

    def get_pic(self, page):
        source = BeautifulSoup(page)
        article = source.find("div", {"id": "center_col"})
        link = article.findAll('a')[0]['href']
        return self.get_img_src(link)

    def get_img_src(self, link):
        return re.findall(".*imgurl=(.*?)&imgrefurl.*", link)[0]

    def write_html(self):
        with open('index.html', 'w') as f:
            f.write('<html>' +
                    '<head>' +
                    '<script src="speakClient.js"></script>' +
                    '</head>' +
                    '<body>' +
                    '<img src="'+self.query_term+'.jpg"><br><h3>' + self.query_term + '</h3>' +
                    '<button onclick="speak(\'' + self.query_term + '\')">Talk</button>' +
                    '<div id="audio"></div>' +
                    '</body>' +
                    '</html>')


if __name__ == "__main__":
    spider = Crawler()
