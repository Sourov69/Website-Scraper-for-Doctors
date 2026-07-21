import time
import random
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import pandas as pd
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from db import Database

load_dotenv()

# Connect with Database
db = Database(
    host="localhost",
    user = "root",
    password = os.getenv("DATABASE_PASSWORD"),
    database = "doctor_scraper"
)

# Extract single page html data
def extract_therapist_info(html_page):
    soup = BeautifulSoup(html_page, "html.parser")
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

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://care.headway.co/search/california?address=San+Diego%2C+CA+92108%2C+USA&forChild=ADULTS&frontEndCarrierId=61&issues=lgbtq&lat=32.7742488&lon=-117.1411815&medium=VIRTUAL&state=CALIFORNIA&typeOfCare=Talk+Therapy&availabilities=EVENING&modalityCareTypes=INDIVIDUAL_THERAPY")
    page.wait_for_timeout(3000)
    
    for _ in range(1, random.randint(13, 15)):
        scrool_amount = random.randint(800, 1000)
        page.mouse.wheel(0, scrool_amount)
        time.sleep(random.uniform(0.5, 2))
    
    ## Storing first page in database
    html_page = page.content()
    columns_value_list = extract_therapist_info(html_page)
    rows = [tuple(row.values()) for row  in columns_value_list]
    db.inser_many_rows(rows)

    ## Storing first page in csv
    df = pd.DataFrame(columns_value_list)
    df.to_csv("therapist_info.csv", index=False)

    ## Storing first page in excel
    df.to_excel("therapist_info.xlsx", sheet_name="therapist", index=False)


    while True:
        try:
            next_page = page.locator("nav.hlx-pagination ul > li:last-child")
            if not next_page.is_visible():
                print("No next page")
                break
            next_page.click()

        except Exception as e:
            print(f"Pagination stopped : {e}")
            break
        page.wait_for_timeout(300)
        for _ in range(1, random.randint(12, 15)):
            scrool_amount = random.randint(800, 1000)
            page.mouse.wheel(0, scrool_amount)
            time.sleep(random.uniform(0.5, 2))
        html_page = page.content()
        
        print("therapist : ", len(extract_therapist_info(html_page)))

        # Storing scraped data into database (insert)
        columns_value_list = extract_therapist_info(html_page)
        rows = [tuple(row.values()) for row  in columns_value_list]
        db.inser_many_rows(rows)

        # Storing scraped data into csv (increment storing)
        df = pd.DataFrame(columns_value_list)
        df.to_csv("therapist_info.csv", mode="a", header=False, index=False)
        
        # Storing Scraped data into excel (increment storing)
        workbook = load_workbook("therapist_info.xlsx")
        sheet = workbook["therapist"]
        for row in rows:
            sheet.append(row)
        workbook.save("therapist_info.xlsx")
        workbook.close()

    page.wait_for_timeout(3000)
  
    page.close()

# Closing database connection
db.close_connection()
