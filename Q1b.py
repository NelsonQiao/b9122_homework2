import requests
from bs4 import BeautifulSoup
import urllib.parse
from urllib.parse import urljoin

def extract_press_release(url,Question_Number, Number_of_Press_Release):
    response = requests.get(url)
    html_content = response.text
    f = open("{}_{}.txt".format(Question_Number,Number_of_Press_Release), "w", encoding= 'utf-8')
    f.write(html_content)
    f.close()
    print("HTML content for Question 1 part {}, article {} is saved.".format(Question_Number,Number_of_Press_Release))

Question_Number = "b"

seed_url = "https://www.europarl.europa.eu/news/en/press-room"
target_word = "crisis"

url_seen = []
url_needed = []
m=0
page_num = 0

while len(url_needed)<10:
    print("Now we are moving to page No. {}".format(page_num))
    page_num+=1
    PRESS_URL = f"{seed_url}/page/{page_num}"
    url_seen.append(PRESS_URL)
    #Get all the links from this page
    LINKS = []
    ALL_CONTENT = requests.get(PRESS_URL).text
    SOUP = BeautifulSoup(ALL_CONTENT,'html.parser')
    TEXT = SOUP.find_all("div", class_ = "ep_title")
    for t in TEXT:
        URL_DETECTED = t.find_all("a", href = True)
        for h in URL_DETECTED:
            l = h['href']
            LINKS.append(l)

    for browse_url in LINKS:
        if seed_url in browse_url:
            try:

                m += 1
                print(m)
                print("Currently found {}".format(len(url_needed)))
                print("Try to search web {}".format(browse_url))
                result = requests.get(browse_url).content
                soup = BeautifulSoup(result, 'html.parser')
                #check whethwe it is in the press room
                press_room_tag = soup.find_all("span", class_ = "ep_name", string = "Press Releases")

                if len(press_room_tag)==1 and browse_url not in url_seen:
                    # check whether this url is a plenary session
                    cate_tag = soup.find_all('span', class_="ep_name", string='Plenary session')
                    if len(cate_tag) > 0:
                        main_content_tag = soup.find_all('article', id = "website-body", role = "main")
                        for i in main_content_tag:
                            main_content = i.get_text().lower()
                            # check whether it contains word 'crisis'
                            if target_word in main_content and browse_url not in url_needed:
                                url_needed.append(browse_url)
                                print("This is a {} web that contains word {}.".format("Plenary Session", target_word))
                                extract_press_release(browse_url,Question_Number,len(url_needed))
                                break
                            else:
                                print("This {} url does not contain word {}.".format("Plenary Session", target_word))
                    else:
                        print("This is not a Plenary Session")


            except:
                continue

print("This is the list of {} web containing word {}, there are {} urls in total.".format("Plenary Session",target_word,len(url_needed)))
print(url_needed)
