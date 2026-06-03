import time
import random
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://care.headway.co/search/california?address=San+Diego%2C+CA+92108%2C+USA&forChild=ADULTS&frontEndCarrierId=61&issues=lgbtq&lat=32.7742488&lon=-117.1411815&medium=VIRTUAL&state=CALIFORNIA&typeOfCare=Talk+Therapy&availabilities=EVENING&modalityCareTypes=INDIVIDUAL_THERAPY")
    page.wait_for_timeout(3000)
    
    for _ in range(1, random.randint(7, 10)):
        scrool_amount = random.randint(300, 600)
        page.mouse.wheel(0, scrool_amount)
        time.sleep(random.uniform(0.5, 2))

    therapist_list = page.locator('div[data-testid="best-match-cards"] > div')
    print(therapist_list.count())

   
    # with context.expect_page() as therapist_profile:
    #     therapist_list.nth(1).click()
    # therapist_profile_page = therapist_profile.value
    # therapist_profile_page.wait_for_timeout(3000)
 
    # for i in range(1, 3):
    #     therapist_profile_page.mouse.wheel(0, 400)
    #     therapist_profile_page.wait_for_timeout(1500)
    # therapist_profile_page.close()

    therapist_list_html_page1 = page.content()
    with open("page.html", "w", encoding="utf-8") as f:
        f.write(therapist_list_html_page1)

    page.wait_for_timeout(2500)
    page.close()