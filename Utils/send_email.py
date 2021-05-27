import yagmail
import os

yag = yagmail.SMTP(os.environ.get("EMAIL"),os.environ.get("EMAIL_PASSWORD"))

def send_email(receiver,subject,body,filename):
    yag.send(
        to=receiver,
        subject=subject,
        contents=body, 
        attachments=filename if filename.strip() else None
    )