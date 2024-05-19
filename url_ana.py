from bs4 import BeautifulSoup
import requests

class Ana:
    """
    urlj解析器，负责爬取传入的URL的下一级url并返回一个集合

    """


    def __init__(self,url):
        self.url=url

    def ana(self):
        try:
            r = requests.get(self.url)
            r.encoding = r.apparent_encoding
            if r.status_code != 200:        #判断网页响应码是否为200，如果不是则为连接成功
                print(f"网页连接失败，错误代码：{r.status_code}")
                return set()        #未成功返回空集合
            soup = BeautifulSoup(r.text,'html.parser')
            a = soup.find_all('a')
            urlset = set()      #初始化一个集合，用于存放待爬取的URL，以便将待爬取的url存入url管理器中
            for i in a:
                if 'href' in i.attrs:       #判断页面中有没有url
                    with open("wangzhi.txt", "a", encoding='utf-8') as f:
                        f.write(i.text + ":" + i.attrs['href'] + "\n")      #如果有就将url和标签名写入txt中
                    if 'http' in i.attrs['href'] and '.com' in i.attrs['href']:     #判断这个URL是否包括http和.com，因为requests只能解析带http的URL
                        urlset.add(i.attrs['href'])     #只有带http的url才能放入url管理器中
                    else:
                        continue
                else:
                    print("本页面无URL")        #如果网页中没有url，
                    continue
            print(self.url+'爬取完毕！')
            return urlset
        except Exception as e:
            print(f"爬取网页：{self.url}时，出现错误：{e}")
            return set()


if __name__ == '__main__':
    nan = Ana('https://www.mayiwsk.com/')
    b = nan.ana()
    print("*"*30)
    print(b)
    from url_sql import URL_SQL
    a = URL_SQL(b)
    a.sql_add()
    print(a.url_wei)
    a.sql_get()
    print(a.url_yi)
    a.sql_get()
    print(a.url_yi)
