
import requests
from bs4 import BeautifulSoup

import re


def login(url):
    #url = 'https://www.winespectator.com/wine/search?submitted=Y&scope=ratings&winery=bordeaux'
    #url='https://www.winespectator.com/wine/search?submitted=Y&page=1&winery=bordeaux&text_search_flag=wine_plus_vintage&search_by=all&scorelow=-1&scorehigh=-1&pricelow=-1&pricehigh=-1&case_prod=null_case_prod&taste_date=&issue_date=&issue_year=&varietal%5B%5D=null_varietal&regions%5B%5D=null_regions&vintage%5B%5D=&size=15&sort_by=score&sort_dir=desc'
    header = {
        'Cookie': '_ga=GA1.2.1635341982.1567698554; _gid=GA1.2.1323968393.1567698554; __gads=ID=75b881e44fbdae2e:T=1567698553:S=ALNI_MYcKnm18GrtWj1kRJ37fu7nMN9fdA; _ceir=1; wso_session=1-5876b7247aef3669e64192c32d4ab050; bolt_session_3fd645b695cc401a1e18e1f62fad493b=ceb75294412307e0b26fcea6228957c9; __utma=93936667.1635341982.1567698554.1567698816.1567698816.1; __utmc=93936667; __utmz=93936667.1567698816.1.1.utmcsr=winespectator.com|utmccn=(referral)|utmcmd=referral|utmcct=/wine/search; xyz_cr_781_et_100==NaN&cr=781&et=100&ap=; wso_li=1; _gat=1',
        'User-Agent': 'Mozilla/5.0'

        }
    infor = requests.get(url, headers=header)

    return infor.text
    #print(infor.text)


def fillBookdata(Bookdata,html):
    wine_infors =[]
    soup = BeautifulSoup(html, 'html.parser')

    #wine = soup.find_all('strong','text-uppercase')
    #Get the name of the wine
    wine_names = soup.find_all('p', 'm-0')
    #print(wine_names[0].get_text(' ','br/'))
    #Get the Vintage/Score/Release
    #wine_infor = soup.find_all('p','d-md-none mb-0')
    #Get the reviews
    wine_reviews = soup.find_all('div','collapse collapse-tn pb-16')
    #print(wine_reviews[0].find(text=True).strip())
    # wine_judges = wine_reviews[0].find('em')
    # print(wine_judges.get_text())
    #Get the Country/region/Issus Date
    wine_country = soup.find_all('div', 'paragraph')
    #print(wine_country[0].get_text())
    # Get the Vintage/Score/Release
    wine_infor = soup.find_all('td', 'd-none d-md-table-cell border-0')
    #seperate them
    a = 0
    for j in range(len(wine_names)):
        wine_infors.append([wine_infor[a].get_text(),wine_infor[a+1].get_text(),wine_infor[a+2].get_text()])
        a = a+3


    for i in range(len(wine_names)):
        Bookdata.append([wine_names[i].get_text(' ','br/'), wine_infors[i],wine_reviews[i].find(text=True).strip(),wine_reviews[i].find('em').get_text(),wine_country[i].get_text()])
    return Bookdata

def printList(Bookdata,num):
    file_handle = open('reviews.txt', mode='a',encoding="utf-8")
    for i in range(num):
        u = Bookdata[i]
        #print("{}\n{}\t{}\n{}\n{}\t{}\t{}\t".format(u[0],u[2],u[3],u[4],u[1][0],u[1][1],u[1][2]))
    # for i in range(num):
    #     u = Bookdata[i]
    #     print("序号:{}\n用户名:{}\n评论内容:{}\n评分:{}星\n".format(i + 1,u[0], u[1],int(int(u[2])/10)))
        file_handle.writelines("{}\n{}\t{}\n{}\n{}\t{}\t{}\n".format(u[0],u[2],u[3],u[4],u[1][0],u[1][1],u[1][2]))

    file_handle.close()



def main(url):
    unifo1 =[]
    html = login(url)
    #print(html)
    fillBookdata(unifo1,html)
    printList(unifo1,15)



#main("https://www.winespectator.com/wine/search?submitted=Y&page=1&winery=bordeaux&text_search_flag=wine_plus_vintage&search_by=all&scorelow=-1&scorehigh=-1&pricelow=-1&pricehigh=-1&case_prod=null_case_prod&taste_date=&issue_date=&issue_year=&varietal%5B%5D=null_varietal&regions%5B%5D=null_regions&vintage%5B%5D=&size=15&sort_by=score&sort_dir=desc")


for  i in range(200):
    main("https://www.winespectator.com/wine/search?submitted=Y&page="+str(i+1)+"&winery=bordeaux&text_search_flag=wine_plus_vintage&search_by=all&scorelow=-1&scorehigh=-1&pricelow=-1&pricehigh=-1&case_prod=null_case_prod&taste_date=&issue_date=&issue_year=&varietal%5B%5D=null_varietal&regions%5B%5D=null_regions&vintage%5B%5D=&size=15&sort_by=score&sort_dir=desc")
    print("I am in page " + str(i))
