class URL_SQL:
    """
    url管理器，负责将爬取下的网页储存起来，以便进行下一级爬取

    """

    def __init__(self, url):
        self.url = url
        self.url_wei = set()
        self.url_yi = set()

    def sql_add(self):
        if isinstance(self.url, set):
            self.url_wei.update(self.url)
        elif isinstance(self.url, str):
            self.url_wei.add(self.url)
        else:
            pass

    def sql_get(self):
        if not self.url_wei:
            print("No URLs left to retrieve.")
            return None

        a = self.url_wei.pop()

        if a in self.url_yi:
            print(f"{a} 已爬取！")
        else:
            self.url_yi.add(a)

        return a


if __name__ == '__main__':
    a = {'wwwsad','wwwaaaa'}
    url_instance = url_sql(a)
    url_instance.sql_add()
    print(url_instance.url_wei)
    retrieved_url = url_instance.sql_get()
    print(f"Retrieved URL: {retrieved_url}")
    print(url_instance.url_wei)





