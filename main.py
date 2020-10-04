#!/usr/bin/python
# -- coding: utf-8 --
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
        self.tocook = tocook
        self.place1 = place1
        self.place2 = place2
        self.place3 = place3

# Read csv file and return a 2d array width person
def Read_file(File_path):
    with open(File_path, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        pairs = []
        for row in spamreader:
            pair = Pair(row[TEAMNR],row[NAME],row[EMAIL],row[PHONENR],row[ADRESS],row[ALERGY],row[TEAMMEMBER],-1,-1,-1,-1,-1)
            pairs.append(pair)

    del pairs[0]

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
def decide_meal(Pairs):

    amont_of_pairs = len(Pairs)
    amount_of_pepole_per_meal = amont_of_pairs / 3

    i = 0
    for pair in Pairs:
        if i <= amount_of_pepole_per_meal:
            pair.tocook = 1
        elif i <= amount_of_pepole_per_meal*2:
            pair.tocook = 2
        else:
            pair.tocook = 3

        i+=1

    strike_pair = adress_check()
    if len(strike_pair) > 0:
        i = 0
        for s in strike_pair:
            if i % 2 == 0:
                if s.tocook == 1:

                elif s.tocook == 2:

                elif s.tocook == 3:



        i +=1


    return Pairs


def adress_check(Pairs):

    adress_meal_1 = []
    adress_meal_2 = []
    adress_meal_3 = []
    for pair in Pairs:
        if pair.tocook == 1:
            adress_meal_1.append(pair.adress)
        elif pair.tocook == 2:
            adress_meal_2.append(pair.adress)
        elif pair.tocook == 3:
            adress_meal_3.append(pair.adress)
    strike_pair = []
    for p in Pairs:
        strike = 0
        for a in adress_meal_1:
            if p.adress.lower() == a.lower():
                strike +=1
                if strike > 1:
                    strike_pair.append(pair)
        for a in adress_meal_2:
            if p.adress.lower() == a.lower():
                strike +=1
                if strike > 1:
                    strike_pair.append(pair)
        for a in adress_meal_3:
            if p.adress.lower() == a.lower():
                strike +=1
                if strike > 1:
                    strike_pair.append(pair)

    return strike_pair

def swap_meal(pair1,pair2):

    meal_for_pair1 = pair1.tocook
    meal_for_pair2 = pair2.tocook

    pair1.tocook = meal_for_pair2
    pair2.tocook = meal_for_pair1


    return pair1,pair2

# Decide everyone's route
def decide_route(p):
    list.append(p,2)

    return p


def main():
    pairs = Read_file("../Test.csv")

    decide_meal(pairs)



main()
