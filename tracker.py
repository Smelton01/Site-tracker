from requests import get
from bs4 import BeautifulSoup as bs
import json
from email_app import send_email
import time
from random import randint

url = "https://www.fukuoka-now.com/en/classified/archive/?category=156"

def main():
    while True:
        response = get(url)
        page = bs(response.text, "html.parser")
        posts = page.find("div", class_="section_post_block02")
        posted = posts.find_all("div", class_="posted")
        posts = posts.find_all("div", class_="classifiedMain")

        det_url = [post.find("a").get("href") for post in posts]

        titles = []
        # get the title of the post
        for post in posts:
            titles.append(post.find("h3").text)

        log = {}
        # get the full text of the post
        for i, title in enumerate(titles):
            resp = get(det_url[i])
            pg = bs(resp.text, "html.parser")
            txt = pg.find("div", class_="entry").text
            log[title] = "Yo Dude,\n" + txt + "\n" + det_url[i] + "\n" + posted[i].text.strip()

        try:
            # check the posts already seen
            with open("log.json", "r", encoding="utf-8") as fp:
                read = json.load(fp)
        except Exception as i:
            print("Error: " + i)
            read = {}
        with open("log.json", "w", encoding="utf-8") as fp:
            for item in log.keys():
                if item not in list(read.keys()):
                    # Notify me by email and record in the log file if new post is found
                    status = send_email(log[item], SUBJECT = item)
                    read[item] = log[item]
                    print(status)
            # edit log file for debugging purposes
            # log.pop(list(log.keys())[randint(0, len(log)-1)])
            json.dump(log, fp, indent=True, sort_keys=4, ensure_ascii=False)
        print("Checked for updates, resting for 8.05hours (nice)...")
        time.sleep(69*420/2) #run every ~4 hours

if __name__ == "__main__":
    main()

