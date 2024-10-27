import time, os
import requests, selectorlib
import smtplib, ssl
URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}
DEFAULT_ACCOUNT = "silvanas.python.projects@gmail.com"


def scrape(url):
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message, username=DEFAULT_ACCOUNT, receiver=DEFAULT_ACCOUNT):
    host = "smtp.gmail.com"
    port = 465
    password = os.getenv("PASSWORD_PYTHON_PROJECTS")
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
    print("Email was sent!")


def store(extracted):
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")


def read():
    try:
        with open("data.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        return ""


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        if extracted != "No upcoming tours":
            content = read()
            if extracted not in content:
                store(extracted)
                send_email(message="Hey a new event was found!")
        time.sleep(2)
