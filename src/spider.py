#-*-coding:utf-8-*-
import time
import queue
import threading
from urllib import request
from lxml import etree
from urllib import error

header = {"User-Agent": xxx,
          "Cookie": xxx
        }
proxy_handler = request.ProxyHandler({"socks4/5": "xxx.xxx.xxx.xxx:xxxx"})
opener = request.build_opener(proxy_handler)
request.install_opener(opener)
# 整个分析结果，将会写写入这个字典
dict_result = {}

CrawlQueue = queue.Queue(1500)
for num in range(10000000, 10001500):
    CrawlQueue.put(num)
ParseQueue = queue.Queue(1500)
crawl_exit = False
parse_exit = False

class CrawlThread(threading.Thread):
    def __init__(self, threadName, CrawlQueue, ParseQueue):
        super(CrawlThread, self).__init__()
        self.threadName = threadName
        self.CrawlQueue = CrawlQueue
        self.ParseQueue = ParseQueue
    def run(self):
        print("启动" + self.threadName)
        while not crawl_exit:
            try:
                post_num = self.CrawlQueue.get(block=False)
                try:
                    full_url = "https://zhuanlan.zhihu.com/p/" + str(post_num)
                    rqo = request.Request(full_url, headers=header)
                    rp = request.urlopen(rqo).read().decode("utf-8")
                    self.ParseQueue.put(rp)
                    print(full_url)
                except error.HTTPError:
                    pass
            except queue.Empty:
                pass
        print("退出" + self.threadName)

class ParseThread(threading.Thread):
    def __init__(self, threadName, ParseQueue):
        super(ParseThread, self).__init__()
        self.threadName = threadName
        self.ParseQueue = ParseQueue
    def run(self):
        print("启动" + self.threadName)
        while not parse_exit:
            try:
                rp = self.ParseQueue.get(block=False)
                if rp != "":    #知乎被建议修改的文章不显示赞数，但是html里面有内容
                    htmldom = etree.HTML(rp)
                    # 先用xpath获取到点赞数（返回的是个只有一项的列表，大概是“["赞同 0"]”这个样式）
                    list_ag_num = htmldom.xpath("//button[@class=\"Button VoteButton VoteButton--up\"]/@aria-label")
                    # 取列表的第0项，然后切成两片，取右边那片就是字串的赞同数
                    num_agree = (list_ag_num[0].split())[1]
                    # 如果字串长度大于等于3，或者字串里有“K”，也就是干赞，就把这个高赞（gaozan）的url保留下来
                    if len(num_agree) >= 3 or num_agree.find("K") != -1:
                        gaozan_url = htmldom.xpath("//meta[@property=\"og:url\"]/@content")
                        print(gaozan_url, ":", num_agree)
                    try:
                        dict_result[num_agree] += 1
                    except KeyError:
                        dict_result[num_agree] = 1
            except queue.Empty:
                pass
        print("退出" + self.threadName)


def zhihu_post_spider():
    """
    爬取知乎文章，分析赞数
    :return: None
    """
    start_time = time.time()
    print("起始时间：", time.asctime(time.localtime(time.time())))
    # 线程名列表
    CrawlNameList = ["挖掘线程1", "挖掘线程2", "挖掘线程3"]
    ParseNameList = ["解析线程1", "解析线程2", "解析线程3"]
    # 初始化线程的对象列表，后面主线程join()阻塞的时候要用
    crawl_list = []
    parse_list = []
    for item in CrawlNameList:
        crawl_thread = CrawlThread(item, CrawlQueue, ParseQueue)
        crawl_thread.start()
        crawl_list.append(crawl_thread)
    for item in ParseNameList:
        parse_thread = ParseThread(item, ParseQueue)
        parse_thread.start()
        parse_list.append(parse_thread)
    while not CrawlQueue.empty():
        pass
    global crawl_exit
    crawl_exit = True
    print("挖掘对列空了，挖掘线程全部退出")
    # 用线程的join方法对主线程进行阻塞，目的是让主线程等着他的儿子们（子线程）都完事，他再离开
    for thread in crawl_list:
        thread.join()
        print(1)
    while not ParseQueue.empty():
        pass
    global parse_exit
    parse_exit = True
    print("解析队列空了，解析线程全部退出")
    for thread in parse_list:
        thread.join()
        print(2)
    global dict_result
    list_ag_num = list(dict_result.keys())
    list_post_num = list(dict_result.values())
    # 把结果按「赞数:拥有这个赞数的文章数」这个格式写到文件里
    for num in range(len(list_ag_num)):
        with open("D:\\XXXXXX.txt", "a") as f:
            f.write(list_ag_num[num] + "," + str(list_post_num[num]))
            f.write("\n")
    end_time = time.time()
    print("结束时间为：", time.asctime(time.localtime(time.time())))
    workin_time = end_time - start_time
    print("工作时长为：", workin_time)


if __name__ == "__main__":
    zhihu_post_spider()
