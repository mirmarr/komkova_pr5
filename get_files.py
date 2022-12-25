from bs4 import BeautifulSoup
import requests
import time
import os


allHeaders = {
    "Referer": "https://wallpaperscraft.ru/catalog/animals",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}


from traitlets.utils.descriptions import class_of
import re
def valid_link(link):
    """
    С помощью функции проверяем доступ к сайту.
    """
    try:
        url = requests.get(link, headers = allHeaders, verify=False)
    except:
        return False
    if url.status_code == 200:
        url.close()
        return True
    else:
        return url.status_code

def get_page(link):
    """
    С помощью функции получаем код страницы целиком.
    """
    if valid_link(link) == True:
        url = requests.get(link, headers = allHeaders, verify=False)
        page = BeautifulSoup(url.text, "lxml")
        url.close()
        return page
    else: 
        return valid_link(link)

def img_in_post(post, adress="Images"):
    """
    С помощью функции скачиваем и сохраняем все изображения 
    """
    postCont = post.find("span", class_="wallpapers__canvas")
    if(postCont != None):
      postCont = postCont.find("img")
    if(postCont != None):
      img_link_list = [postCont.get("src")]
      img = requests.get(img_link_list[0], headers = allHeaders, verify=False)
      if (img_link_list[0])[-3:] == "gif":
          with open(f"{adress} n-{post_name(post)} t-{taglist_in_post(post)}.gif", 'wb') as f:
              f.write(img.content)
      elif (img_link_list[0])[-3:] == "jpg":
          with open(f"{adress} n-{post_name(post)} t-{taglist_in_post(post)}.jpg", 'wb') as f:
              f.write(img.content)
      elif (img_link_list[0])[-3:] == "png":
          with open(f"{adress} n-{post_name(post)} t-{taglist_in_post(post)}.png", 'wb') as f:
              f.write(img.content)
      elif (img_link_list[0])[-3:] == "ebm":
          with open(f"{adress} n-{post_name(post)} t-{taglist_in_post(post)}.webm", 'wb') as f:
              f.write(img.content)
      else:
          with open(f"{adress} n-{post_name(post)} t-{taglist_in_post(post)}.jpg", 'wb') as f:
              f.write(img.content)

def post_name(post):
  """
  С помощью функции получаем разрешение 
  """

  post_name = post.find("span",class_ = "wallpapers__info")
  post_name = post_name.text
  return post_name

def post_saved_times(post):
  """
С помощью функции получаем количество скачиваний людьми 
  """

  times_saved = post.find("span",class_ = "wallpapers__info")
  times_saved = times_saved.find("span",class_="wallpapers__info-downloads")
  if times_saved!=None:
    saved = times_saved.text
    if saved != None:

      saved = re.sub("[^0-9]", "", saved)
      return saved[0]
  return 0

def taglist_in_post(post):
    """
    С помощью данной функции получаем имена 
    """

    taglist = post.find_all("span",class_="wallpapers__info")
    taglist = taglist[1].text
    return taglist

def find_posts(page):
    """
    С помощью данной функции находим все картинки на странице
    """
    posts = page.find_all("li", class_ = "wallpapers__item")
    return posts

def get_title(url):
    page = get_page(url)
    return (page.find("title")).text

def find_count_pages(res):
    """
    С помощью данной функции получам количество страниц с изображениями
    """
    pages = res.find_all("ul", class_ = "wallpapers__list ")
    return len(pages) + 1 
