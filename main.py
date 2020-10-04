#!/usr/bin/python
# -- coding: utf-8 --
import csv
import ssl
import smtplib

# Constants found in csv file
PAIRNR = 0
NAME = 2
EMAIL = 3
PHONENR = 4
ADRESS = 5
ALERGY = 6
TEAMMEMBER = 7
ALCHOL = 9
TOCOOK = 11
PLACE1 = 12
PLACE2 = 13
PLACE3 = 14


#Defines a class "pair", contact info and preferences
class Pair:

    def __init__(self, pairnr, name, email, phonenr, adress, alergy, teammember,alchol, tocook, place1, place2, place3):
        self.pairnr = pairnr
        self.name = name
        self.email = email
        self.phonenr = phonenr
        self.adress = adress
        self.alergy = alergy
        self.teammember = teammember
        self.alchol = alchol
        self.tocook = tocook
        self.place1 = place1
        self.place2 = place2
        self.place3 = place3

# Read csv file and return a 2d array width person
def Read_file(File_path):
    with open(File_path, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        pairs = []

        for row in spamreader:
            pair = Pair(row[PAIRNR],row[NAME],row[EMAIL],row[PHONENR],row[ADRESS],row[ALERGY],row[TEAMMEMBER],row[ALCHOL], row[TOCOOK], -1,-1,-1)
            pairs.append(pair)

        del pairs[0]

        for p in pairs:
            #abc = "-1"
            print(p.tocook, type(p.tocook))
            print(int(p.tocook), type(p.tocook))

            #p.pairnr = int(p.pairnr,base=10)

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
def decide_meal(pairs):

    unasigned_tocook = []
    meal_1 = []
    meal_2 = []
    meal_3 = []

    for p in pairs:

        if p.tocook == -1:
            unasigned_tocook.append(p)
        elif p.tocook == 1:
            meal_1.append(p)
        elif p.tocook == 2:
            meal_2.append(p)
        elif p.tocook == 3:
            meal_3.append(p)

    amont_of_pairs = len(pairs)
    amount_of_people_per_meal = amont_of_pairs / 3

    for p in unasigned_tocook:
        if amount_of_people_per_meal > len(meal_1):
            p.tocook = 1
            meal_1.append(p)
            print(p.name)
        elif amount_of_people_per_meal > len(meal_2):
            p.tocook = 2
            meal_2.append(p)
        else:
            p.tocook = 3
            meal_3.append(p)

    pairs = []
    for m in meal_1:
        pairs.append(m)
    for m in meal_2:
        pairs.append(m)
    for m in meal_3:
        pairs.append(m)

    strike_pair = adress_check(pairs)
    if len(strike_pair) > 0:
        i = 0
        for s in strike_pair:
            if i % 2 == 0:
                if s.tocook == 1:
                    for p in pairs:
                        if p.tocook != 1:
                            print("Time to swap a meal in group 1")
                            pairs = swap_meal(pairs, s, p)
                            break

                elif s.tocook == 2:
                    for p in pairs:
                        if p.tocook != 2:
                            print("Time to swap a meal in group 2")
                            pairs = swap_meal(pairs, s, p)
                            break

                elif s.tocook == 3:
                    for p in pairs:
                        if p.tocook != 3:
                            print("Time to swap a meal in group 3")
                            pairs = swap_meal(pairs, s, p)
                            break

            i +=1

    return pairs

def adress_check(pairs):

    pairs_meal_1 = []
    pairs_meal_2 = []
    pairs_meal_3 = []

    for pair in pairs:
        if pair.tocook == 1:
            pairs_meal_1.append(pair)
        elif pair.tocook == 2:
            pairs_meal_2.append(pair)
        elif pair.tocook == 3:
            pairs_meal_3.append(pair)

    strike_pairs = []

    for a in pairs_meal_1:
        for b in pairs_meal_1:
            if (a.adress.lower() == b.adress.lower()) and (a.pairnr != b.pairnr):
                strike_pairs.append(b)

    for a in pairs_meal_2:
        for b in pairs_meal_2:
            if (a.adress.lower() == b.adress.lower()) and (a.pairnr != b.pairnr):
                strike_pairs.append(b)

    for a in pairs_meal_3:
        for b in pairs_meal_3:
            if (a.adress.lower() == b.adress.lower()) and (a.pairnr != b.pairnr):
                strike_pairs.append(b)

    for s in strike_pairs:
        print("Strike pairs = ", s.name)

    print("Strike pair lengh: ", len(strike_pairs))

    return strike_pairs

def swap_meal(pairs, pair1, pair2):

    print(pair1.name, " har nr ",pair1.tocook, pair2.name, "har nr " ,pair2.tocook)

    i = 0
    for p in pairs:
        if p.pairnr == pair1.pairnr:
                del pairs[i]
        if p.pairnr == pair2.pairnr:
                del pairs[i]
        i += 1

    meal_for_pair1 = pair1.tocook
    meal_for_pair2 = pair2.tocook

    pair1.tocook = meal_for_pair2
    pair2.tocook = meal_for_pair1

    print(meal_for_pair1,meal_for_pair2)

    print(pair1.name, " har nr ",pair1.tocook, pair2.name, "har nr " ,pair2.tocook)

    pairs.append(pair1)
    pairs.append(pair2)

    print("Swapped ", pair1.name , " with ", pair2.name , ".")

    return pairs

# Decide everyone's route
def decide_route(p):
    list.append(p,2)

    return p


def main():
    pairs = Read_file("Test.csv")

    pairs = decide_meal(pairs)

    for p in pairs:
        print(p.pairnr, " Namn: ", p.name, "Adress: ", p.adress, "Måltid: ", p.tocook)

main()
