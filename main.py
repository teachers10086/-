from url_sql import URL_SQL
from url_ana import Ana

# 初始化URL管理器
url_sql = URL_SQL("https://www.mayiwsk.com/")
url_sql.sql_add()

# 循环处理待爬取的URL集合
while url_sql.url_wei:
    url = url_sql.sql_get()  # 从待爬取集合中获取一个URL

    if url:
        # 使用Ana类解析URL并获取新的URL集合
        url_ana = Ana(url)
        new_url_set = url_ana.ana()

        # 将新获取的URL集合添加到URL管理器
        new_url_manager = URL_SQL(new_url_set)
        new_url_manager.sql_add()
        url_sql.url_wei.update(new_url_manager.url_wei)
    print(f"未爬取网页数量：{len(url_sql.url_wei)}已爬取网页数量：{len(url_sql.url_yi)}")

