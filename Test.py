#coding=utf-8

import urllib.request
import re

# 获取html内容
def getHtmlContent(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    try:
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        content = response.read().decode(encoding='gbk')
    except urllib.request.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return content


# 获取图片页的URL
def getWorksUrl(pageNum):

    workUrlList = []
    pageUrl = "http://my.poco.cn/act/act_list.htx&p=" + str(pageNum) + "&user_id=55629005&m=all&param=0&act_type_id=0&tag_name=&m_tag=&q=&gid=-1&is_vouch=&browse="

    pageHtml = getHtmlContent(pageUrl)

    # 获取每个分页的作品链接
    patternWorks = re.compile(
            r"<h2 class=\"title\"><a href=\"(.*?)\"",
            re.M)
    worksUrl = re.findall(patternWorks, pageHtml)
    for wu in worksUrl:
        workUrlList.append(wu)

    return workUrlList


if __name__ == '__main__':
    print(getWorksUrl(3))