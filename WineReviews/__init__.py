
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

def get_numwine(html):
    soup = BeautifulSoup(html, 'html.parser')
    num_wines = soup.find_all('h3', 'float-md-left font-weight-normal mb-0')
    a = num_wines[0].get_text()
    a = a.replace(',','')
    pattern = re.compile('(\d+) wines found')
    num_wine = re.findall(pattern, a)

    return num_wine[0]

def fillWinedata(Winedata,html):
    wine_infors =[]
    soup = BeautifulSoup(html, 'html.parser')

    #print(num_wine)
    #wine = soup.find_all('strong','text-uppercase')
    #Get the name of the wine
    wine_names = soup.find_all('p', 'm-0')
    #print(wine_names[0].get_text(' ','br/'))
    #Get the Vintage/Score/Release
    #wine_infor = soup.find_all('p','d-md-none mb-0')
    #Get the reviews
    wine_reviews = soup.find_all('div','collapse collapse-tn pb-16')

    #pattern = re.compile('Score range: (\d+)-(\d+)')
    #num_wine = re.findall(pattern, wine_reviews[1].get_text())
    # num_wine = re.findall(pattern, str(wine_reviews))
    # print(len(num_wine))
    # avgerage_score = round(float((int(num_wine[0][0]) + int(num_wine[0][1])) / 2), 2)
    # print(avgerage_score)

    #avgerage_score = round(float((int(num_wine[0][0])+int(num_wine[0][1]))/2),2)

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
    b = 0
    for j in range(len(wine_names)):

        if(wine_infor[a+1].get_text() == 'BT'):
            pattern = re.compile('Score range: (\d+)-(\d+)')
            num_wine = re.findall(pattern, wine_reviews[b].get_text())
            if(len(num_wine)!=0):
                avgerage_score = round(float((int(num_wine[0][0]) + int(num_wine[0][1])) / 2))
                wine_infors.append(
                    [wine_infor[a].get_text(), avgerage_score, wine_infor[a + 2].get_text()])
            else:

                wine_infors.append([wine_infor[a].get_text(), wine_infor[a + 1].get_text(), wine_infor[a + 2].get_text(',','-')])
        #     wine_infors.append([wine_infor[a].get_text(), round(float((int(num_wine[0][0])+int(num_wine[0][1]))/2),2), wine_infor[a + 2].get_text()])
        else:
            wine_infors.append([wine_infor[a].get_text(),wine_infor[a+1].get_text(),wine_infor[a+2].get_text()])
        a = a+3
        b = b+1

    for i in range(len(wine_names)):
        Winedata.append([wine_names[i].get_text(' ','br/'), wine_infors[i],wine_reviews[i].find(text=True).strip(),wine_reviews[i].find('em').get_text(),'Country: France'])


    return Winedata

def printList(Winedata,num):
    #file_handle = open('reviews.txt', mode='a',encoding="utf-8")
    for i in range(num):
        u = Winedata[i]
        print("{}\n{}\t{}\n{}\n{}\t{}\t{}\n".format(u[0],u[2],u[3],u[4],u[1][0],u[1][1],u[1][2]))
        #file_handle.writelines("{}\n{}\t{}\n{}\n{}\t{}\t{}\n".format(u[0],u[2],u[3],u[4],u[1][0],u[1][1],u[1][2]))

    #file_handle.close()



def main(url,n):
    unifo1 =[]
    html = login(url)
    #print(html)
    fillWinedata(unifo1,html)
    #print(a)
    printList(unifo1,n)

def getAllPages(url):
    html = login(url)
    a = get_numwine(html)
    return a

def getAllPages1():
    pages =[]
    for i in range(2000,2017):
        a = getAllPages("https://www.winespectator.com/wine/search?submitted=Y&page=1&winery=bordeaux+"+str(i)+"&text_search_flag=wine_plus_vintage&search_by=all&scorelow=-1&scorehigh=-1&pricelow=-1&pricehigh=-1&case_prod=null_case_prod&taste_date=&issue_date=&issue_year=&varietal%5B%5D=null_varietal&regions%5B%5D=null_regions&vintage%5B%5D=&size=15&sort_by=score&sort_dir=desc",15)
        pages.append(a)
    return pages

#main("https://www.winespectator.com/wine/search?submitted=Y&page=1&winery=bordeaux+2001&text_search_flag=wine_plus_vintage&search_by=all&scorelow=-1&scorehigh=-1&pricelow=-1&pricehigh=-1&case_prod=null_case_prod&taste_date=&issue_date=&issue_year=&varietal%5B%5D=null_varietal&regions%5B%5D=null_regions&vintage%5B%5D=&size=15&sort_by=score&sort_dir=desc",15)
main("https://www.winespectator.com/wine/search/recall/yes/page/1/sort_by/score/sort_dir/asc",15)

#pages
#a = getAllPages1()


pages = [710, 628, 537, 753, 666, 1073, 910, 491, 874, 1292, 1288, 1092, 998, 573, 853, 837,774]

print(sum(pages))

#
# year = 2000
# for j in pages:
#     print("I am in year ", + year)
#     for  i in range(int(j/15)):
#         main("https://www.winespectator.com/wine/search?submitted=Y&page="+str(i+1)+"&winery=bordeaux+"+str(year)+"&text_search_flag=wine_plus_vintage&search_by=all&scorelow=-1&scorehigh=-1&pricelow=-1&pricehigh=-1&case_prod=null_case_prod&taste_date=&issue_date=&issue_year=&varietal%5B%5D=null_varietal&regions%5B%5D=null_regions&vintage%5B%5D=&size=15&sort_by=score&sort_dir=desc",15)
#         print("I am in page " + str(i+1))
#     main("https://www.winespectator.com/wine/search?submitted=Y&page="+str(int(j/15)+1)+"&winery=bordeaux+"+str(year)+"&text_search_flag=wine_plus_vintage&search_by=all&scorelow=-1&scorehigh=-1&pricelow=-1&pricehigh=-1&case_prod=null_case_prod&taste_date=&issue_date=&issue_year=&varietal%5B%5D=null_varietal&regions%5B%5D=null_regions&vintage%5B%5D=&size=15&sort_by=score&sort_dir=desc",int(j%15))
#     year = year+1


#
# for j in pages:
#     print(year," ",j)
#     for i in range(int(j/15)):
#         print(i, " 15")
#     print((int(j/15))+1)
#     year = year +1