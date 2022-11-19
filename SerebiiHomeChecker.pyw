import time
import smtplib
import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from datetime import datetime
import os
from os.path import exists
import secrets
from email.message import EmailMessage


#cd F:\Users\dudeo\AppData\Local\Programs\Python\Python39
#pyinstaller --onefile SerebiiHomeChecker.pyw
TheConfigurationFile = 'F:\\Users\\dudeo\\AppData\\Local\\Programs\\Python\\Python39\\dist\\Config.txt'


configTXT = 'F:\\Users\\dudeo\\AppData\\Local\\Programs\\Python\\Python39\\dist\\Config.txt'

def better_sleep(time2wait):
    start = time.time()
    while((time.time()-start)<time2wait-.00042):
        time.sleep(1)
#Get email and password
def login_info():
    configFile = open(TheConfigurationFile, 'r')
    config = str(configFile.read())
    email = config.split('Email: ')
    email = email[1].split('Password: ')
    password = str(email[1].strip())
    email = str(email[0].strip()).strip()
    try:
        server = config.split('Server: ')[1]
        server = str(server.split('Email: ')[0].strip())
    except:
        print('its the server')
    try:
        port = config.split('Port: ')[1]
        port = port.split('Server: ')[0].strip()
        port = int(str(port))
    except:
        print('port also fucked up')
    try:
        app = config.split('App Pass: ')[1]
        app = app.split('Port: ')[0].strip()
        app = str(app)
    except:
        print('port also fucked up')
    configFile.close()
    return email, password, server, port, app


#email function
def email(sites):
    myEmail, myPass, theServer, thePort, theAppPassword = login_info()
    configFile = open(configTXT, 'r')
    raw_emails = configFile.readlines()
    configFile.close()
    notDone = 1
    x = 0
    while notDone > 0:
        bad = 0
        for line in range(0, len(raw_emails)-x, 1):
            if ((str(raw_emails[line]).__contains__('@')) and ((str(raw_emails[line]).__contains__('.')))):
                if (str(raw_emails[line]).__contains__('Email')):
                    try:
                        raw_emails[line] = raw_emails[line+1]
                        raw_emails[line+1] = 0
                    except:
                        raw_emails[line] = 0
                else:                    
                    raw_emails[line] = str(raw_emails[line]).strip()
            else:
                try:
                    raw_emails[line] = raw_emails[line+1]
                    raw_emails[line+1] = 0
                except:
                    raw_emails[line] = 0
                bad = 1
        x=x+1
        if bad == 0:
            notDone = 0
        #print(raw_emails)
        
    the_emails = []
    for i in range(0, len(raw_emails), 1):
        if raw_emails[i] != 0:
            the_emails.append(raw_emails[i])
            print(the_emails[i])
    try:
        server = smtplib.SMTP_SSL(theServer, thePort)
        server.login(myEmail, theAppPassword)
        msge = EmailMessage()
        msge.set_content(sites)
        server.send_message(msge, from_addr=myEmail, to_addrs=myEmail)
        server.quit()
    except:
        better_sleep(1)
        logger = open('Pokemon.txt', 'a')
        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
        logger.write('\n')
        logger.write(dt_string + '\n')
        logger.write(str('Failed to send email to me!'))
        logger.close()
    for i in range(0, len(the_emails), 1):
        try:
            server = smtplib.SMTP_SSL(theServer, thePort)
            server.login(myEmail, theAppPassword)
            msge = EmailMessage()
            msge.set_content(sites)
            server.send_message(msge, from_addr=myEmail, to_addrs=str(the_emails[i]))
            server.quit()
        except:
            better_sleep(1)
            logger = open('Pokemon.txt', 'a')
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
            logger.write('\n')
            logger.write(dt_string + '\n')
            logger.write(str('Failed to send email to ' + str(the_emails[i]) + '!'))
            logger.close()



