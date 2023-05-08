import requests
from bs4 import BeautifulSoup
import time
import json

Headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", 
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0"
    }

Categories_IGN = {
    "game": "",
    "movie": "",
    "tv": "",  
    "comics": "",
    "tech": ""
    }

def get_page():

    for category in Categories_IGN:

        Url = f"https://me.ign.com/en/article/review/?keyword__type={category}"

        response = requests.get(Url, headers=Headers)
        soup = BeautifulSoup(response.text, "lxml")

        total_page= soup.find("section", class_="broll wrap").get("data-total")
        Categories_IGN[category] = total_page

def get_cards():

    for category in Categories_IGN:

        print(f"\nINFO: Scrapping category: {category}\n")

        list_card = []

        for page in range(1, int(Categories_IGN[category])+1): 

            print(f"\nINFO: Going to page: {page}/{Categories_IGN[category]} of {category}\n")
            time.sleep(2)

            category_url = f"https://me.ign.com/en/article/review/?keyword__type={category}&page={page}&ist=broll"

            request = requests.get(category_url, headers=Headers)
            soup = BeautifulSoup(request.text, "lxml")

            data = soup.find_all("article", class_="article REVIEW")

            for review in data:
                
                review_date = review.find("time").get("datetime").split("T")[0]
                review_name = review.find("h3").text.strip()
                review_url = review.find("a").get("href")
                review_desc = review.find("p").text.strip()
                    
                list_card.append({
                    "review_name": review_name,
                    "review_date": review_date,
                    "review_url": review_url,
                    "review_desc": review_desc
                })
        Categories_IGN[category] = list_card
    
    with open("/home/alena/Desktop/Coding/ScrappingPrac/IGN_Reviews.json", "w") as file:
        json.dump(Categories_IGN, file, indent=4, ensure_ascii=False)
          
def main():
    get_page()
    get_cards()

main()


    



