#!/usr/bin/python
# -- coding: utf-8 --
import csv
import math
import ssl
import smtplib
from collections import Counter
import datetime
import random

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

# Meal constants
STARTER = 1
MAIN_COURSE = 2
DESERT = 3


# Defines a class "pair", contact info and preferences
class Pair:

    def __init__(self, pairnr, name, email, phonenr, adress, alergy, teammember, alchol, tocook, place1, place2,
                 place3):
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
            pair = Pair(row[PAIRNR], row[NAME], row[EMAIL], row[PHONENR], row[ADRESS], row[ALERGY], row[TEAMMEMBER],
                        row[ALCHOL], row[TOCOOK], -1, -1, -1)
            pairs.append(pair)

        del pairs[0]

        for p in pairs:
            p.tocook = int(p.tocook)

    return pairs


# Send an email to recipient with message
def send_email(recipient, subject, message):
    sender = ""
    password = ""

    mail = f"""\
Subject: {subject}
To: {recipient}
From: {sender}
{message}

""".format(sender, recipient, subject, message)

    # Create a secure SSL context
    port = 465  # for ssl
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, mail.encode("utf-8"))



# Decide all
def decide_meal(pairs):
    unasigned_tocook = []
    meal_1 = []
    meal_2 = []
    meal_3 = []

    for p in pairs:
        if p.tocook == -1 or p.tocook == 0:
            unasigned_tocook.append(p)
        elif p.tocook == 1:
            meal_1.append(p)
        elif p.tocook == 2:
            meal_2.append(p)
        elif p.tocook == 3:
            meal_3.append(p)

    amount_of_pairs = len(pairs)
    amount_of_people_per_meal = int(math.ceil(amount_of_pairs / 3.0))

    i = 0
    for p in unasigned_tocook:
        if amount_of_people_per_meal > len(meal_1):
            p.tocook = STARTER
            unasigned_tocook[i].tocook = STARTER
            meal_1.append(p)
        elif amount_of_people_per_meal > len(meal_2):
            p.tocook = MAIN_COURSE
            unasigned_tocook[i].tocook = MAIN_COURSE
            meal_2.append(p)
        else:
            p.tocook = DESERT
            unasigned_tocook[i].tocook = DESERT
            meal_3.append(p)

        i +=1

    pairs = []
    for m in meal_1:
        pairs.append(m)
    for m in meal_2:
        pairs.append(m)
    for m in meal_3:
        pairs.append(m)

    strike_pair = address_check(pairs)
    if len(strike_pair) > 0:
        i = 0
        for s in strike_pair:
            if i % 2 == 0:
                if s.tocook == 1:
                    for p in unasigned_tocook:
                        if p.tocook != 1:
                            print("Time to swap a meal in group 1")
                            pairs = swap_meal(pairs, s, p)
                            break

                elif s.tocook == 2:
                    for p in unasigned_tocook:
                        if p.tocook != 2:
                            print("Time to swap a meal in group 2")
                            pairs = swap_meal(pairs, s, p)
                            break

                elif s.tocook == 3:
                    for p in unasigned_tocook:
                        if p.tocook != 3:
                            print("Time to swap a meal in group 3")
                            pairs = swap_meal(pairs, s, p)
                            break

            i += 1

    return pairs


def address_check(pairs):
    pairs_meal_1 = []
    pairs_meal_2 = []
    pairs_meal_3 = []

    for pair in pairs:
        if pair.tocook == STARTER:
            pairs_meal_1.append(pair)
        elif pair.tocook == MAIN_COURSE:
            pairs_meal_2.append(pair)
        elif pair.tocook == DESERT:
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

    if len(strike_pairs) > 0:
        print("multiple pairs using same address")
        for s in strike_pairs:
            print(s.pairnr, "Name: ", s.name, "Address: ", s.adress)

    return strike_pairs


