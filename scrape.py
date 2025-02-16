import requests
from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

driver.get('https://apps.ualberta.ca/catalogue/course/cmput')
time.sleep(4)

def splitCourses(soup):
    '''
    Split course element into course name and description and appends them to a dictionary
    returns a dictionary
    - soup: html data
    '''

    courses = []
    desc = []

    pattern = re.compile(r'([A-Za-z]+)\s*(\d+)')    #   Regex pattern
    course_blocks = soup.find_all('div', class_='mb-3 pb-3 border-bottom')
    for div in course_blocks:
        a_tag = div.find('h2').find('a') if div.find('h2') else None    #   Check for matching tags
        if a_tag:
            course_code = a_tag.text.strip()
            match = pattern.match(course_code)

            if match:   #   Use regex code
                course_code = f"{match.group(1)} {match.group(2)}"
                courses.append(course_code)     #   Apppend course code

        p_tag = div.find('p')   #   Check for matching tags
        if p_tag:
            description = p_tag.text.strip()
            desc.append(description)    #   Append description
        else:   #   No description
            alert_div = div.find('div', class_='alert alert-warning')
            description = alert_div.text.strip() if alert_div else "No description avaliable"
            desc.append(description)

    courses_dict = dict(zip(courses, desc))     #   Convert to dictionary
    return courses_dict     #   Return

def extract_prequisites(description):
    '''
    Extracts the prerequisites from a course description
    Returns a string
    - description: description of course, type str
    '''

    pattern = re.compile(r'(?:Prerequisite|Prerequisites|Pre-requisite|Pre-requisites|Must have completed|Recommended preparation):\s*(.*?)(?=\n|\.|$)',
        re.IGNORECASE)  #   Regex code
    match = pattern.search(description)
    if match:   #   Search for regex
        return match.group(1).strip()   #   Return prereqs
    return "No prerequisites found"

def extract_code(course_name):
    pattern = re.compile(r'CMPUT \d{3}')    #   Regex pattern
    match = pattern.search(course_name)

    if match:
        return match.group()    #   Return code
    return None

def main():
    url = 'https://apps.ualberta.ca/catalogue/course/cmput' #   URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    course_dict = splitCourses(soup)
    prereqs = {course: extract_prequisites(description) for course, description in course_dict.items()}

    course = input("Enter course: ")
    print(prereqs[course])

if __name__ == "__main__":
    main()