import requests
import os
import lxml
import smtplib
from yaml import safe_load
from bs4 import BeautifulSoup
from pandas import DataFrame
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from pathlib import Path

currentMonth = datetime.now().month
currentYear = datetime.now().year
base_url = 'https://www.livegigs.de/frankfurt-main/ska/umkreis-50?Page={}#Termine'
current_dir = Path(__file__).parent.resolve()
Path(current_dir/'log_files').mkdir(parents=True, exist_ok=True)
log_dir = current_dir/'log_files'
log_file = log_dir/f'{currentMonth}_{currentYear}.txt'

def scrap_data() -> DataFrame:
    is_last_page = False
    page_counter = 1
    concert_list = []
    link_list = []

    while is_last_page == False:
        request = requests.get(base_url.format(page_counter))
        soup = BeautifulSoup(request.text, 'lxml')

        if soup.select('.title') == []:
            is_last_page = True
        else:
            for concert in soup.select('.title'):
                for a in concert.find_all('a', href=True):
                    href = a['href']
                    concert_link = 'https://www.livegigs.de/' + href
                    concert_url = href.split('/')
                    concert_url = concert_url[2:]
                    concert_list.append(concert_url)
                    link_list.append(concert_link)

            df = DataFrame(concert_list, columns=['Artist','Venue','Date'])
            df['Link'] = link_list
            page_counter +=1
    return df


def send_mail(send_to:list) -> None:
    if not log_file.is_file():
        scrapped_data:DataFrame = scrap_data()
        load_dotenv()
        sender_email = os.getenv('email_sender')
        sender_email_pw = os.getenv('email_sender_pw')
        sender_name = os.getenv('name_sender')
        subject = f"Monthly SKA Update {currentMonth}/{currentYear}"
        message = """\
        <p>Hi,</p>
        <p>your monthly SKA Update is here!</p>
        <p><br></p>
        <p>{}</p>
        <p>Best,</p>
        <p>{}</p>
        """.format(scrapped_data.to_html(), sender_name)
        
        for receiver in send_to:
            multipart = MIMEMultipart()
            multipart["From"] = sender_email
            multipart["To"] = receiver
            multipart["Subject"] = subject  
            multipart.attach(MIMEText(message, "html"))
            server = smtplib.SMTP('smtp-mail.outlook.com',587) 
            type(server) 
            server.ehlo()
            server.starttls()
            server.login(multipart["From"], sender_email_pw)
            server.sendmail(multipart["From"], multipart["To"], multipart.as_string())
            server.quit()

        log_file.touch(exist_ok=True)
        
if __name__ == "__main__":
    with open(current_dir / 'recipient_email_config.yml') as config_file:
        recipient_email_list = safe_load(config_file)
    send_mail(recipient_email_list)
