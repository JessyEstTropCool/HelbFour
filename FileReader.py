import difflib
import threading
import time
import re
#from collections import Counter #to consider

def get_products():
    l = []

    for i in range(100):
        l.append("p_" + str(i + 1))

    return l

year_prefix = "YEAR:"
week_prefix = "WEEK:"
day_prefix = "DAY:"
total_prefix = "TOTAL"
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
products = get_products()

def waiting_anim(count: list, total: int):
    animation = "◤◥◢◣"
    idx = 0
    while count[0] != total:
        print(f"\r{animation[idx % len(animation)]} | lines done : {count[0]} / {total}", end="")
        idx += 1
        time.sleep(0.1)

    print(f"\r{animation[idx % len(animation)]} | lines done : {count[0]} / {total}")

def isevaluable(s):
    try:
        eval(s)
        return True
    except:
        return False

#TODO use setdefault method or counter class
def add_product(main_dict: dict, sub: list, other_dicts: list, keys: list):
    #éviter les doublons : si le toutes les valeurs ont pas des hash diff alors doublons
    # if len(sub) != len(set(sub)): 
    #     return None

    for item in sub:
        if item in main_dict:
            main_dict[item] = main_dict.setdefault(item, 0) + 1

            for i in range(len(other_dicts)):
                add_to_dict(other_dicts[i][keys[i]], item)
        else:
            #main_dict[item] = 1
            if item not in products:
                corr = difflib.get_close_matches(item, products, n=1, cutoff=0.6)

                if len(corr) > 0:
                    main_dict[corr[0]] = main_dict.setdefault(corr[0], 0) + 1

                    for i in range(len(other_dicts)):
                        add_to_dict(other_dicts[i][keys[i]], corr[0])
                else:
                    main_dict[item] = main_dict.setdefault(item, 0) + 1

                    for i in range(len(other_dicts)):
                        add_to_dict(other_dicts[i][keys[i]], item)

def add_to_dict(d:dict, item):
    if item in d:
        d[item] += 1
    else:
        d[item] = 1

def read_transact(filename: str, lines_to_read: int) -> dict:
    transact = open(filename, "r").readlines()

    if lines_to_read is None or lines_to_read > len(transact):
        lines_to_read = len(transact)

    day = None
    week = None
    year = None
    count = [0]
    prev_purchase = []
    product_freq = {}
    day_freq = {}
    week_freq = {}
    year_freq = {}

    threading.Thread(target=waiting_anim, kwargs={"count": count,"total": lines_to_read}).start()

    #for line in transact:
        #line = line.strip()
    for i in range(lines_to_read):
        line = transact[i].strip()
        count[0] += 1

        while line != "":
            # articles
            if line.startswith("["):

                #if year_prefix in line or week_prefix in line or day_prefix in line:
                    #print("Mixed line :" + line)

                #print(">" + line + "<")
                if "]" in line and ("[" not in line[1::] or line.index("[", 1) > line.index("]")):
                    array = line[:line.index("]") + 1:]
                    line = line[line.index("]") + 1::]

                    array = re.sub("[^p_0-9\s,'\[\]]", "", array)

                    if isevaluable(array):
                        purchase = eval(array)
                        if purchase != prev_purchase:
                            prev_purchase = purchase
                            add_product(
                                product_freq, 
                                purchase, 
                                [day_freq, week_freq, year_freq],
                                [day, week, year]
                            )
                            #print("ok")
                        #else:
                            #print("double")
                    #else:
                        #print("OW : " + array)

                    #print(array)
                    #print(">" + line + "<") 
                else:
                    #print("unfinished array : " + line)
                    line = ""
                
            else:
                if year_prefix in line:
                    year = line[line.index(year_prefix) + len(year_prefix):line.index("*"):]
                    line = line[line.rindex("*") + 1::] 

                    if year not in year_freq:
                        year_freq[year] = {}

                if week_prefix in line:
                    week = line[line.index(week_prefix) + len(week_prefix):line.index("+"):]
                    line = line[line.rindex("+") + 1::]

                    if week not in week_freq:
                        week_freq[week] = {}

                if day_prefix in line:
                    day = line[line.index(day_prefix) + len(day_prefix):line.index("-"):]

                    if day not in days:
                        corr = difflib.get_close_matches(day, days, n=1, cutoff=0.6)

                        #print("weird day : " + line + " -> corr = " + str(corr))
                        if len(corr) > 0:
                            day = corr[0]
                        else:
                            day = None

                    line = line[line.rindex("-") + 1::]

                    if day not in day_freq:
                        day_freq[day] = {}

                    
                if "]" in line and "[" not in line:
                    #print("only end to array: " + line)
                    line = "[" + line

                if line != "" and (not line.startswith(year_prefix) or not line.startswith(week_prefix) or not line.startswith(day_prefix)):
                    #print("weird start : " + line)
                    if "[" in line:
                        line = line[line.index("[")]
                    else:
                        line = ""
                    
                #print(str(year) + " / " + str(week) + " / " + str(day))
                #print(">" + line + "<")

    time.sleep(0.1)

    return {total_prefix: product_freq, day_prefix: day_freq, week_prefix: week_freq, year_prefix: year_freq}