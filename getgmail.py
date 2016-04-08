import imaplib, sys, email, time 

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('your email id', 'yourpassowrd')
mail.list()
# Out: list of "folders" aka labels in gmail.
mail.select("inbox") # connect to inbox.


#result, data = mail.search(None, '(HEADER Subject "devops" NOT Subject "Dice JobAlert - DevOps" NOT Subject "Dice JobAlert - linux devops" NOT FROM "jagent@route.monster.com" SINCE "01-Mar-2015")')
#result, data = mail.search(None, '(HEADER FROM "member@linkedin.com" SINCE "01-Jan-2015")')
#result, data = mail.search(None, '(HEADER FROM "mailer-daemon" FROM "postmaster" SINCE "01-Aug-2015")')
result, data = mail.search(None, '(HEADER FROM "@naukri.com" SINCE "27-Jan-2016")')
#result, data = mail.search(None, '(HEADER FROM "@monsterindia.com" SINCE "01-Aug-2015")')

for num in reversed(data[0].split()):
    rv, data = mail.fetch(num, '(RFC822)')
    raw_email = data[0][1] # here's the body, which is raw text of the whole email
# including headers and alternate payloads
    

    email_message = email.message_from_string(raw_email)
    if email_message['Reply-To'] in ( None,): 
        continue
    print email_message['Reply-To']