#pokemon checker
def Pokemon(counter, past):
    s = str(past)
    #s = 9
    #get the sites from the configuration file
    serebii_site = 'https://www.serebii.net/'
    print(serebii_site)
    short_serebii_site = 'serebii.net'
    msg = 'There is cool Pokemon info! Check out ' + short_serebii_site + '   --Love Evan'
    try:
        response = requests.get(serebii_site)
        site = str(response)
    except:
        site = 'Fucked'
    if site != "Fucked":
        logger = open('Pokemon.txt', 'a')
        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
        logger.write('\n')
        logger.write(dt_string + '\n')
        logger.write(str('serebii got response'))
        logger.close()
    bs_response = BeautifulSoup(response.text, "lxml")
    bs_response = bs_response.body.main.find(class_='subcat').getText()
    print(bs_response)
    bs_response = str(bs_response)
    stripped_bs_response = bs_response.replace(s, '')
    original_bs_response = str(bs_response)
    print('----------')
    print(stripped_bs_response)
    if bs_response == s:
        #there was not change to the site
        s = bs_response
        sendEmail = 0
        #sendEmail = 1 # comment out this line
    else:
        ignore = 0
        sendEmail = 0
        bs_response = str(stripped_bs_response)
        s = bs_response
        if bs_response.__contains__('In The Games'):
            if bs_response.__contains__('news') or bs_response.__contains__('istribution'):
                if bs_response.__contains__('mon GO'):
                    if bs_response.__contains__('Diancie') or bs_response.__contains__('Volcanion') or bs_response.__contains__('Deoxys'):
                        sendEmail = 1
                if bs_response.__contains__('asters E') or bs_response.__contains__('mon GO') or bs_response.__contains__('mon UNIT') or bs_response.__contains__('Caf') or bs_response.__contains__('mon Smil'):
                    sendEmail = 0
                    ignore = 1
                else:
                    sendEmail = 1
            else:
                if bs_response.__contains__('asters E') or bs_response.__contains__('mon UNIT') or bs_response.__contains__('Caf') or bs_response.__contains__('mon Smil') or bs_response.__contains__('VGC Ruleset'):
                    sendEmail = 0
                    ignore = 1
                sendEmail = 0
        elif bs_response.__contains__('The Pokémon Company'):
            sendEmail = 1
        elif bs_response.__contains__('Direct') or bs_response.__contains__('Present'):
            sendEmail = 1
        else:
            sendEmail = 0
        if bs_response.__contains__('TCG') or bs_response.__contains__('ards D'):
            sendEmail = 0
            ignore = 1
        #Check for special temporary key words
        if (sendEmail == 0) and (ignore == 0):
            spot = 0
            separatorIs = [5, 9]
            logger = open(configTXT, 'r')
            desiredInfoSeparators = '|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n'
            desiredLines = logger.readlines()
            #print(desiredLines)
            for i in range(10, len(desiredLines)):
                if desiredLines[i] == desiredInfoSeparators:
                    separatorIs[spot] = i
                    spot = spot + 1
                    if spot == 3:
                        i = 2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2
            i = 0
            for i in range(separatorIs[0]+1, separatorIs[1]):
                #print(i)
                line_no_space = desiredLines[i].split('\n')[0]
                line_no_space = line_no_space.rstrip()
                if bs_response.__contains__(line_no_space):
                    print(line_no_space)
                    sendEmail = 1
                    i = 2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2
                    
        #sendEmail = 1 # comment out this line
    if counter > 0:
        if sendEmail == 1:
            #print('sending email')
            email(str(msg))
            logger = open('Pokemon.txt', 'a')
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
            logger.write('\n')
            logger.write(dt_string + '\n')
            logger.write('New Info!\n')
            logger.close()
        else:
            #print('not sending email')
            logger = open('Pokemon.txt', 'a')
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
            logger.write('\n')
            logger.write(dt_string + '\n')
            logger.write('No New Info\n')
            logger.close()
    else:
        logger = open('Pokemon.txt', 'a')
        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
        logger.write('\n')
        logger.write(dt_string + '\n')
        logger.write('Just started.  Not sending the email. \n')
        logger.close()
        pastsoup = s
    msg = 'Go to: '
    sendEmail = 0
    s = original_bs_response
    return s


def main():
    #email('This is a test.  Current BDSP events are Shayman.  Connect to Mystery Gift internet.  Starting April 1st to April 30th connect to MG internet and get Darkrai.  I love you a ton and once I finish school I promis Ill have more game time for you <3')
    z = 0
    count = 0
    daycount = count
    past = 0
    if(exists('Pokemon.txt')):
        pass
    else:
        logger = open('Pokemon.txt', 'w')
        logger.write('This is the log of stuff:' + '\n')
        logger.close()
    while z < 30:
        # should do the initializing
        # wont send email.  Just doing set up
        if count == 0:
            past_soup = Pokemon(count,  past)
        #now the set up is done do the check for real
        if count > 0:
            now = datetime.now()
            today = now.strftime("%I")
            if today == past:
                past = today
            else:
                try:
                    past_soup = Pokemon(count, past_soup)
                except:
                    msg = 'There was a main() error on home. Maybe check serebii'
                    email(msg)
                    logger = open('Pokemon.txt', 'a')
                    now = datetime.now()
                    dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
                    logger.write('\n')
                    logger.write(dt_string + '\n')
                    logger.write('There was a main() error on home serebii. \n' + '\n')
                    logger.close()
                past = today
                daycount = daycount + 1
        better_sleep(secrets.randbelow(7))
        count = count + 1
        #print(count)

        better_sleep(8)
        
if __name__ == '__main__':
    main()








