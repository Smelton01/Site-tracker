from requests import get
from bs4 import BeautifulSoup as bs
from .email_app import send_email
from .database import *
import psycopg2
import os
import logging

url = "https://www.fukuoka-now.com/en/classified/archive/?category=156"
footer = "These email updates are provided by Simon J. View the source code at https://github.com/Smelton01/Site_tracker \nTo unsubcribe please follow this link https://fuknowclass.herokuapp.com/"


def scrape_page():
    """
    Scrape URL for new posts and send email updates to users
    """
    # create connection to PostgreSQL database
    conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode='require')

    # create database table
    create_table(conn)

    # get posts from url
    posts = get_posts(url)
    if not posts:
        return False

    for post, details in posts.items():
        send_updates(conn, post, details)


def send_updates(conn, post, details):
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
            return

        # draft email notification
        email_content = f"{details['text']} \nLink to original post: {details['src']} \nPosted by: {details['posted_by']} \nDate: {details['date']}\n\n{'*'*40}\n{footer}"

        recipients = get_users(conn)

        # try sending email to registered users
        status = send_email(
            email_content, subject="[FUKNOW] " + post, recipients=recipients)

        if status:
            # add seen post to database
            post_details = (post, details["text"],
                            details["posted_by"], details["date"])
            create_post(conn, post_details)
        else:
            logging.error("Failed to send email")
        return


def get_posts(url):
    """
    Scrape provided url to return post data
    :param url: url to Fukuoka Now classifieds page
    :return: details of posts available, keyed by title 
    """
    try:
        response = get(url)
    except Exception as e:
        logging.critical("failed to get: ", e)
        return None
    page = bs(response.text, "html.parser")
    posts = page.find("div", class_="section_post_block02")
    posted = posts.find_all("div", class_="posted")
    posts = posts.find_all("div", class_="classifiedMain")
    det_url = [post.find("a").get("href") for post in posts]
    titles = []
    # get the title of the post
    for post in posts:
        titles.append(post.find("h3").text)
    all_posts = {}
    # get the full text of the post
    for i, title in enumerate(titles):
        resp = get(det_url[i])
        pg = bs(resp.text, "html.parser")
        txt = pg.find("div", class_="entry").text

        *date, posted_by = posted[i].text.strip().split()
        date = " ".join(date[2:-1])
        all_posts[title] = {"title": title, "text": txt,
                            "src": det_url[i], "date": date, "posted_by": posted_by}

    return all_posts
