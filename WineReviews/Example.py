import requests
from bs4 import BeautifulSoup
import re

def getHTMLText(url):
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status()
        r.enconding = "utf-8"
        return r.text
    except:
        return ""

def fillBookdata(Bookdata,html):
    soup = BeautifulSoup(html, 'html.parser')
    commmentinfo = soup.find_all("span", 'comment-info')
    print(commmentinfo)
    pattern = re.compile('user-stars allstar(\d+) rating')
    p = re.findall(pattern, str(commmentinfo))
    comments = soup.find_all('span', 'short')

    for i in range(len(commmentinfo)):
        Bookdata.append([commmentinfo[i].a.string, comments[i].string, p[i]])
def printList(Bookdata,num):
    for i in range(num):
        u = Bookdata[i]
        print("序号:{}\n用户名:{}\n评论内容:{}\n评分:{}星\n".format(i + 1,u[0], u[1],int(int(u[2])/10)))
def main(url):
    uinfo1 = []
    url = 'https://book.douban.com/subject/20492971/comments/hot'
    html = getHTMLText(url)
    fillBookdata(uinfo1,html)
    #printList(uinfo1,20)

main('https://book.douban.com/subject/20492971/comments/hot')
