import requests
from bs4 import BeautifulSoup


url = 'https://pc.weixin.qq.com'
async def download_setup(url,keywords):
    response = requests.get(url)
    url_text = BeautifulSoup(response.text, 'html.parser')
    specific_links = []
    for link in url_text.find_all('a', href=True):
        if keywords in link.get('href'):  
            specific_links.append(link.get('href'))
    for link in specific_links:
        print('获取到' + keywords + '的链接：' + link)
        return link

