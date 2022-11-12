import difflib
import threading
import time
import re

def compare_keys(frequencies: dict, subject: str):
    sums = {}

    for key, sub_freq in frequencies.items():
        sums[key] = sum(sub_freq.values())

    max_freq = max(sums, key=sums.get)
    min_freq = min(sums, key=sums.get)

    print("Best " + subject + " : " + max_freq + " - " + str(sums[max_freq]))
    print("Worst " + subject + " : " + min_freq + " - " + str(sums[min_freq]))

def show_max_min(frequencies: dict):
    max_freq = max(frequencies, key=frequencies.get)
    min_freq = min(frequencies, key=frequencies.get)
    total = sum(frequencies.values())

    print("Maximum : " + max_freq + " - " + str(frequencies[max_freq]))
    print("Minimum : " + min_freq + " - " + str(frequencies[min_freq]))
    print("Total : " + str(total))
    print("Values : " + str(frequencies))
    print("-" * 100)
    
def get_products():
    l = []

    for i in range(100):
        l.append("p_" + str(i + 1))

    return l

def waiting_anim(total: int):
    animation = "◤◥◢◣"
    idx = 0
    while count != total:
        print(f"\r{animation[idx % len(animation)]} | lines done : {count} / {total}", end="")
        idx += 1
        time.sleep(0.1)

    print(f"\r{animation[idx % len(animation)]} | lines done : {count} / {total}")

def isevaluable(s):
    try:
        eval(s)
        return True
    except:
        return False

#TODO use setdefault method or counter class
def add_product(main_dict: dict, sub: list, other_dicts: list, keys: list):
    #éviter les doublons : si le toutes les valeurs ont pas des hash diff alors doublons
    if len(sub) != len(set(sub)): 
        # if sub[0] in infline:
        #     infline[sub[0]] += len(sub)
        # else:
        #     infline[sub[0]] = len(sub)
        return None

    for item in sub:
        if item in products:
            main_dict[item] = main_dict.setdefault(item, 0) + 1

            for i in range(len(other_dicts)):
                add_to_dict(other_dicts[i][keys[i]], item)
        #else:
            #main_dict[item] = 1
            # if item not in products:
            #     corr = difflib.get_close_matches(item, products, n=1, cutoff=0.6)

            #     if len(corr) > 0:
            #         main_dict[corr[0]] = main_dict.setdefault(corr[0], 0) + 1

            #         for i in range(len(other_dicts)):
            #             add_to_dict(other_dicts[i][keys[i]], corr[0])
            #     else:
            #         main_dict[item] = main_dict.setdefault(item, 0) + 1

            #         for i in range(len(other_dicts)):
            #             add_to_dict(other_dicts[i][keys[i]], item)

def add_to_dict(d:dict, item):
    if item in d:
        d[item] += 1
    else:
        d[item] = 1

filename = "HELBFour_2223_project_dataset.txt"
# filename = "test.txt"
lines_to_read = None

print("Reading file...")

transact = open(filename, "r").readlines()

if lines_to_read is None or lines_to_read > len(transact):
    lines_to_read = len(transact)

year_prefix = "YEAR:"
week_prefix = "WEEK:"
day_prefix = "DAY:"
total_prefix = "TOTAL"
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
products = get_products()

day = None
week = None
year = None
count = 0
prev_purchase = []
product_freq = {}
day_freq = {}
week_freq = {}
year_freq = {}
#infline = {}

threading.Thread(target=waiting_anim, name="AnimThread", kwargs={"total": lines_to_read}).start()

for i in range(lines_to_read):
    line = transact[i].strip()
    count += 1

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

#print(str(infline))

new_dict = {}
keys = product_freq.keys()
for key in keys:
    if product_freq[key] > 1:
        new_dict[key] = product_freq[key]

print("Done !")
print(product_freq)
show_max_min(new_dict)
compare_keys(day_freq, "day")
compare_keys(week_freq, "week")
compare_keys(year_freq, "year")