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
    columns = columns[1:] # index 0 is an empty element
    trs = table.find_all('tr')[1:]
    rows = list()
    for tr in trs:
        rows.append([td.text.replace('\n', '').replace('\xa0', '') for td in tr.find_all('td')][1:]) # index 0 is an empty element

    df = pd.DataFrame(data=rows, columns=columns)
    return df

# to get all data from url 
def getAllTableData(url: str, class_of_table: str)-> pd.DataFrame:

    start_offset = 0
    df = pd.DataFrame() # the dataframe stored all data
    print("Loading the table one by one")
    while checkAccessibility(getOffsetURL(url,start_offset),class_of_table): # check the table can be accessed or not first
        target_url = getOffsetURL(url,start_offset)
        sub_df = getOneTableData(target_url,class_of_table) # table for only one data frame
        df = pd.concat([df,sub_df],ignore_index = True)
        start_offset += sub_df.shape[0]
    print("End loading the table")
    return df

# to write csv file from data frame
def writeCSV(dataframe: pd.DataFrame, file_path : str,index: bool, header : bool ):
    try:
        dataframe.to_csv(file_path,index = index , header = header)
        print("Write CSV file successfully: " + file_path )
    except:
        print("Cannot write CSV file from pandas Dataframe. Please Check the dataframe or path correct or not")

# to get how many rows in url
def getAmountOfMovie(url: str,class_of_table: str, method = 'binary search') -> int:
    if method == 'binary search':

        print("=======Binary Search Start=======")
        index = binarySearchAmount(url,class_of_table,0,67150)
        print("=======Binary Search End=======")
        return index

# by using binary search method, how many rows in url can be found
def binarySearchAmount(url: str,class_of_table: str,low: int, high: int) -> int:

    # search Accessibility
    # if Accessibility at i and i + 1 th item == [True, False], index i is the last item of rows
    target = [True,False]
    
    if high >= low:

        mid = (high + low) // 2 
        high_access = checkAccessibility(getOffsetURL(url,high),class_of_table)
        low_access = checkAccessibility(getOffsetURL(url,low),class_of_table)
        mid_and_plus1_access = [checkAccessibility(getOffsetURL(url,mid),class_of_table), checkAccessibility(getOffsetURL(url,mid + 1),class_of_table)]

        if mid_and_plus1_access == target:
            return mid
        elif mid_and_plus1_access == [True,True] and low_access != high_access: #if low_access == high_access, the function will recursively run infinitv
            print("Change: let mid become low")
            return binarySearchAmount(url,class_of_table,mid,high)
        elif mid_and_plus1_access == [False,False] and low_access != high_access:
            print("Change: let mid become high")
            return binarySearchAmount(url,class_of_table,low,mid)
        else:
            print('Error: cannot find the amount of the table in URL between ' + str(low) + ' and ' + str(high))
            return -1 
    else:
        print('Error: parameter "high" should be higher than "low"')
        return -1

def checkAccessibility(url: str,class_of_table: str):
    try:
        df = getOneTableData(url,class_of_table)
        print('Can find movie table :' + url)
        return True
    except:
        print('Cannot find movie table: ' + url)
        return False
        
# to get offset URL
def getOffsetURL(url: str, number: int):

    return url + '?offset=' + str(number)

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
    url = 'https://reelgood.com/curated/trending-picks'
    class_of_table = 'css-1179hly'
    showURLTag(url,'href')
    df = getAllTableData(url,class_of_table)
    file_path = 'C:\\Users\\01723899\\Desktop\\webscrapping\\movsys\\' + 'trending-picks.csv'
    writeCSV(df,file_path,index = False, header = True)