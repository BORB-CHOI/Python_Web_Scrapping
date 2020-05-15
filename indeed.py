import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/jobs?q=python&limit={LIMIT}"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div",  class_="pagination")

    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        # // link.find("span").string하지 않아도 bs에서 알아서 찾아줌
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


def extract_job(job_html):
    title = job_html.find("h2", class_="title").find("a")["title"]
    company = job_html.find("span", class_="company")
    if company:
        company_anchor = company.find("a")
        if company_anchor is not None:
            company = str(company_anchor.string)
        else:
            company = str(company.string)
    else:
        compnay = None
    company = company.strip()
    location = job_html.find("div", class_="recJobLoc")["data-rc-loc"]
    job_id = job_html["data-jk"]
    return {'title': title, 'company': company, 'location': location, "link": f"https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?jk={job_id}"}


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping page {page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", class_="jobsearch-SerpJobCard")
    for result in results:
        job = extract_job(result)
        jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
