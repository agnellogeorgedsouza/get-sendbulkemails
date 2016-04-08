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

 How are you doing. You  had sent me a email throuth Naukri regarding the DevOps role.



         Few of the important technologies i have been working on :

  1.        AWS (  EC2 , ELB , CloudFront, Elasticcache , S3 , RDS, Route53  , autoscaling and used cloudformation)
  2.       HAproxy , Nginx  , apache
  3.       mysql ( mater-salve replication)
  4.       ELK ( elasticsearch , Logstash , Kibana )
  5.       Nagios  and plugin development
  6.       Jenkins , puppet and Ansible
  7.       scripting languages in Python , perl , shell scripting
  ----------------------------------------------------------------------------------------------

  ( You may forward this to any other HR/ recruiter that my be looking out for my skill sets )


   
 Please find attached my resume 

 It would be nice to hear from you

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
    #print "%s " % hrname
    #hrname = ''
    mail( match.group(0) , "Re:  Looking for job opportunities in yyeerrdd ","/scripts/resume.pdf" , hrname )
