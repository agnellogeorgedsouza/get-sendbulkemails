import imaplib, sys, email, time 

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('your email id', 'yourpassowrd')
mail.list()
# Out: list of "folders" aka labels in gmail.
mail.select("inbox") # connect to inbox.



result, data = mail.search(None, '(HEADER FROM "@somedomain.com.com" SINCE "27-Jan-2016")')
#result, data = mail.search(None, '(HEADER FROM "@monsterindia.com" SINCE "01-Aug-2015")')

for num in reversed(data[0].split()):
    rv, data = mail.fetch(num, '(RFC822)')
    raw_email = data[0][1] # here's the body, which is raw text of the whole email
# including headers and alternate payloads
    

    email_message = email.message_from_string(raw_email)
    if email_message['Reply-To'] in ( None,): 
        continue
    print email_message['Reply-To']
