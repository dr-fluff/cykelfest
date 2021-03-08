
NUM_MEALS = 3
FOD_INDEX_PRE_CORSE = 1
FOD_INDEX_MAIN_CORSE = 2
FOD_INDEX_DESERT = 3

pairs = []

class pair():

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
        self.food_index = tocook
        self.place1 = place1
        self.place2 = place2
        self.place3 = place3


# Sort The groups in random order
def create_groups(pairs):

    # TODO scramble the pair list


    for i in range(pairs):




    # while len(pairs) > 0:
    #     group = []
    #     if len(pairs) >= 3:
    #         group = [pairs[1],pairs[1],pairs[2]]
    #         pairs.remove(0,1,2)
    #         groups.append(group)
    #     else:
    #         for i in range(pairs):
    #             groups[i].append(pairs[0])
    #             pairs.remove(0)








# Write all groups to a file
def write_to_file(File_path):
    print("")


# Read all data from file
def read_from_file(File_path):
    print("")


# Send email to all groups
def send_email():
    print("")


def main():
    print("hej")
    file_path = ""

    read_from_file(file_path)

main()