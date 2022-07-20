import android
import smtplib
import phonenumbers
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from email.mime.multipart import MIMEMultipart

sender_email = "sender@gmail.com"
receiver_email = "receiver@gmail.com"
password = "password"
answer = 'Hola!, esta es una respuesta automatizada, soy una persona sorda y por esta razón no puedo atender llamadas telefonicas, por esta razón es preferible contactarme via whatsapp o correo electronico a guillermo punto uno nueve ocho arroba gmail punto com'
osint_data = {}
message = MIMEMultipart("alternative")
message['Subject'] = 'Llamada recibida:'
message["From"] = sender_email
message["To"] = receiver_email

droid = android.Android()
droid.startTrackingPhoneState()
def IsSPAM(number):
    return responderono(number) == False

def responderono(number):
    html = urlopen("https://www.responderono.es/numero-de-telefono/" + number).read()
    soup = BeautifulSoup(html)
    unknown = soup.find_all('div', attrs={'class':'score unknown'})
    negative = soup.find_all('div', attrs={'class':'score negative'})
    neutral = soup.find_all('div', attrs={'class':'score neutral'})
    if (len(negative)>0 or len(neutral)>0):
        return False
    else:
        return True
def OSINT(number):
    parse = phonenumbers.parse(number)
    varrier = phonenumbers.carrier.name_for_number(parse, None)
    tiimezone = phonenumbers.timezone.time_zones_for_number(parse)
    region = phonenumbers.geocoder.description_for_number(parse, None)
    osint = "Número de telefono : " + parse + "\n"
    osint = "Proveedor de internet(ISP) es : " + varrier + "\n"
    osint = "Región: " + region + "\n"
    osint += "TimeZone: " + tiimezone + "\n"
    osint += "Posible link whatsapp :  https://wa.me/" + number + "\n"
    osint += "https://www.responderono.es/numero-de-telefono/" + number + "\n"

    return osint
def send(message):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender_email, password)
    s.sendmail(sender_email, receiver_email, message)
    s.quit()  

outerDict = droid.readPhoneState()
innerDict = outerDict['result']
number = innerDict['incomingNumber']
if number != None:
    if IsSPAM(number) == False:
        droid.makeToast("Preparado para responder...")
        message['Subject'] += number
        droid.speak(answer)
    else:
        droid.makeToast("Es SPAM")
        message['Subject'] = "spam: "+ number
        send('SPAM telefónico recibido:'+number)
    send(OSINT(number))
