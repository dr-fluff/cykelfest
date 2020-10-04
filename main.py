import csv
import ssl
import smtplib

# Constants
TEAMNR = 0
NAME = 2
EMAIL = 3
PHONENR = 4
ADRESS = 5
ALERGY = 6
TEAMMEMBER = 7
MEAL = 8
PLACE1 = 9
PLACE2 = 10
PLACE3 = 11

#Defines a class "pair", contact info and preferences
class Pair:

    def __init__(self, pairnr, name, email, phonenr, adress,friend, alergy, teammember, tocook, place1, place2, place3):
        self.pairnr = pairnr
        self.name = name
        self.friend = friend
        self.email = email
        self.phonenr = phonenr
        self.adress = adress
        self.alergy = alergy
        self.teammember = teammember

# Read csv file and return a 2d array width person
def Read_file(File_path):
    with open(File_path, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        pairs = []
        for row in spamreader:
            pair = Pair(row[TEAMNR],row[NAME],row[EMAIL],row[PHONENR],row[ADRESS],row[ALERGY],row[TEAMMEMBER],-1,-1,-1,-1,-1)
            pairs.append(pair)

    return pairs

# Send an email to recipent with message
def send_email(recipient, message):
    sender = "max@idermark.com"
    port = 465 #for ssl
    password = "asd"

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, message.encode("utf-8"))


# Decide all
def decide_meal(persons):

    return persons


# Decide everyone's route
def decide_route(p):
    list.append(p,2)

    return p


def main():
    pairs = Read_file("../Test.csv")


main()
