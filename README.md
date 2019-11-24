# ZhihuPostSpider
这次的项目和我上一个项目：https://github.com/LiDong-96/Li_Lab 的目的一样，还是爬取知乎的文章然后分析赞数。只不过是个多线程版本。
原理
------------------
#####一般的python程序都是默认单线程（线程，简单理解就是一个程序分割下来的体量更小的子程序）的，而CPU的一个核在同一时间只能运行一个线程。单线程程序只在CPU的一个核中运行。采用多线程，可以把程序分份，在多个核中同时运行。就我这个程序而言，采用的三个线程可以把整个程序的运行时间下降三分之一还不止（估计只有单线程的1/4）。我的WIN7系统内别的进程运行也一切正常，未出现明显的卡顿。由此可见，多线程是多么强大了。
#####python里的线程都是一个程序员自定义的线程类的类对象。比如你创建三个线程，首先你需要自己写一个线程类，然后用这个类创建三个对象就行。线程类是从threading模块（python3自带）里的thread类作为基类派生而来的。线程的基本通用功能pyhton开发者已经在模块里给你写好了，你只需要在派生类定义里面补充你的这个线程的功能代码就行。比如我的项目里就设计了两个线程类，一个是挖掘线程类，一个是解析线程类。然后分别创建了三个线程。
#####挖掘线程每次从页面挖掘队列CrawlQueue里面取一个页码，拼接成url然后发请求，最后把响应HTML文件压入解析队列ParseQueue；解析线程每次从解析队列里拿一个HTML文件然后用xpath或者正则等方法进一步挖掘想要的数据（我这里采集的主要就是赞数，和高赞文章的url）。
使用
------------------
#####把你的请求头填入header里面，然后找个代理填入proxy_handler里面。之后把你要爬的页面用for循环填入挖掘队列就行，一般我是一次挖1500个页面。注意如果你爬的页面超过1500个，要把队列的空间开大。如果你一次爬3000个页面，队列只有1500个空间，程序可是要卡死在这一步的。
结果
------------------
#####互联网传媒是个基尼系数极大，分配极其失衡的行业。极少数帐号和文章获取了极高的赞数（平均每1500篇文章，才有一个能达到干赞以上）。超过70%的文章是0赞，写出来几乎就没人看的。我把我粗分析的图片也发在了这个项目下。
