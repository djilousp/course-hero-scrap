import requests
import pandas as pd
from termcolor import colored
import sys
from fake_useragent import UserAgent

questions = {}
question_num = 0
for subject_id in range(1, 3499):
    print(colored('[+]','green'), colored('Scrapping Subject id = '), colored(f'{subject_id}.....', 'red'))
    baseUrl = f"https://www.coursehero.com/api/v1/school/{subject_id}/questions/?offset=0&limit=5000&dataArray=true&cacheComposite=false"
    headers = {'User-Agent': ua.random,}
    try:
        response = requests.get(baseUrl, headers=headers)
        print(response.text)
        if (response.status_code == 200):
            print("status 200")
            for question in response.json():
                question_id = question['question_id']
                name = question['name']
                content = question['question']
                subject = question['subject']
                date_asked = question['date_asked']
                question_num = question_num + 1 
                questions[question_num] = [question_id, subject, name, content, date_asked]
                items_df = pd.DataFrame.from_dict(questions, orient='index', columns = ['Question N˚', 'Subject' ,'Name', 'Content', 'Date'])
                items_df.to_csv('questions.csv')  
    except KeyboardInterrupt:
        # quit
        sys.exit()
    except:
        items_df = pd.DataFrame.from_dict(questions, orient='index', columns = ['Question N˚', 'Subject' ,'Name', 'Content', 'Date'])
        items_df.to_csv('questions.csv')   
    
 
items_df = pd.DataFrame.from_dict(questions, orient='index', columns = ['Question N˚', 'Subject' ,'Name', 'Content', 'Date'])
items_df.to_csv('questions.csv')
    