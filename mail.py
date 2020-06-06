#!/usr/bin/env python
from smtplib import SMTP_SSL
from datetime import date
from config import USER_EMAIL, TOKEN
from mailing_list import MAILING_LIST

RECIPIENTS=MAILING_LIST[-1]

TODO_LIST_TECH = [
    "Recap Evernote life notes", "Read tech articles", "Core exercise",
    "Recap Javascript notes", "Attempt leetcode exercise in evening",
    "Read chapter of Why We Sleep", "Attempt to tweet 3x"
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

def create_body(category):
    contents = ""
    contents += " \"If we do not make the unconscious conscious, it will direct our life and we will call it fate\"\n\n"
    todos = TODO_LIST_TECH if category == "tech" else TODO_LIST_MERGER
    todos = create_todos(todos)
    contents += f'{todos}\n'
    contents += read_file(category)
    subject=f"Sendobot TODOs & {category.title()} Newsletter"
    email_text = f"""\
From: {USER_EMAIL}
To: {RECIPIENTS}
Subject: {subject}

{contents}

From Sendoka bot :)
"""
    return email_text

def main():
    tech_body = create_body("tech")
    merger_body = create_body("merger")

    emails = [{"title": "Tech news", "body": tech_body}, {"title": "Merger news", "body": merger_body}]
    try:
        with SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.ehlo()
            smtp.login(USER_EMAIL, TOKEN)
            for email in emails:
                smtp.sendmail(USER_EMAIL, RECIPIENTS, email['body'])
                print(f"{email['title']} mail sent to: {RECIPIENTS}")
    except Exception as e:
        print(e)

main()

