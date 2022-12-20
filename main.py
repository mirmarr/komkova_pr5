from bs4 import BeautifulSoup
import requests
import time
import os
import datetime

import get_files as gf



def main():
    link = "https://pikabu.ru/best"

    if os.path.exists("Images") == True:
        pass
    else:   
        os.mkdir("Images")

    fileName = ((sj.get_title(link)).split("/")[0]).strip()
    
    if os.path.exists("Images/"+fileName) == True:
        pass
    else:   
        os.mkdir("Images/"+fileName)

    pageCount = gf.find_count_pages(get_page(link))

    for i in range(1, pageCount):
        targetLink = link
        targetPage = gf.get_page(targetLink)
        posts = gf.find_posts(targetPage)

        j = 0
        for post in posts:
            gj.img_in_post(post, adress = ("Images\\"+fileName+"\\"+(str(i)+"-"+str(j))))
            j += 1



if __name__ == '__main__':
    main()
