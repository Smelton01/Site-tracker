from requests import get
from bs4 import BeautifulSoup as bs
import json
from email_app import send_email
import time
from random import randint
from database import *
from datetime import datetime
import os

url = "https://www.fukuoka-now.com/en/classified/archive/?category=156"
database = r"database/database.db"
footer = "These email updates are provided by Simon J. View the source code at https://github.com/Smelton01/Site_tracker \nTo unsubcribe please follow this link https://github.com/Smelton01/Site_tracker"


def main():    
    # print("actually running, I think")
    # create connection to SQLite database
    conn = create_connection(database)
    create_table(conn)

    log = get_posts(url)
    conn = create_connection(database)
    for post, details in log.items():
        database_queries(conn, post, details)
        # TODO remove for production 
        # return
    print("Checked for updates, resting for 15 minutes...")

def database_queries(conn, post, details):
    """
    Check database for post and send email, update database if not exists
    :param conn: Connection to the SQLite database
    :param log: details of the posts
    :return:  None
    """
    with conn:
        res = check_post(conn, details["title"], details["date"])
        if res:
            # post already handled
            print("post already handled")
            return
        
        else:
            # send email notification
            email_content = f"Dear user,\n {details['text']} \nLink to original post: {details['src']} \nPosted by: {details['posted_by']} \nDate: {details['date']}\n\n{'*'*40}\n{footer}"
            
            print(email_content)
            # recipients = get_users(conn)
            # print(recipients)
            status = send_email(email_content, SUBJECT = "[FUKNOW] " + post, TO=["b4ck10up@gmail.com"])
            print(status)
            if status:
                # add seen post to database
                post_details = (post, details["text"], details["posted_by"], details["date"])
                create_post(conn, post_details)
            return

def get_posts(url):
    """
    Scrape provided url to return post data
    :param url: url to Fukuoka Now classifieds page
    :return: details of posts available, keyed by title 
    """
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
        # log[title] = "Yo Dude,\n" + txt + "\n" + det_url[i] + "\n" + posted[i].text.strip()
        *date, posted_by = posted[i].text.strip().split()
        date = " ".join(date[2:-1])
        # print(date)
        # date = datetime #.strptime(date, "%b. %d, %Y, %H:%M")
        log[title] = {"title": title, "text": txt, "src": det_url[i], "date": date, "posted_by": posted_by}
        # .strftime("%b. %d, %Y, %H:%M")

    return log


if __name__ == "__main__":
    main()
