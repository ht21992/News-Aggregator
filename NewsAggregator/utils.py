import httpx
from bs4 import BeautifulSoup
import re


def get_vox_headlines() -> list:
    """
    this function gets all the headlines from the Vox

    Returns:
        list: a list of dictionary will be returned.
              each inner dict contains four elements [{ 'title': refers to the title,
                                                        'date_and_author': refers to the author and date ,
                                                        'image' : image link,
                                                        'link': news orginal link
                                                      }]
    """

    r = httpx.get("https://www.vox.com/world-politics")
    soup = BeautifulSoup(r.content, 'html.parser')
    headlines_html = soup.find_all("div", {"class": "c-compact-river__entry"})
    headlines_list = list()
    for headline in headlines_html:
        image_src = headline.select('img')[-1].attrs["src"]
        article_href = headline.select('a')[1].attrs["href"]
        headline_contents = headline.text.split('\n')
        content = [h.strip() for h in headline_contents if h.strip() != '']
        # extending  image src and article_href
        content.extend([image_src, article_href])
        headlines_list.append(content)

    headlines = [{'title':  re.sub('[^A-Za-z0-9]+', ' ', i[0]), 'date_and_author':f'{i[3]} {i[1]} {i[2]}',
                  'image':i[4], 'link':i[5]} for i in headlines_list]
    return headlines


def get_time_headlines() -> list:
    """
     this function gets all the headlines from the Vox

     Returns:
         list: a list of dictionary will be returned.
               each inner dict contains four elements [{ 'title': refers to the title,
                                                         'date_and_author': refers to the author and date ,
                                                         'image' : image link,
                                                         'link': news orginal link
                                                       }]
    """

    r = httpx.get("https://time.com/section/world/")

    soup = BeautifulSoup(r.content, 'html.parser')

    headlines_html = soup.find_all("div", {"class": "taxonomy-tout"})

    headlines_list = list()
    for headline in headlines_html:
        headline_contents = headline.text.split('\n')
        content = [h.strip() for h in headline_contents if h.strip() != '']
        image_src = headline.select('img')[-1].attrs["src"]
        href = 'https://time.com/' + headline.select('a')[0].attrs["href"]

        content.extend([image_src, href])  # appending image src
        headlines_list.append(content)
    headlines = [{'title':  re.sub('[^A-Za-z0-9]+', ' ', i[0]), 'date_and_author':i[2],
                  'image':i[3], 'link':i[4]} for i in headlines_list if len(i) == 5]
    return headlines


def get_npr_headlines():
    """
     this function gets all the headlines from the Vox

     Returns:
         list: a list of dictionary will be returned.
               each inner dict contains four elements [{ 'title': refers to the title,
                                                         'date_and_author': refers to the author and date ,
                                                         'image' : image link,
                                                         'link': news orginal link
                                                       }]
    """
    r = httpx.get("https://www.npr.org/sections/world/")

    soup = BeautifulSoup(r.content, 'html.parser')

    headlines_html = soup.find_all("article", {"class": "item has-image"})

    headlines_list = list()
    for headline in headlines_html:
        headline_contents = headline.text.split('\n')

        content = [h.strip() for h in headline_contents if h.strip() != '']
        if len(content) < 8:
            continue
        image_src = headline.select('img')[-1].attrs["src"]

        href = headline.select('a')[0].attrs["href"]

        content.extend([image_src, href])  # appending image src
        headlines_list.append(content)
    headlines = [{'title': re.sub('[^A-Za-z0-9]+', ' ', i[6]), 'date_and_author': i[7][:i[7].find('•')],
                  'image':i[8], 'link':i[9]} for i in headlines_list if len(i) >= 9]
    return headlines


WEBSITE_DICT = {"Vox": get_vox_headlines,
                "Time": get_time_headlines, 'NPR': get_npr_headlines}
