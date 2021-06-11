# Site-tracker
A Flask based application designed to send email notifications when new posts are made to [Fukuoka-now](https://www.fukuoka-now.com/) classified section.

Designed for residents of Fukuoka looking to make early bids on items being sold on the site.

Deployed using Google's Compute Engine.

View running demo [here](http://smelton01.github.io/me)

## Requirements

Python 3

## Running

Set the following environment variables:
- FROM_ADDR - email address to send emails from
- PWD - password for the email 

```
git clone https://github.com/Smelton01/Site-tracker.git
cd Site-tracker
pip install -r requirements.py 
cd src
python app.py

view running app on http://localhost:5000
```
