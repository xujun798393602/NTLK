#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Filename: analysis_evaluate.py
运行: python analysis_evaluate.py
在以下测试环境通过:
    1.在Window7-X64 以及 Python3.6.2 或者pyhton2.7.13
需要的包: requests, jieba, snownlp

需求：
    1. 使用 selenium 或者 requests 模块抓取  华为商城荣耀9    https://www.vmall.com/product/738677717.html  的评论数据5000 条 ，保存到文件中 。
    2.  使用snownlp 模块对  该文件中的评论进行分析， 统计出   5000条里面   积极的评论 和 消极评论的 数目， 区分出 积极和消极的
    3.  使用 jieba 模块，统计出 文件中 出现最多的50个关键词，了解评论中大家最关心的手机哪些方面。
目的：
    1. 熟悉 selenium 或者 requests 模块
    2. 熟悉 大数据分析--- 文本分析的模块
要点:
    1. selenium  取 body.text  或者 requests 取 返回的代码
    2. 了解 snownlp  方法 用法
    3. 了解 jieba 分词模块的用法
分析:
        在谷歌浏览器中打开https://www.vmall.com/product/738677717.html,然后按F12打开开发者工具;选择"network",点击用户评价的第2页
        获取到https://remark.vmall.com/remark/queryEvaluate.json?pid=738677717&pageNumber=2&t=1503710872991&callback=jsonp1503710706766
    前两个参数表示是产品和页码,后两个不清楚是什么参数,并且会发生变化,去掉后两个并不会影响结果,所以我们需要访问的是
    https://remark.vmall.com/remark/queryEvaluate.json?pid=738677717&pageNumber=2
        每页10个,5000条则需要500页.
        上面的url在运行时会报错,连接到443端口.最后使用IP地址加上端口号,则能正确访问,最终访问url为
    r"http://172.19.64.37:8080/remark/queryEvaluate.json?pid=738677717&pageNumber=%d" % (page_num + 1)

        在使用jieba 分词时,出现了"，"," 。", "！","我"等单个字的分词,
    这不是我们所要的(了解评论中大家最关心的手机哪些方面),所以需要过滤掉

实现:
    main(): 主程序入口
    get_vmall_v9_evaluate() # 获取用户评价并输出到文件v9_evaluate.json中
    # 分析正面和负面评价条数,并将评价分类写入到文件v9_evaluate_positive.txt 和 v9_evaluate_negative.txt
    analysis_evaluate()
    # 根据评价内容content统计出现最多的单词
    stat_most_keywords("content")
    # 根据标签列表labelList统计出现最多的单词
    stat_most_keywords("labelList")

