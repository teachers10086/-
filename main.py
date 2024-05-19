import tkinter as tk
from tkinter import messagebox
from threading import Thread, Event
from url_sql import URL_SQL
from url_ana import Ana
from PIL import Image, ImageTk

class CrawlerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("url获取器")
        self.root.geometry("450x250")

        # 使窗口位于屏幕中心
        self.center_window(450, 250)

        # 加载背景图片
        self.background_image = Image.open(r"C:\Users\Administrator\Desktop\新建位图图像.bmp")
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # 创建一个背景标签
        self.background_label = tk.Label(root, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        # 创建输入框和按钮等控件
        self.url_label = tk.Label(root, text="请输入网址：", bg="white", fg="black")
        self.url_label.pack(pady=5)

        self.url_entry = tk.Entry(root, width=50, bd=0, highlightthickness=0, relief='flat')
        self.url_entry.pack(pady=5)

        self.start_button = tk.Button(root, text="开始爬取", command=self.start_crawling, bd=0, highlightthickness=0, relief='flat', bg="white", fg="black")
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="停止爬取", command=self.stop_crawling, bd=0, highlightthickness=0, relief='flat', bg="white", fg="black")
        self.stop_button.pack(pady=5)

        self.status_label = tk.Label(root, text="", bg="white", fg="black")
        self.status_label.pack(pady=5)

        self.crawling_thread = None
        self.stop_event = Event()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def start_crawling(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showwarning("输入错误", "请输入有效的网址")
            return

        self.stop_event.clear()
        self.crawling_thread = Thread(target=self.crawl, args=(url,))
        self.crawling_thread.start()
        self.update_status("爬取中...")

    def stop_crawling(self):
        if self.crawling_thread:
            self.stop_event.set()
            self.crawling_thread.join(timeout=5)
            if self.crawling_thread.is_alive():
                messagebox.showinfo("提示", "爬取线程尚未结束，请稍后再试")
            else:
                self.update_status("爬取已停止")

    def crawl(self, url):
        url_sql = URL_SQL(url)
        url_sql.sql_add()

        while url_sql.url_wei and not self.stop_event.is_set():
            current_url = url_sql.sql_get()
            if current_url:
                url_ana = Ana(current_url)
                new_url_set = url_ana.ana()
                new_url_manager = URL_SQL(new_url_set)
                new_url_manager.sql_add()
                url_sql.url_wei.update(new_url_manager.url_wei)
            self.update_status(f"未爬取网页数量：{len(url_sql.url_wei)} 已爬取网页数量：{len(url_sql.url_yi)}")

        if not self.stop_event.is_set():
            self.update_status("爬取完成!!!!")

    def update_status(self, message):
        self.status_label.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    app = CrawlerApp(root)
    root.mainloop()
