import requests
import lxml
from bs4 import BeautifulSoup
from pandas import DataFrame
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from datetime import datetime
import pathlib

currentMonth = datetime.now().month
currentYear = datetime.now().year
base_url = 'https://www.livegigs.de/frankfurt-main/ska/umkreis-50?Page={}#Termine'
current_dir = pathlib.Path(__file__).parent.resolve()
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


def send_mail(send_to:list, df:DataFrame) -> None:

    if not log_file.is_file():
        subject = f"Monthly SKA Update {currentMonth}/{currentYear}"
        send_from = "your_email@outlook.com"
        password = "your_pw"
        message = """\
        <p>Hi,</p>
        <p>your monthly SKA Update is here!</p>
        <p><br></p>
        <p>{}</p>
        <p>Best,</p>
        <p>Your Name</p>
        """.format(df.to_html())
        
        for receiver in send_to:
            multipart = MIMEMultipart()
            multipart["From"] = send_from
            multipart["To"] = receiver
            multipart["Subject"] = subject  
            multipart.attach(MIMEText(message, "html"))
            server = smtplib.SMTP('smtp-mail.outlook.com',587) 
            type(server) 
            server.ehlo()
            server.starttls()
            server.login(multipart["From"], password)
            server.sendmail(multipart["From"], multipart["To"], multipart.as_string())
            server.quit()

        log_file.touch(exist_ok=True)
        
if __name__ == "__main__":
    send_mail(['recipient1@outlook.com', 'recipient2@outlook.com'],scrap_data())