# Help function for swapping meals
def swap_meal(pairs, pair1, pair2):
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

    pairs.append(pair1)
    pairs.append(pair2)

    print("Swapped ", pair1.name, " with ", pair2.name, ".")

    return pairs


# Decide everyone's route
def decide_route(pairs):
    starter_list = []
    main_corse_list = []
    desert_list = []

    org_pairs = pairs

    while len(pairs) % 3 != 0:
        pair = Pair(-1, -1, -1, -1, -1, -1, -1, -1, 3, -1, -1, -1)
        pairs.append(pair)

    for p in pairs:
        if p.tocook == STARTER:
            starter_list.append(p)
        elif p.tocook == MAIN_COURSE:
            main_corse_list.append(p)
        elif p.tocook == DESERT:
            desert_list.append(p)

    print(len(desert_list),len(main_corse_list),len(starter_list))

    all_meal_groups = []
    for i in range(len(starter_list)):
        rout_group = []
        for j in range(3):
            meal_group = [None,None,None]

            meal_group[0] = starter_list[i]
            meal_group[1] = main_corse_list[(i+j) % len(main_corse_list)]
            meal_group[2] = desert_list[(i+(j*2)) % len(desert_list)]

            #print(meal_group[0].pairnr,meal_group[1].pairnr,meal_group[2].pairnr)

            """
            if j == 0:
                meal_group[1] = main_corse_list[i]
                meal_group[2] = desert_list[i]

                print(meal_group[0].pairnr, meal_group[1].pairnr, meal_group[2].pairnr)

            # main corse
            elif j == 1:

                meal_group[1] = main_corse_list[(i+1) % (len(main_corse_list)-1)]
                meal_group[2] = desert_list[((i*2)-1) % len(main_corse_list)-1]

                print(meal_group[0].pairnr,meal_group[1].pairnr,meal_group[2].pairnr)

            # Desert
            elif j == 2:
                meal_group[1] = main_corse_list[(i+2) % len(main_corse_list) - 1]
                meal_group[2] = desert_list[(((i * 2) - 1)+1) % len(main_corse_list) - 1]

                print(meal_group[0].pairnr, meal_group[1].pairnr, meal_group[2].pairnr)

            """

            rout_group.append(meal_group)
        print("----------")
        all_meal_groups.append(rout_group)

    print("")
    print("")

    all_meal_groups = check_routs(all_meal_groups,org_pairs)

    print("--- Group schedule ---")
    for rout_group in all_meal_groups:
        print("---")
        for meal_group in rout_group:
            if len(meal_group) > 3:
                print(meal_group[0].pairnr,meal_group[1].pairnr,meal_group[2].pairnr, meal_group[3].pairnr)
            else:
                print(meal_group[0].pairnr,meal_group[1].pairnr,meal_group[2].pairnr)

    return all_meal_groups


# Check routs
def check_routs(all_meal_groups, pairs):

    painr = []
    for rout_group in all_meal_groups:
        for meal_group in rout_group:
            for pair in meal_group:
                painr.append(int(pair.pairnr))

    painr.sort()

    print("Amount of times a pair occurs in route",Counter(painr))

    s = []
    m = []
    i = 0
    for rout_group in all_meal_groups:

        if rout_group[2][2].pairnr == -1:
            s.append(rout_group[2][0])
            m.append(rout_group[2][1])
            del all_meal_groups[i][2]
        i += 1

    for sx in s:
        i = 0
        for rout_group in all_meal_groups:
            if len(rout_group) >= 3:
                desert = rout_group[2]
                if len(desert) <= 3:
                    if sx.pairnr != desert[0].pairnr and sx.pairnr != desert[1].pairnr and sx.pairnr != desert[2].pairnr:
                        if is_ok(all_meal_groups,sx,desert[0]) and is_ok(all_meal_groups,sx,desert[1]) and is_ok(all_meal_groups,sx,desert[2]):
                            all_meal_groups[i][2].append(sx)
                            break
            i += 1

    for sx in m:
        i = 0
        for rout_group in all_meal_groups:
            if len(rout_group) >= 3:
                desert = rout_group[2]
                if len(desert) <= 3:
                    if sx.pairnr != desert[0].pairnr and sx.pairnr != desert[1].pairnr and sx.pairnr != desert[2].pairnr:
                        if is_ok(all_meal_groups, sx, desert[0]) and is_ok(all_meal_groups, sx, desert[1]) and is_ok(
                                all_meal_groups, sx, desert[2]):
                            all_meal_groups[i][2].append(sx)
                            break
            i += 1

    pairs_prep_count = [0 for _ in range(len(pairs))]
    for rout_group in all_meal_groups:
        pairs_prep_count[int(rout_group[0][0].pairnr)-1] += 1
        pairs_prep_count[int(rout_group[1][1].pairnr)-1] += 1
        if len(rout_group) > 2:
            pairs_prep_count[int(rout_group[2][2].pairnr)-1] += 1

    print("Pair preperation count = ", pairs_prep_count)

    return all_meal_groups


