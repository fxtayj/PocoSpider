# coding=utf-8

import urllib.request
import re
import os


# 显示下载进度
def schedule(a, b, c):
    """
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
    """
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
        # print('%.2f%%' % per)


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
def getWorksUrl(index_url,pageNum):

    workUrlList = []

    page_url = ""
    if(index_url == None):
        page_url = "http://my.poco.cn/act/act_list.htx&p=" + str(pageNum) + "&user_id=55629005&m=all&param=0&act_type_id=0&tag_name=&m_tag=&q=&gid=-1&is_vouch=&browse="
    else:
        page_url = index_url

    pageHtml = getHtmlContent(page_url)

    # 获取每个分页的作品链接
    patternWorks = re.compile(
            r"<h2 class=\"title\"><a href=\"(.*?)\"",
            re.M)
    worksUrl = re.findall(patternWorks, pageHtml)
    for wu in worksUrl:
        workUrlList.append(wu)
    return workUrlList

# 下载图片
def downloadImg(html):
    global publishDate
    global title
    pattern = re.compile(r"photoImgArr\[[1-9]\].orgimg = \'([a-zA-z]+://[^\s]*)\'", re.I)
    imglist = re.findall(pattern, html)

    # 抓取作品发表时间
    patternDate = re.compile(
            r"发表日期：([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8])))",
            re.I)
    folderDate = re.findall(patternDate, html)
    for fd in folderDate:
        publishDate = fd[0] + "-" + fd[1]

    # 抓取作品标题
    patternTitle = re.compile(
            r"<h1 class=\"mt10\">(.*?)<",
            re.I)
    folderTitle = re.findall(patternTitle, html)
    for ft in folderTitle:
        title = ft.strip()

    # 定义文件夹的名字
    foldername = str(publishDate)
    picpath = '/Users/tao/personal/images/RayShen/%s_%s' % (foldername, title)  # 下载到的本地目录

    if not os.path.exists(picpath):  # 路径不存在时创建一个
        os.makedirs(picpath)
    x = 0
    for imgurl in imglist:
        target = picpath + '/%s_%s.jpg' % (title, x)
        print('Downloading image to location: ' + target + '\nurl=' + imgurl)
        image = urllib.request.urlretrieve(imgurl, target, schedule)
        x += 1
    return image;


if __name__ == '__main__':
    print('''       *************************************
      **	  Welcome to use Image Spider	  **
      **	  Created on  2015-12-22	      **
      **	  @author: tao		              **
      **************************************''')
    indexUrl = "http://my.poco.cn/act-act_list-htx-user_id-55629005.shtml"

    errorUrl = "http://my.poco.cn/act/act_list.htx&p=6&user_id=55629005&m=all&param=0&act_type_id=0&tag_name=&m_tag=&q=&gid=-1&is_vouch=&browse="

    pageUrlList = []
    for x in range(16,20):
        urls = getWorksUrl(None,x)
        pageUrlList.append(urls)
    # pageUrlList.append(getWorksUrl(indexUrl,None))
    # pageUrlList.append(getWorksUrl(errorUrl,None))

    for uls in pageUrlList:
        for url in uls:
            html = getHtmlContent(url)
            downloadImg(html)

    print("Download has finished.")
