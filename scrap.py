import requests
import pandas as pd
from termcolor import colored
import sys
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

questions = {}
question_num = 0
for subject_id in range(1, 3500):
    print(colored('[+]','green'), colored('Scrapping Subject id = '), colored(f'{subject_id}.....', 'red'))
    baseUrl = f"https://www.coursehero.com/api/v1/school/{subject_id}/questions/?offset=0&limit=5000&dataArray=true&cacheComposite=false"
    ua = UserAgent()
    #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',}
    headers = {'User-Agent': ua.random}
    # try:
    response = requests.get(baseUrl, headers=headers)
    print(response.status_code)
    if (response.status_code == 200):
        for question in response.json(): 
            resource_url = question['resource_url']
            response2 = requests.get(f'https://www.coursehero.com{resource_url}', headers=headers)
            #response2 = requests.get(f'https://www.coursehero.com/tutors-problems/Nursing/31064094-Only-answer-if-you-are-sure-No-guess-work-Two-nurses-are-establishing/', headers=headers)
            question_id = question['question_id']
            print(colored('[++]','green'), colored('Fetching data from Question = '), colored(f'{question_id}.....', 'red')) 
            soup = BeautifulSoup(response2.content, features="html.parser")
            content = soup.select(".question-text", limit=1)
            if len(content):
                content = content[0].get_text(separator='\n', strip=True)
                name = question['name']
                subject = question['subject']
                date_asked = question['date_asked']
                question_num = question_num + 1 
                questions[question_num] = [question_id, subject, name, date_asked]
                items_df = pd.DataFrame.from_dict(questions, orient='index', columns = ['Question N˚', 'Subject' ,'Name', 'Date'])
                items_df.to_csv('questions.csv')  
    # except KeyboardInterrupt:
    #     # quit
    #     sys.exit()
    # except:
    #     items_df = pd.DataFrame.from_dict(questions, orient='index', columns = ['Question N˚', 'Subject' ,'Name', 'Content', 'Date'])
    #     items_df.to_csv('questions.csv')   
    
    