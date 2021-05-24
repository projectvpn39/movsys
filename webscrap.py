import requests
from bs4 import BeautifulSoup
import pandas as pd

def getOneTableData(url: str, class_of_table: str) -> pd.DataFrame:
    # add User-Agent to header to pretend as browser visit, more detials can be found in FireBug plugin    
    # if we don't add the below, error message occurs. ERROR: urllib.error.HTTPError: HTTP Error 403: Forbidden
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    next_page  = requests.get(url, headers = headers )
    soup = BeautifulSoup(next_page.text, 'html.parser')
    table = soup.find('table', {'class': class_of_table})
    columns = [th.text.replace('\n', '') for th in table.find('tr').find_all('th')]

    trs = table.find_all('tr')[1:]
    rows = list()
    for tr in trs:
        rows.append([td.text.replace('\n', '').replace('\xa0', '') for td in tr.find_all('td')])

    df = pd.DataFrame(data=rows, columns=columns)
    return df

def getAllTableData(url: str, class_of_table: str)-> pd.DataFrame:
    page_index = 0
    pass


def getAmountOfMovie(url: str,class_of_table: str,method = 'binary search')-> int:
    pass
def checkAccessibility(url: str,class_of_table: str):
    try:
        df = getOneTableData(url,class_of_table)
        print('Can find movie table')
        return True
    except:
        print('Cannot find movie table')
        return False
# to search url information for further information
def searchURL(url:str):
    # url as a domain

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    try:
        req  = requests.get(url,headers = headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        url_info = soup.find_all('a', href=True)
        return url_info
    except:
        print('Unable to request URL: ' + url)

# to get url tag by specific type of information
def getURLTag(url: str, attribute: str): # e.g. attribute =  'href' 
    url_info = searchURL(url)
    info_array = []

    index = 0 
    for a in url_info:
        info_array.extend([a[attribute]])
    return info_array

# to show url tag by specific type of information
def showURLTag(url:str, attribute: str): # e.g. attribute =  'href
    url_info = searchURL(url)
    for a in url_info:
        print ("Found the URL:", a[attribute])
if __name__ == '__main__':
    url = 'https://reelgood.com/movies'
    class_of_table = 'css-1179hly'
    df = getOneTableData(url, class_of_table)
    showURLTag(url,'href')
    print(df.shape)