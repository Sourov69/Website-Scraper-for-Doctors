# Extract and Analyze **Doctors** listing data

## This was a client project:

### Client requirements was

I’m looking for a freelancer to extract and analyze listing data from the following website with filters: 

https://care.headway.co/search/california?address=San+Diego%2C+CA+92108%2C+USA&forChild=ADULTS&frontEndCarrierId=61&issues=lgbtq&lat=32.7742488&lon=-117.1411815&medium=VIRTUAL&state=CALIFORNIA&typeOfCare=Talk+Therapy&availabilities=EVENING&modalityCareTypes=INDIVIDUAL_THERAPY

**Additional criteria would include:**
- 1. The profile must include the word(s) ‘neurodivergent’ or ‘neurodivergence’. 
- 2. Must verify that they have an appointment available after 6pm at some point over the next 2 weeks. 
- 3. Must accept ‘Blue Shield of California’ insurance. For all of the results I need all fields extracted as possible into XLSX.

--- 

## Deliverables

•	Collect/enrich all of the information you can such as (you can tell me what is & is not possible):
•	Company Name
•	Brief Description
•	Categories / Keywords
•	Contact Name
•	Contact Title
•	Type (Buyer/Broker/D2C)
•	Website
•	Email
•	Phone
•	Estimated Size (Employees or revenue)
•	Source
•	~100 promising prospects


## My approaches

> Extract all Doctors list and their profile url from all pages(1-66 ).
> Store them in an excel file
> Browse each Doctors profile url (stored in excel) to extract required information

## Tools i used :
 - **Python Plywright** : Browser Automation to  interect and navigate with the website
 - **BeautifuSoup** : Parsing messy html to extract data
 - **Pandas** : Cleaning data (text, url, lists) & Transformation (Dictionaries, DataFrames, tables)
 - **Excel** : saving & storing clean row data



