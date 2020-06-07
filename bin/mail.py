#!/usr/bin/env python3.7
import os
from random import choice
from smtplib import SMTP_SSL
from datetime import date, datetime
from config import USER_EMAIL, TOKEN
from mailing_list import MAILING_LIST
from quotes import QUOTES
from email.mime.text import MIMEText

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
RECIPIENTS=MAILING_LIST
weekday = datetime.today().weekday()
random_choice = choice([x for x in range(0, len(QUOTES)) if x not in [weekday - 1, weekday - 2]])
quote = QUOTES[random_choice]

TODO_LIST_TECH = [
    "Recap Evernote life notes", "Read tech articles", "Play around with AWS free tier",
    "Recap Python notes", "Attempt leetcode exercise in evening",
    "Read chapter of Why We Sleep", "Attempt to tweet 4x"
]

TODO_LIST_MERGER = [
    "Recap Evernote quotes", "Read market articles", "Core exercise",
    "Recap Kubernetes notes", "Play around with AWS",
    "Read chapter of Why We Sleep", "Attempt to tweet 4x"
]

today = date.today().strftime("%d/%m/%Y")
def create_todos(todos):
    todo_format = f"TODO: ({today})\n"
    for note in todos:
        todo_format += f"* {note}\n"
    return todo_format

def read_file(category):
    with open(f"{DIR_PATH}/{category}_news.txt", "r") as f_obj:
        return f_obj.read().strip().encode('ascii', 'ignore').decode('ascii')

def create_body(category, list_todos=""):
    contents = ""
    contents += f"  \"<i><strong>{quote}</strong></i><br>"
    contents += f'<br>{list_todos}\n'
    contents += read_file(category)
    subject=f"Sendobot {category.title()} Newsletter"
    email_text = f"""\
<html>
<head>
<meta charset=“UTF-8”>
</head>
<body>
{contents}
From,<br>
<strong>Sendoka Bot</strong> <span style="font-size:30px">&#x1F916;</span>
</body>
</html>

""".format(todos=list_todos)
    return email_text

def main():
    todos = create_todos(TODO_LIST_TECH)

    try:
        with SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.ehlo()
            smtp.login(USER_EMAIL, TOKEN)
            for i, recipient in enumerate(RECIPIENTS):
                if i == 0:
                    tech_body = create_body("tech", todos)
                    # merger_body = create_body("merger", "")
                    # smtp.sendmail(USER_EMAIL, recipient, merger_body)
                    # print(f"Merger & Acquisitions news mail sent to: {recipient}")
                else:
                    tech_body = create_body("tech", "")
                msg = MIMEText(tech_body, 'html')
                msg['Subject'] = 'Daily Tech News From Senna'
                msg['from'] = USER_EMAIL
                smtp.sendmail(USER_EMAIL, recipient, msg.as_string())
                print(f"Tech news mail sent to: {recipient}")
    except Exception as e:
        print(e)

main()

