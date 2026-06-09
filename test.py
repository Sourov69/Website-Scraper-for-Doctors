import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright


all_therapist_info_list = []

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

            "therapist_url" : urljoin(base_url, href),

            "Specialty" : [j.get_text() for j  in i.select(".hlx-badge-content")][:-3],

            "style" : [j.get_text() for j  in i.select(".hlx-badge-content")][-3:],

            
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
    

    # while True:
    for i in range(1, 3):
        next_page = page.locator("nav.hlx-pagination ul > li:last-child")
        if not next_page.is_visible():
            break

        next_page.click()
        page.wait_for_timeout(300)
        for _ in range(1, random.randint(12, 15)):
            scrool_amount = random.randint(800, 1000)
            page.mouse.wheel(0, scrool_amount)
            time.sleep(random.uniform(0.5, 2))
        html_page = page.content()
        
        print("therapist : ", len(extract_therapist_info(html_page)))
        all_therapist_info_list.extend(extract_therapist_info(html_page))

    page.wait_for_timeout(3000)
  
    page.wait_for_timeout(2500)
    page.close()

df = pd.DataFrame(all_therapist_info_list)

df.to_excel("all_therapist_info_list_sample_table.xlsx", sheet_name="therapist_info", index=False)