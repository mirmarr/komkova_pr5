from bs4 import BeautifulSoup
import requests
import time
import os


allHeaders = {
    "Referer": "https://pikabu.ru/",
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
    С помощью функции скачиваем и сохраняем все изображения найденный в посте 
    """
    postCont = post.find("div", class_="story__content-wrapper")
    if(postCont != None):
      postCont = postCont.find("img")
    if(postCont != None):
      img_link_list = [postCont.get("data-src")]
      img = requests.get(img_link_list[0], headers = allHeaders, verify=False)
      if (img_link_list[0])[-3:] == "gif":
          with open(f"{adress}-{i}_s-{post_saved_times(post)}_t-{taglist_in_post(post)}.gif", 'wb') as f:
              f.write(img.content)
      elif (img_link_list[0])[-3:] == "jpg":
          with open(f"{adress}-{i}_s-{post_saved_times(post)}_t-{taglist_in_post(post)}.jpg", 'wb') as f:
              f.write(img.content)
      elif (img_link_list[0])[-3:] == "png":
          with open(f"{adress}-{i}_s-{post_saved_times(post)}_t-{taglist_in_post(post)}.png", 'wb') as f:
              f.write(img.content)
      elif (img_link_list[0])[-3:] == "ebm":
          with open(f"{adress}-{i}_s-{post_saved_times(post)}_t-{taglist_in_post(post)}.webm", 'wb') as f:
              f.write(img.content)
      else:
          with open(f"{adress}-{i}_s-{post_saved_times(post)}_t-{taglist_in_post(post)}.jpg", 'wb') as f:
              f.write(img.content)

def post_name(post):
  """
  С помощью функции получаем имя поста
  P.S. данная функция должна была участвовать в создании имени фотографии,
  но, т.к. иногда имя оказывается слишком длинным, оно не помещается в название файла 
  """

  post_name = post.find("h2",class_ = "story__title")
  post_name = post_name.find("a")
  return post_name.text

def post_saved_times(post):
  """
С помощью функции получаем количество сохранений людьми данного поста
  """

  times_saved = post.find("div",class_="story__content-wrapper")
  times_saved = times_saved.find("div",class_ = "story__footer")
  times_saved = times_saved.find("div",class_="story__save")
  if times_saved!=None:
    saved = [times_saved.get("aria-label")]
    if saved != None:
      saved[0] = re.sub("[^0-9]", "", saved[0])
      return saved[0]
  return 0

def taglist_in_post(post):
    """
    С помощью данной функции получаем массив тегов к данному посту
    """

    taglist = post.find("div",class_="story__tags")
    taglist = taglist.find_all("a")
    for i in range(len(taglist)):
      taglist[i] = [taglist[i].get("data-tag")]
      taglist[i][0].translate({ord(j): None for j in "[']"})
    return taglist

def find_posts(page):
    """
    С помощью данной функции находим все посты на странице
    """
    posts = page.find_all("div", class_ = "story__main")
    return posts

def get_title(url):
    page = get_page(url)
    return (page.find("title")).text

def find_count_pages(res):
    """
    С помощью данной функции получам количество страниц с изображениями
    """
    pages = res.find_all("div", class_ = "story-image__content ")
    return len(pages)
