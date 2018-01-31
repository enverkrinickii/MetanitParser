import urllib.request
from bs4 import BeautifulSoup

metanitLink = 'https://metanit.com/'
https = 'https:'

#get all html
def GetHtml(url):
    siteHeaders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/62.0.3202.75 Safari/537.36 '
    }
    response = urllib.request.Request(url, headers=siteHeaders)
    html = urllib.request.urlopen(response).read().decode('utf-8')
    return html


# get data from html
def GetData(html, tagName, tagClass):
    soup = BeautifulSoup(html, "html.parser")
    data = soup.find(tagName, tagClass)
    return data


def GetAllData(html, tagName, tagClass):
    soup = BeautifulSoup(html, "html.parser")
    data = soup.find_all(tagName, tagClass)
    return data


def GetHrefFromChilds(data):
    list = []
    for x in data.find_all('a'):
        list.append(https + x.get('href'))
    return list


def GetHrefFromChilds1(data):
    list = []
    for x in data.find_all('a'):
        list.append(x.get('href'))
    return list


def GetHref(data):
    links = []
    for x in data:
        links.append(x.find('a').get('href'))
    return links


#ссылки с левой менюшки
def GetSubChapterLinks(link):
    html = GetHtml(link)
    menu = GetData(html, 'div', 'navmenu')
    links = GetHrefFromChilds(menu)
    return links


#из центра страницы и только у шарпов
def GetSubSectionLinks(link):
    links = GetSubChapterLinks(link)
    subSectionLinks = []
    for x in links:
        html = GetHtml(x)
        menu = GetData(html, 'ul', 'contpage')
        if menu is not None:
            subSectionLinks.append(GetHrefFromChilds1(menu))
    return subSectionLinks

#все ссылки на статьи соединяем по языку программирования
# где link - metanit.com/python for example metanit.com/pуthon + /1.1.php
#так же получаем все .php
def GetArticleLinksAndConcatThem(link):
    articleLinks = []
    html = GetHtml(link)
    data = GetAllData(html, 'span', 'file')
    for x in GetHref(data):
        articleLinks.append(link + x)
    return articleLinks

#используется если у раздела есть левая менюшка
def GetAticleSubchapterLinks(links):
    subChapterArticleLinks = []
    for link in links:
        if ".php" not in link:
            subChapterArticleLinks.append(GetArticleLinksAndConcatThem(link))
        else:
            subChapterArticleLinks.append(link)
    return subChapterArticleLinks


def GetAticleSubchapterLinksForNet(links, mainLink):
    subChapterArticleLinks = []
    for link in links:
        for x in link:
            subChapterArticleLinks.append(mainLink + x)
    return subChapterArticleLinks


def GetInfoFromLink(link):
    html = GetHtml(link)
    data = GetAllData(html, 'p', '')
    return data


def main():
    data = GetData(GetHtml(metanitLink), 'ul', 'mainmenu')
    MainLinks = GetHrefFromChilds(data)
    # subChapterLinksNet = GetAticleSubchapterLinksForNet(GetSubSectionLinks(MainLinks[0]), MainLinks[0])
    # print(GetSubSectionLinks(MainLinks[0]))
    # print(GetAticleSubchapterLinks(subChapterLinksNet))

    # subChapterLinks = GetSubChapterLinks(MainLinks[2])
    # # print(subChapterLinks)
    # print(GetAticleSubchapterLinks(subChapterLinks))

    pythonLinks = GetArticleLinksAndConcatThem(MainLinks[3])
    print(GetInfoFromLink(pythonLinks[1]))
    # print(GetArticleLinksAndConcatThem(MainLinks[3]))
    # #python
    # print(GetArticleLinksAndConcatThem(MainLinks[6]))
    # #kotlin
    # print(GetArticleLinksAndConcatThem(MainLinks[7]))
    # #go
    # print(GetArticleLinksAndConcatThem(MainLinks[8]))
    # #mongoDB
    # print(GetArticleLinksAndConcatThem(MainLinks[9]))
    # #VB
    # print(GetArticleLinksAndConcatThem(MainLinks[10]))
    #swift


if __name__ == '__main__':
    main()