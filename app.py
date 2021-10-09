from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import smtplib
import re

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        # This video downloader was created for the site animepisode.com

        print("Starting Download...")

        r = requests.get(url)
        soup = BeautifulSoup(r.content, features="lxml")

        for val in soup.find_all():
            if (re.search("let video2 = '<iframe allowfullscreen=", str(val))) is not None:
                result = str(val)

        address = re.search("(?P<url>https?://www[^\s]+)", result).group("url")
        address = address.replace('"', '')

        print("Accessed first url - ", address)

        r = requests.get(address)
        soup = BeautifulSoup(r.content, features="html.parser")

        mp4_source_tag = soup.find('source', attrs={'type': 'video/mp4'})
        mp4_url = mp4_source_tag['src']

        print("Downloading mp4 file - ", mp4_url)

        split_url = re.split("/", url)
        filename = split_url[len(split_url) - 2] + ".mp4"
        print("Mp4 file -", filename, "accessed")
        r = requests.get(mp4_url)

        with open(filename, 'wb') as f:
            f.write(r.content)

        print("Download Finished\nCommencing Email")
        FROM = "elone.mailer@gmail.com"
        PASS = "hawal123!"
        TO = "Rathcoole786@gmail.com"
        PORT = 587
        SERVER = "smtp.gmail.com"
        CONTENT = ""

        msg = MIMEMultipart()

        msg['From'] = FROM
        msg['To'] = TO
        msg['Subject'] = "Anime Episode <Automated>"
        filename = "/Users/Admin/Downloads/"
        file = open("/Users/Admin/Documents/AnimeVideoMailer/src/"+filename, 'rb')

        # msg.attach(MIMEText())
        return render_template('finish.html', file=file, filename=filename)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
