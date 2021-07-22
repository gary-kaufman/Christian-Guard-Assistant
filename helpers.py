from math import floor
from random import shuffle

def get_roles(p_count):
    
    temp_guard_num = round(int(p_count) * .3)  # 30% creates the total Guard Number
    c_g_num = floor(temp_guard_num / 5)  # 1 Christian Guard for every 5 Guards
    if temp_guard_num < 5:
        c_g_num = 1

    guard_num = temp_guard_num - c_g_num

    christian_num = int(p_count) - int(temp_guard_num)  # Remaining players are Christians

    roles = []

    for item in range(c_g_num):
        roles.append("Christian Guard")

    for item in range(guard_num):
        roles.append("Guard")

    for item in range(christian_num):
        roles.append("Christian")

    shuffle(roles)

    print("Total players: {}\nGuards: {}\nChristians: {}\nChristian Guards: {}".format(p_count, guard_num, christian_num, c_g_num))
    print(roles)

    return roles


def check_name(name):
    # Check if name is empty
    if name == "":
        return False
        
    # Check if name has any numbers
    for item in name:
        if item.isdigit():
            return False

    return True
