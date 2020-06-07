#!/usr/bin/env python
from smtplib import SMTP_SSL
from datetime import date
from config import USER_EMAIL, TOKEN
from mailing_list import MAILING_LIST

RECIPIENTS=MAILING_LIST

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
    with open(f"{category}_news.txt", "r") as f_obj:
        return f_obj.read().strip().encode('ascii', 'ignore').decode('ascii')

def create_body(category, list_todos=""):
    contents = ""
    contents += " \"We have two lives and the second one begins when we realise we only have one - Conficious\"\n\n"
    contents += f'{list_todos}\n'
    contents += read_file(category)
    subject=f"Sendobot {category.title()} Newsletter"
    email_text = f"""\
From: {USER_EMAIL}
To: {RECIPIENTS}
Subject: {subject}

{contents}

From Sendoka bot :)
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
                    merger_body = create_body("merger", "")
                    smtp.sendmail(USER_EMAIL, recipient, merger_body)
                    print(f"Merger & Acquisitions news mail sent to: {recipient}")
                else:
                    tech_body = create_body("tech", "")

                smtp.sendmail(USER_EMAIL, recipient, tech_body)
                print(f"Tech news mail sent to: {recipient}")
    except Exception as e:
        print(e)

main()

