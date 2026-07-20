from db import Database
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import pandas as pd
from bs4 import BeautifulSoup

load_dotenv()

db = Database(
    host="localhost",
    user = "root",
    password = os.getenv("DATABASE_PASSWORD"),
    database = "doctor_scraper"
)

db.check_connection()

with open("C:/Users/ASUS/OneDrive/Desktop/Web Scraping/05_Website Scraper for Doctors/page.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
soup

therapist_list  =soup.select_one('div[data-testid="best-match-cards"]')
therapist_list

from urllib.parse import urljoin
def extract_therapist_info(html_page):
    soup = BeautifulSoup(html, "html.parser")
    therapist_list  =soup.select_one('div[data-testid="best-match-cards"]')
    base_url = "https://care.headway.co"

    therapist_info_list = []
    for i in therapist_list:
        href = i.select_one("a.block.h-full.w-full").get("href")
        full_url = urljoin(base_url, href)
        therapist_info_list.append({
            "therapist_name" : i.select_one("h4").get_text(),

            "sub_title" : i.select_one(".hlx-typography-content-body").get_text(separator=", "),

            "Bio"  : i.find(class_="[&_*]:!font-normal [&_*]:not-italic [&_*]:no-underline line-clamp-3").get_text(separator=", "),

            "therapist_url" : str(urljoin(base_url, href)),

            "Specialty" : str([j.get_text() for j  in i.select(".hlx-badge-content")][:-3]),

            "style" : str([j.get_text() for j  in i.select(".hlx-badge-content")][-3:]),

            
        })
    return therapist_info_list

temp_list = extract_therapist_info(html)

rows = [tuple(row.values()) for row  in temp_list]

## Single row data inserttion
# db.insert_single_row(str(rows[0][0]), str(rows[0][1]), str(rows[0][2]), str(rows[0][3]), str(rows[0][4]), str(rows[0][5]))

## Multiple row data insrertion
db.inser_many_rows(rows)
# # print(rows)
# for i in range(len(rows[0])):
#     print(i, " : ", type(str(rows[0][i])),rows[0][i] )
