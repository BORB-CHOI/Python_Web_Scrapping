import requests
from bs4 import BeautifulSoup

URL = "https://stackoverflow.com/jobs?q=python"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", class_="s-pagination").find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(job_html):
    title = job_html.find("div", class_="grid--cell fl1").h2.a["title"]
    company, location = job_html.find(
        "div", class_="fl1").h3.find_all("span", recursive=False)
    company = company.get_text(strip=True).strip("\r")
    location = location.get_text(strip=True).strip("-")
    job_id = job_html['data-jobid']
    return {'title': title, 'company': company, 'location': location, 'link': f"https://stackoverflow.com/jobs/{job_id}"}


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping page {page}")
        result = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", class_="-job")
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
