import urllib.parse
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
#hello
def extract_press_release(url,Question_Number, Number_of_Press_Release):
    response = requests.get(url)
    html_content = response.text
    f = open("{}_{}.txt".format(Question_Number,Number_of_Press_Release), "w", encoding= 'utf-8')
    f.write(html_content)
    f.close()
    print("HTML content for Question 1 part {}, article {} is saved.".format(Question_Number,Number_of_Press_Release))

Question_Number = "a"

print("Hello， this is Nelson's HW2, Question 1, part a:)")

seed_url = "https://press.un.org/en"


target_url = "/en/press-release"
target_word = "crisis"
count = 0
url_seen = []
url_seen.append(seed_url)
url_needed = []
round = 0

for urls in url_seen:
    if len(url_needed) < 9:
        print("Current ROUND {} and FOUND {}".format(round,len(url_needed)))

        result = requests.get(urls).content

        soup = BeautifulSoup(result)

        links = soup.find_all("a", href = True)
        for i in links:

            child_url = urllib.parse.urljoin(seed_url,i['href'])
            if child_url not in url_seen and seed_url in child_url:
                url_seen.append(child_url)

                print("Try to get into " + child_url)
                try:
                    child_content = requests.get(child_url).content
                    child_content_links = BeautifulSoup(child_content).find_all("a", href = True)
                    for m in child_content_links:

                        press_check = urllib.parse.urljoin(seed_url,m['href'])
                        if seed_url in press_check and press_check not in url_seen:
                            round += 1
                            print(round)
                            print("Try to get into {}".format(press_check))
                            if m['href'] == target_url:
                                response = requests.get(child_url).content
                                soup = BeautifulSoup(response, 'html.parser')
                                main_content = soup.find_all('div', class_="field field--name-body field--type-text-with-summary field--label-hidden field__item")
                                for t in main_content:
                                    text_content = t.get_text()
                                if target_word in text_content and child_url not in url_needed:
                                    print("This is a url we need")
                                    url_needed.append(child_url)
                                    extract_press_release(child_url,Question_Number,len(url_needed))

                                else:
                                    print("This is a press release without 'crisis' word in it")
                            else:
                                print("This website is not a press release")

                except:
                    continue



print("These are the press release containing word {} {}".format('crisis',url_needed))