def is_ok(all_meal_groups, pair1, pair2):
    for rout_group in all_meal_groups:
        for meal_group in rout_group:
            if (pair1.pairnr == meal_group[0].pairnr or pair1.pairnr == meal_group[1].pairnr or pair1.pairnr == meal_group[2].pairnr) and \
                    (pair2.pairnr == meal_group[0].pairnr or pair2.pairnr == meal_group[1].pairnr or pair2.pairnr == meal_group[2].pairnr):
                return False
    return True


# Help function for deciding routs
def group_placement(s, m, d, what_list):
    list1 = []
    list2 = []
    list3 = []

    if what_list == STARTER:
        list1 = s
        list2 = m
        list3 = d
    elif what_list == MAIN_COURSE:
        list1 = m
        list2 = d
        list3 = s
    elif what_list == DESERT:
        list1 = d
        list2 = s
        list3 = m

    group_group = []
    j = 0
    list1_index = 1
    list2_index = 2
    for i in list1:
        g = []
        g.append(i)

        if j + list1_index > len(list2) - 1:
            g.append(list2[len(list2) - 1 - j])
        else:
            g.append(list2[j + list1_index])

        if j + list2_index > len(list3) - 1:
            g.append(list3[len(list3) - list2_index - j])
        else:
            g.append(list3[j + list2_index])

        group_group.append(g)

        j += 1

    """
    prnr = []
    for g in group_group:
        for i in g:
            prnr.append(i.pairnr)

    print(Counter(prnr),len(prnr))

    """

    return group_group


def generate_schedule(all_meal_groups,start_time,meal_time,travel_time):

    for route_groups in all_meal_groups:
        i = 0
        for meal_group in route_groups:
            where_array = schedual_help(meal_group[i],all_meal_groups)
            where_array[i]=meal_group[i]

            amount_visit_pairs = find_visiting_pairs(meal_group[i], all_meal_groups)

            schedual_template(meal_group[i],where_array,amount_visit_pairs,start_time,meal_time,travel_time)

            i +=1

def find_visiting_pairs(pair, all_meal_groups):

    for rout_groups in all_meal_groups:
        i = 0

        for meal_group in rout_groups:
            if i + 1 == pair.tocook and meal_group[i] == pair:

                inval_group_count = 0
                for group in meal_group:
                    if group.pairnr == -1:
                        inval_group_count += 1

                amount_visit_pairs = len(meal_group) - 1 - inval_group_count

                return amount_visit_pairs

            i += 1

    return -1

