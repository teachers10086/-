from bs4 import BeautifulSoup
import requests
from url_sql import URL_SQL
import os
import re

class Ana:
    """
    URL解析器，负责爬取传入的URL的下一级URL并返回一个集合
    """

    def __init__(self, url):
        self.url = url

    def sanitize_filename(self, filename):
        # 移除不可见字符并用下划线替换非法字符
        return re.sub(r'[^\w\s-]', '_', filename.strip())

    def ana(self):
        try:
            r = requests.get(self.url)
            r.encoding = r.apparent_encoding
            if r.status_code != 200:
                print(f"{self.url}网页连接失败，错误代码：{r.status_code}")
                return set()
            soup = BeautifulSoup(r.text, 'html.parser')
            a = soup.find_all('a')
            urlset = set()

            folder_path = r"D:\目录"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"已创建文件夹: {folder_path}")

            for i in a:
                if 'href' in i.attrs:
                    sanitized_filename = self.sanitize_filename(i.text)
                    with open(os.path.join(folder_path, f"{sanitized_filename}.txt"), "a", encoding='utf-8') as f:
                        f.write(i.text + ":" + i.attrs['href'] + "\n")
                    if 'http' in i.attrs['href'] and ('.com' in i.attrs['href'] or '.net' in i.attrs['href'] or '.cn' in i.attrs['href']):
                        urlset.add(i.attrs['href'])
                else:
                    print("本页面无URL")
            print(f"{self.url}爬取完毕！")
            return urlset
        except Exception as e:
            print(f"爬取网页：{self.url}时，出现错误：{e}")
            return set()

if __name__ == '__main__':
    nan = Ana('https://www.example.com/')
    b = nan.ana()
    print("*" * 30)
    print(b)
    a = URL_SQL(b)
    a.sql_add()
    print(a.url_wei)
    a.sql_get()
    print(a.url_yi)
    a.sql_get()
    print(a.url_yi)