"""


import os
import sys
import codecs
import json
import requests
import jieba
from snownlp import SnowNLP

def get_vmall_v9_evaluate(record_page=500):
    """
     使用 requests 模块抓取  华为商城荣耀9    https://www.vmall.com/product/738677717.html  的评论数据5000 条 ，保存到文件中 。
    :param record_page:获取用户评价的记录页数,每页10条记录,缺省值为500=5000/10
    :return: None
    """
    #获得响应数据处理
    def process_page(page, record=None):
        """
        根据response返回的结果,进行数据分析
        :param page: 从服务器的来的数据
        :param record: 处理后的结果,以列表形式存放的用户评价信息,缺省为None,函数内部创建列表对象
        :return: None
        """
        # 结果列表为None时创建列表
        if record == None:
            record = []

        # 如果返回码不为200,表示已经出现错误,则打印出url后续分析
        if page.status_code != 200:
            print(page.url)
        # 如果编码不为UTF-8则转为UTF-8
        if page.encoding != "UTF-8":
            page.encoding = "UTF-8"
        # 获取回来的数据如下:jsonp1503710706766({"success":true,"page":{"firstRow":10,"pageNumber":2,"pageSize":10,"totalPage":5926,"totalRow":59253},"remarkList":[{"content":"这是我买的第四部华为手机，真的很好用，支持华为!","createDate":"2017-08-19 11:17","custId":150086000021334171,"custName":"Z***g","custNameStatus":3,"gradeCode":3,"id":4941161,"labelList":["分辨率高","画质细腻","系统流畅","照相给力","长久续航"],"msgReplyList":[{"id":870906,"isSystemAdmin":"1","isshow":"1","replyContent":"这么好用的手机，当然值得您一次次选择，有您的支持真好~","replyTime":"2017-08-19 17:29:06","replyerGradeName":"0","replyerId":969,"replyerName":"华为商城","replyerloginName":"华为商城"}],"productId":"738677717","remarkLevel":"好评","score":5},{"content":"很棒很流畅的手机，非常满意","createDate":"2017-08-19 11:06","custId":260086000244028816,"custName":"许***雁","custNameStatus":3,"gradeCode":2,"id":4941098,"labelList":["分辨率高","画质细腻","系统流畅","照相给力","物流快"],"msgReplyList":[{"id":870904,"isSystemAdmin":"1","isshow":"1","replyContent":"新一代麒麟960八核处理器，CPU多核性能提升18%，GPU性能提升180% ，快无止境！","replyTime":"2017-08-19 17:27:16","replyerGradeName":"0","replyerId":969,"replyerName":"华为商城","replyerloginName":"华为商城"}],"productId":"738677717","remarkLevel":"好评","score":5},{"content":"整体设计不错，系统运行快，物流快。","createDate":"2017-08-19 08:01","custId":300086000021600480,"custName":"h***8","custNameStatus":3,"gradeCode":2,"id":4940359,"labelList":["v9物超所值","荣耀V9"],"msgReplyList":[{"id":870901,"isSystemAdmin":"1","isshow":"1","replyContent":"咱们宝贝就是这么棒棒哒，给您的眼光点赞。","replyTime":"2017-08-19 17:25:15","replyerGradeName":"0","replyerId":969,"replyerName":"华为商城","replyerloginName":"华为商城"}],"productId":"738677717","remarkLevel":"好评","score":5},{"content":"非常感谢华为，很棒的手机📱超级喜欢，还会继续购买","createDate":"2017-08-19 06:44","custId":260086000074563907,"custName":"f***8","custNameStatus":3,"gradeCode":4,"id":4940229,"labelList":["分辨率高","系统流畅","手感超棒"],"msgReplyList":[{"id":870900,"isSystemAdmin":"1","isshow":"1","replyContent":"感谢您这么高的评价，如您喜欢记得多多推荐哦！","replyTime":"2017-08-19 17:24:33","replyerGradeName":"0","replyerId":969,"replyerName":"华为商城","replyerloginName":"华为商城"}],"productId":"738677717","remarkLevel":"好评","score":5},{"content":"挺不错的，物流特快没的说，那性能，真是我想要的快","createDate":"2017-08-19 01:00","custId":10086000027261801,"custName":"不***人","custNameStatus":3,"gradeCode":2,"id":4940070,"labelList":["我想要的快"],"msgReplyList":[{"id":870899,"isSystemAdmin":"1","isshow":"1","replyContent":"物流快、性能快，还有谁~嘻嘻!","replyTime":"2017-08-19 17:23:46","replyerGradeName":"0","replyerId":969,"replyerName":"华为商城","replyerloginName":"华为商城"}],"productId":"738677717","remarkLevel":"好评","score":5},{"content":"这物流太快了，必须给赞","createDate":"2017-08-19 00:13","custId":260086000240085358,"custName":"huafans01224864323","custNameStatus":3,"gradeCode":2,"id":4939986,"labelList":["系统流畅","照相给力","物流快","我想要的快"],"msgReplyList":[{"id":870897,"isSystemAdmin":"1","isshow":"1","replyContent":"快看快递小哥飞过去了，就是需要这种效果~","replyTime":"2017-08-19 17:22:16","replyerGradeName":"0","replyerId":969,"replyerName":"华为商城","replyerloginName":"华为商城"}],"productId":"738677717","remarkLevel":"好评","score":5},{"content":"很漂亮，非常喜欢，大力推荐","createDate":"2017-08-19 00:04","custId":80086000136856798,"custName":"s***r","custNameStatus":3,"gradeCode":2,"id":4939963,"labelList":["分辨率高"],"msgReplyList":[{"id":870896,"isSystemAdmin":"1","isshow":"1","replyContent":"精巧的工艺架构带来手机的纤薄，金属的四种配色更显时尚，无论那个角度，一个字“美”，哈哈~","replyTime":"2017-08-19 17:20:40","replyerGradeName":"0","replyerId":969,"replyerName":"华为商城","replyerloginName":"华为商城"}],"productId":"738677717","remarkLevel":"好评","score":5},{"content":"物所超值，很愉快的一次购物","createDate":"2017-08-26 09:18","custId":260086000226625641,"custName":"1***1","custNameStatus":3,"gradeCode":2,"id":4969535,"labelList":["画质细腻","系统流畅","照相给力","手感超棒","长久续航"],"msgReplyList":[],"productId":"738677717","remarkLevel":"好评","score":5},{"content":"手机发货有一点慢，可能买的人有点多，来不及出货， 但是出了以后配送速度杠杠的","createDate":"2017-08-26 09:10","custId":80086000141966332,"custName":"f***q","custNameStatus":3,"gradeCode":2,"id":4969512,"labelList":["分辨率高","画质细腻","物流快","手感好"],"msgReplyList":[],"productId":"738677717","remarkLevel":"好评","score":5},{"content":"暂未发现什么问题，还不错，只是电池没有想象中的好","createDate":"2017-08-26 09:06","custId":40086000025403594,"custName":"从***始","custNameStatus":3,"gradeCode":2,"id":4969495,"labelList":["系统流畅"],"msgReplyList":[],"productId":"738677717","remarkLevel":"好评","score":5}]})
        # 分析,去掉头尾jsonp1503710706766(和)
        startpos = page.text.find("{")
        respone_data = page.text[startpos:-1]
        # 里面的remarkList是评价列表
        respone_data = json.loads(respone_data)
        record.extend(respone_data['remarkList'])
        pass

    # http头信息,这是必须的,否则会报错
    headers={"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Cache-Control":"max-age=0",
            "Connection":"keep-alive",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
            "Host":"remark.vmall.com",
            "Referer":"https://www.vmall.com/product/738677717.html",
             "Proxy-Connection":"keep-alive"
            }
    remarkList = []
    # 遍历用户评价
    for page_num in range(0, record_page):
        # 这里需要写成IP地址加端口号的方式,否则报错.解析或代理设置有问题

        url=r"http://172.19.64.37:8080/remark/queryEvaluate.json?pid=738677717&pageNumber=%d" % (page_num + 1)
        #url=r"http://10..40.36.191:8080/remark/queryEvaluate.json?pid=738677717&pageNumber=%d" % (page_num + 1)

        
        page = requests.get(url, headers=headers)  # "page":{"firstRow":10,"pageNumber":2,"pageSize":10,"totalPage":5909,"totalRow":59084}
        process_page(page, remarkList)
    # 写文件,保存到*.py文件同目录的文件v9_evaluate.json中
    filename = os.path.join(os.path.abspath(sys.path[0]),"v9_evaluate.json")
    # 输出写的文件名
    print(convert_code("写入文件名:" + filename))

    # 以json格式保存数据,open在python2中不支持encoding参数,所以采用codecs方式打开,该方式python2,python3都支持
    with codecs.open(filename, 'w', encoding="utf-8") as file_obj:
        json.dump(remarkList, file_obj)

def read_record_file():
    """读文件评价文件(以json格式保存的)"""
    # 获取与*.py文件同目录的文件v9_evaluate.json
    filename = os.path.join(os.path.abspath(sys.path[0]), "v9_evaluate.json")
    with codecs.open(filename, 'r', encoding="utf-8") as file_obj:
        record_list = json.load(file_obj)
    return record_list

def analysis_evaluate():
    """
    使用snownlp 模块对  该文件中的评论进行分析， 统计出   5000条里面   积极的评论 和 消极评论的 数目， 区分出 积极和消极的
    """
    # 从v9_evaluate.json文件中读出数据
    record_list = read_record_file()

    # 分析
    positive_num = 0  # 正向评价记录数
    negative_num = 0  # 负向评价记录数

    #遍历记录 ,每条记录的结构示例如下:{"content":"这是我买的第四部华为手机，真的很好用，支持华为!","createDate":"2017-08-19 11:17","custId":150086,"custName":"Z***g","custNameStatus":3,"gradeCode":3,"id":4941161,"labelList":["分辨率高","画质细腻","系统流畅","照相给力","长久续航"],"msgReplyList":[{"id":870906,"isSystemAdmin":"1","isshow":"1","replyContent":"这么好用的手机，当然值得您一次次选择，有您的支持真好~","replyTime":"2017-08-19 17:29:06","replyerGradeName":"0","replyerId":969,"replyerName":"华为商城","replyerloginName":"华为商城"}],"productId":"738677717","remarkLevel":"好评","score":5}
    for record in record_list:
        positive_degree = SnowNLP(record["content"]).sentiments # 正向评价度,在0~1.0之间, 靠近0为负面评价,靠近1为正面评价
        if positive_degree < 0.5:
            negative_num += 1
            record["positive"] = 0 #消极
        else:
            positive_num += 1
            record["positive"] = 1 #积极
    print(convert_code("积极的条数:%d,消极的条数:%d,总计条数:%d" % (positive_num, negative_num, len(record_list))))

    # 将积极的和消极的评论写入文件
    try:
        # 打开正面评价文件v9_evaluate_positive.txt
        filename = os.path.join(os.path.abspath(sys.path[0]), "v9_evaluate_positive.txt")
        positive_file = codecs.open(filename, 'w', encoding="utf-8")
        print(convert_code("积极评论的文件:" + filename))
        # 打开负面评价文件v9_evaluate_negative.txt
        filename = os.path.join(os.path.abspath(sys.path[0]), "v9_evaluate_negative.txt")
        negative_file = codecs.open(filename, 'w', encoding="utf-8")
        print(convert_code("消极评论的文件:" + filename))

        # 对评价结果分为正面和负面,分别写入文件
        file_list=(negative_file, positive_file)
        for record in record_list:
            print(record["content"] + "\n")
            file_list[record["positive"]].write(record["content"] + "\n")
    finally:
        #有无错误都关闭文件
        positive_file.close()
        negative_file.close()

def stat_most_keywords(record_field_name):
    """
    使用 jieba 模块，统计出 文件中 出现最多的50个关键词，了解评论中大家最关心的手机哪些方面。
    :param record_field_name: 抽取评价记录的那个字段,目前可以从"content"和"labelList"较好
    :return: None
    """
    #读取文件
    record_list = read_record_file()  # 评价记录读到内存
    word_dict = {} # 每个单词出现的次数,使用字典方式,例如:{"画面":10, "快":20}
    for record in record_list:
        # 如果要分词的对象已经分好,列表方式,例如labelList字段,则直接引用;否则采用jieba分词进行分词
        if isinstance(record[record_field_name], list):
            word_list = record[record_field_name]
        else:
            word_list = list(jieba.cut(record[record_field_name].strip()))
        # 对评价分词后的数据进行计数
        for word in word_list:
            # 已经在字典中存在则+1,不存在,则添加字典项
            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1
    # 将字典转为列表,例如:[("画面",10), ("快",20)]
    word_list = list(word_dict.items())
    # 因为1个汉字不能表达足够的意思,所以过滤掉
    word_list = list(filter(lambda x: len(x[0]) > 1, word_list))
    # 对列表中按统计次数降序排列
    word_list.sort(key=lambda word_num : word_num[1], reverse=True)
    # 将列表中的前50个单词进行输出
    print(convert_code("根据(%s)统计,出现最多的50个关键词:" % record_field_name ))
    print(",".join([ x[0] for x in word_list[0:50]]))

def convert_code(src_str):
    """对utf-8源码文件中的汉字串进行转码,否则在python2中出现乱码"""
    import sys
    if sys.version_info.major == 2:
        return unicode(src_str.decode("utf-8"))
    else:
        return src_str

# 主程序入口
def main():
    # 获取用户评价并输出到文件v9_evaluate.json中
    get_vmall_v9_evaluate(500)
    # 分析正面和负面评价条数,并将评价分类写入到文件v9_evaluate_positive.txt 和 v9_evaluate_negative.txt
    analysis_evaluate()
    # 根据评价内容content统计出现最多的单词
    stat_most_keywords("content")
    # 根据标签列表labelList统计出现最多的单词
    stat_most_keywords("labelList")
    return 0

# 程序入口和返回值处理
if __name__ == "__main__":
    sys.exit(main())
    pass