def schedual_template(your_group,where_array,amount_of_pairs,start_time,meal_time,travel_time):

    A = ["Förrätt","Huvudrätt","Efterrätt"]

    formated_start_time = start_time.strftime("%H:%M, %d %b %Y")
    format_main_course_time = (start_time+meal_time+travel_time).strftime("%H:%M")
    format_desert_course_time = (start_time+2*meal_time+2*travel_time+datetime.timedelta(minutes=15)).strftime("%H:%M")

    template_text = """
Hejsan {20} och {21}!

{0} är det Cyckelfest!!

Cykelstyret höftar att man borde hinna på en halvtimme mellan måltider. Men vi rekomenderar att man kollar upp hur långt tid det kommer ta till nästa destination.

Ditt och din cykelkompis cykelschema:

Förrätt: {1} - Värd {2} - {3} kontakt till värd om ni inte kan koden till porten är eller liknade. Adress: {17}

30 min restid

Huvudrätt: {4} - Värd {5} - {6}. Adress: {18}

30 min restid

Efterrätt: {7} - Värd {8} - {9}. Adress: {19}

Ni ska servera följande rätt:  {10} och {22} par kommer.
Olika matgnäll: {11}, {12}, {13}
Behövs det ett alkoholfritt alternativ: {14}, {15}, {16}

Efterfest där och då vi säger på Facebook evenemanget.

För funderingar och frågor kontakta mats.gard@me.com

Med vänliga hälsningar,
Cykelstyret
""".format(
        formated_start_time,
        formated_start_time,where_array[0].name,where_array[0].phonenr,
        format_main_course_time,where_array[1].name,where_array[1].phonenr,
        format_desert_course_time,where_array[2].name,where_array[2].phonenr,
        A[your_group.tocook-1],
        where_array[0].alergy,where_array[1].alergy,where_array[2].alergy,
        where_array[0].alchol,where_array[1].alchol,where_array[2].alchol,
        where_array[0].adress,where_array[1].adress,where_array[2].adress,
        your_group.name, your_group.teammember, amount_of_pairs
    )

    file_name = your_group.pairnr
    f = open(file_name+".txt", "w")
    f.write(template_text)
    f.close()


def schedual_help(group_in,all_meal_groups):

    where_array = [None]*3
    i = 0
    for route_groups in all_meal_groups:
        j = 0
        for meal_group in route_groups:
            found_group = False
            for group in meal_group:
                if group == group_in:
                    found_group = True
                    break

            if found_group and group_in != meal_group[j]:
                where_array[j] = meal_group[j]

            j+=1
        i+=1

    return where_array

#Sends out email to all pairs with relation to their generated txt file and their pairnumber
def broadcast_emails(pairs):
    print("Broacast email function called")
    for p in pairs:

        try:
            txt_file = str(p.pairnr + ".txt")

            with open(txt_file, 'r') as file:
                message = file.read()

            send_email(p.email, "Cykelfesten närmar sig!", message)
        except:
            print("Something went wrong", p.name, p.pairnr)

def main():
    start_time = datetime.datetime(2020, 10, 9, 17, 0)
    meal_time = datetime.timedelta(minutes=60)
    travel_time = datetime.timedelta(minutes=30)

    pairs = Read_file("Test.csv")
    random.shuffle(pairs)

    pairs = decide_meal(pairs)



    all_meal_groups = decide_route(pairs)

    generate_schedule(all_meal_groups,start_time,meal_time,travel_time)

    """for rout_group in all_meal_groups:
        for meal_group in rout_group:
            if len(meal_group) > 3:
                print(meal_group[0].pairnr,meal_group[1].pairnr,meal_group[2].pairnr,meal_group[3].pairnr)
            else:
                print(meal_group[0].pairnr, meal_group[1].pairnr, meal_group[2].pairnr)
        print("___________")

    painr = []
    for rout_group in all_meal_groups:
        for meal_group in rout_group:
            for pair in meal_group:
                painr.append(int(pair.pairnr))

    painr.sort()

    print("Amount of times a pair occurs in route", Counter(painr))"""

    broadcast_emails(pairs)
    #send_email("max@idermark.com", "Cykelfest", "meddelande")

main()
