from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
from pywebio.session import go_app,hold

url = None
def defualt():
    put_markdown("## Welcome to Amazon Watcher")
    put_image(open("../static/assets/stonks.jpg",'rb').read())

def homepage():
    global url
    defualt()
    url = input("Enter the url:",type=TEXT,placeholder="https://amazon.in/")
    go_app('task_1',new_window=False)

def scrape_result():
    name= "Loading"
    url = "https://loading.com"
    price = 5000
    defualt()
    put_row(
            [
                put_text(f"Name: "),
                put_link(name=name,url=url)
            ]
    )
    put_text(f"Current Price: {price}")
    put_buttons(["Confirm"],[lambda:go_app("task_2",new_window=False)])
    hold()

def set_condition():
    defualt()
    date = input("Expiration Date",type=DATE)
    time = input("Enter the frequency of checking in HH:MM format",type=TEXT)
    put_text(f"Expiry: {date}, Frequency: {time}")
    put_buttons(['Next'],onclick= lambda x:go_app("task_3",new_window=False))
    hold()

def confirm_email():
    defualt()
    email = input("Enter your email ID",type=TEXT)
    otp = input(f"Enter the OTP recieved in {email}")
    put_markdown("## ☑ Succesfully registered for the alert")
    hold()


start_server({"index":homepage,"task_1":scrape_result,"task_2":set_condition,"task_3":confirm_email})