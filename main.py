import csv

# Constants
TEAMNR = 0
NAME = 2
EMAIL = 3
PHONENR = 4
ADRESS = 5
ALERGY = 6
TEAMMEMBER = 7
MEAL = 8
MEAL1 = 9
MEAL2 = 10
MEAL3 = 11

# Read csv file and return a 2d array width person
def Read_file(File_path):
    peson = [""]
    persons = [[peson]]
    with open(File_path, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            peson = row
            list.append(persons, peson)

    return persons


# Send Email to everyone
def send_email(email_content):
    print(email_content)


# Decide all
def decide_meal(persons):

    adresses = [""]
    i = 0
    for p in persons:
        if len(p) < 10:
            print(i)
            p.remove(p.index())

        print(p)
        #list.append(adresses,p[ADRESS])
        i += 1

    print(adresses)

    return persons


# Decide everyone's route
def decide_route(p):
    list.append(p,2)

    return p


def main():
    persons = Read_file("../test.csv")

    persons = decide_meal(persons)

    persons = decide_route(persons)

main()
