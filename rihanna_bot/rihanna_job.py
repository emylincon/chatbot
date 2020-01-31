import requests
from bs4 import BeautifulSoup
import config


def selector(message):
    if message[:len("job search average salary for ")] == "job search average salary for ":
        query = message[len("job search average salary for "):].split(' in ')
        job = query[0].strip()
        place = query[1].strip()
        return average_salary(job,place)
    elif message[:len("job search min salary for ")] == "job search min salary for ":
        query = message[len("job search min salary for "):].split(' in ')
        job = query[0].strip()
        place = query[1].strip()
        return min_salary(job, place)
    elif message[:len("job search max salary for ")] == "job search max salary for ":
        query = message[len("job search max salary for "):].split(' in ')
        job = query[0].strip()
        place = query[1].strip()
        return max_salary(job, place)
    else:
        return "Rihanna is not in the mood to answer this job search related question"


def go_to(url):
    page = requests.get(url, headers=config.header)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def search_page(job, where):
    url = f"https://www.indeed.co.uk/jobs?q={job}&l={where}"
    page = requests.get(url, headers=config.header)
    soup = BeautifulSoup(page.content, 'html.parser')
    # items = soup.find_all("div", {"class": "jobsearch-jobDescriptionText"})
    items = soup.find_all("div", {"class": "jobsearch-SerpJobCard unifiedRow row result"})

    return items


def search_job(job, where):
    items = search_page(job, where)
    min_ = []
    max_ = []

    for job_post in items:
        try:
            salary_raw = job_post.find("span", {"class": "salaryText"}).get_text()

            if '-' in salary_raw:
                salary_raw = salary_raw.split('-')
                con = salary_raw[1].split()[-1].strip()
                if con == 'year':
                    multi = 1
                elif con == 'month':
                    multi = 12
                else:
                    multi = 5*4*12
                min_.append(float(salary_raw[0].strip()[1:].replace(',', ''))*multi)
                max_.append(float(salary_raw[1].split()[0].strip()[1:].replace(',', ''))*multi)
        except AttributeError:
            pass
    
    return min_, max_


def add_format(query):
    query = str(round(query, 2))
    raw = query.split('.')
    points = raw[1] if len(raw[1]) == 2 else raw[1]+'0'
    int_ = format(int(raw[0]), ',d')

    return f'{int_}.{points}'


def average_salary(job, place):
    min_, max_ = search_job(job,place)
    if len(min_) == 0:
        return f"Rihanna could not find {job}"
    else:
        avg_min = add_format(sum(min_)/len(min_))
        avg_max = add_format(sum(max_)/len(max_))
        display = f"The average annual salary for {job} in {place.capitalize()} ranges from £{avg_min} to £{avg_max}"
        reply = {'display': display, 'say': display}
        return reply


def min_salary(job, place):
    # add min salary and job link
    items = search_page(job, place)
    min_ = {}    # {link: salary}
    min_comp = {}    # {link: company}
    for job_post in items:
        try:
            salary_raw = job_post.find("span", {"class": "salaryText"}).get_text()
            try:

                company = job_post.find("a", {"data-tn-element": "companyName"}).get_text()
            except AttributeError:
                company = job_post.find("span", {"class": "company"}).get_text()
                #company = job_post.find("a", {"class": "turnstileLink"}).get_text()
            link = job_post.find("a", {"class": "jobtitle turnstileLink"}).get('href')
            if '-' in salary_raw:
                salary_raw = salary_raw.split('-')
                con = salary_raw[1].split()[-1].strip()
                if con == 'year':
                    multi = 1
                elif con == 'month':
                    multi = 12
                else:
                    multi = 5 * 4 * 12
                min_[link] = float(salary_raw[0].strip()[1:].replace(',', '')) * multi
                min_comp[link] = company

        except AttributeError:
            pass
    if len(min_) > 0:
        min_job = min(min_, key=min_.get)
        h = '\n'
        reply = {'display': f'The Minimum Salary for {job} in {place} from indeed website is £{add_format(min_[min_job])} Annually. '
                            f'<br>This Job is offered by {min_comp[min_job].replace(h, "")}. '
                            f'<a href="https://www.indeed.co.uk{min_job}" target="_blank">view</a>',
                 'say': f'The Minimum Salary for {job} in {place} from indeed website is £{add_format(min_[min_job])} Annually. '
                            f'This Job is offered by {min_comp[min_job].replace(h, "")}. '
                            f'link is provided'}
        return reply
    else:
        return f"Rihanna could not find {job}"


def max_salary(job, place):
    items = search_page(job, place)
    max_ = {}    # {link: salary}
    max_comp = {}    # {link: company}
    for job_post in items:
        try:
            salary_raw = job_post.find("span", {"class": "salaryText"}).get_text()
            try:

                company = job_post.find("a", {"data-tn-element": "companyName"}).get_text()
            except AttributeError:
                company = job_post.find("span", {"class": "company"}).get_text()
                #company = job_post.find("a", {"class": "turnstileLink"}).get_text()
            link = job_post.find("a", {"class": "jobtitle turnstileLink"}).get('href')
            if '-' in salary_raw:
                salary_raw = salary_raw.split('-')
                con = salary_raw[1].split()[-1].strip()
                if con == 'year':
                    multi = 1
                elif con == 'month':
                    multi = 12
                else:
                    multi = 5 * 4 * 12
                max_[link] = float(salary_raw[1].split()[0].strip()[1:].replace(',', ''))*multi
                max_comp[link] = company

        except AttributeError:
            pass
    if len(max_) > 0:
        min_job = max(max_, key=max_.get)
        h = '\n'
        reply = {'display': f'The Maximum Salary for {job} in {place} from indeed website is £{add_format(max_[min_job])} Annually. '
                            f'<br>This Job is offered by {max_comp[min_job].replace(h, "")}. '
                            f'<a href="https://www.indeed.co.uk{min_job}" target="_blank">view</a>',
                 'say': f'The Maximum Salary for {job} in {place} from indeed website is £{add_format(max_[min_job])} Annually. '
                            f'This Job is offered by {max_comp[min_job].replace(h, "")}. '
                            f'link is provided'}
        return reply
    else:
        return f"Rihanna could not find {job}"


def key_skills(job, place):  # TODO
    # find job key skills
    pass


def salary_graph(job, place):  # TODO
    # return average salary graph of top cities in uk
    pass



#print(selector("job search min salary for devops in london"))


































































