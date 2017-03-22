#!/usr/bin/python

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os,re
from random import randint
from time import sleep

gmail_user = "your gmail id"
gmail_pwd = "yourpassword"

def mail(to, subject, attach, recruitername ):
   msg = MIMEMultipart()

   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject
   text = """
Hi  %s

 this is a dummy email , 
 
 i have hattached a dummy document . 

 Regards
 xyz
 +91 9818888888
 ( xyx@gmail.com )

""" %  recruitername

   msg.attach(MIMEText(text))

   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach, 'rb').read())
   Encoders.encode_base64(part)
   part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach))
   msg.attach(part)

   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()


myemailfile = "/opt/emails_list.txt"
#myemailfile = "/tmp/ee"
emaillist =  open( myemailfile, 'r')


for i in emaillist.readlines()[0:]:
    match = re.search(r'[\w\.-]+@[\w\.-]+', i)
    if not  match:
        continue
    #sleep(randint(1,3))
    print "%s " % match.group(0)
    hrname =  str(re.split("\.|_|-", match.group(0).split('@')[0] )[0])
    
    #hrname = ''
    mail( match.group(0) , "Re:  dummy subject line here  ","/scripts/dummydoc.pdf" , hrname )
