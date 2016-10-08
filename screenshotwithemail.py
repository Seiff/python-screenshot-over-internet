import poplib
from email import parser
from PIL import ImageGrab
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
# setup the poplib gmail server

pop_conn = poplib.POP3_SSL('pop.gmail.com')
pop_conn.user('the gmail')
pop_conn.pass_('the gmail password')
messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
messages = ["\n".join(m.decode() for m in mssg[1]) for mssg in messages]
messages = [parser.Parser().parsestr(mssg) for mssg in messages]
# smtp setup to send the image

def sendmail(ImgFileName):
    img_data = open(ImgFileName, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = 'subject'
    msg['From'] = 'the sender email which is the gmail'
    msg['To'] = 'the reciver'
    text = MIMEText("any text")
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)
    s = smtplib.SMTP('Smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login('the gmail', 'the gmail password')
    s.sendmail('sender email which is the gmail ', 'reciver', msg.as_string())
    s.quit()
# make gmail mark the emails that poplib reads as read from settings of gmail as poplib checks not read emails

def chkmsg():
        for message in messages:
            if message['subject'] == "the subject to trigger the action":
                im = ImageGrab.grab()
                im.save('screenshot.png')
                sendmail('screenshot.png')
                print('done')
chkmsg()
pop_conn.quit()
