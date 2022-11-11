import difflib
import threading
import time
import re

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
    animation = "|/-\\"
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

def add_to_dict(d: dict, sub: list, date: dict):
    #éviter les doublons : si le toutes les valeurs ont pas des hash diff alors doublons
    if len(sub) != len(set(sub)): 
        return None

    for item in sub:
        if item in d:
            d[total_prefix][item] += 1
            d[day_prefix][date[day_prefix]][item] += 1
            d[week_prefix][date[week_prefix]][item] += 1
            d[year_prefix][date[year_prefix]][item] += 1
        else:
            #d[item] = 1
            if item not in products:
                corr = difflib.get_close_matches(item, products, n=1, cutoff=0.6)

                if len(corr) > 0:
                    d[total_prefix][corr[0]] = 1
                    d[day_prefix][date[day_prefix]][corr[0]] = 1
                    d[week_prefix][date[week_prefix]][corr[0]] = 1
                    d[year_prefix][date[year_prefix]][corr[0]] = 1
                else:
                    d[total_prefix][item] = 1
                    d[day_prefix][date[day_prefix]][item] = 1
                    d[week_prefix][date[week_prefix]][item] = 1
                    d[year_prefix][date[year_prefix]][item] = 1

def read_transact(filename: str) -> dict:
    date = {day_prefix:None, week_prefix:None, year_prefix:None}
    count = [0]
    prev_purchase = []
    product_freq = {day_prefix:{}, week_prefix:{}, year_prefix:{}, total_prefix:{}}

    transact = open(filename, "r").readlines()
    lines_to_read = 10000#len(open(filename, "r").readlines())

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
                            #print("ok")
                            prev_purchase = purchase
                            add_to_dict(product_freq, purchase, date)
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
                    date[year_prefix] = line[line.index(year_prefix) + len(year_prefix):line.index("*"):]
                    line = line[line.rindex("*") + 1::] 

                if week_prefix in line:
                    date[week_prefix] = line[line.index(week_prefix) + len(week_prefix):line.index("+"):]
                    line = line[line.rindex("+") + 1::]

                if day_prefix in line:
                    date[day_prefix] = line[line.index(day_prefix) + len(day_prefix):line.index("-"):]

                    if date[day_prefix] not in days:
                        corr = difflib.get_close_matches(date[day_prefix], days, n=1, cutoff=0.6)

                        #print("weird day : " + line + " -> corr = " + str(corr))
                        if len(corr) > 0:
                            date[day_prefix] = corr[0]
                        else:
                            date[day_prefix] = None

                    line = line[line.rindex("-") + 1::]

                    
                if "]" in line and "[" not in line:
                    #print("only end to array: " + line)
                    line = "[" + line

                if line != "" and (not line.startswith(year_prefix) or not line.startswith(week_prefix) or not line.startswith(day_prefix)):
                    #print("weird start : " + line)
                    if "[" in line:
                        line = line[line.index("[")]
                    else:
                        line = ""
                    
                #print(str(date[year_prefix]) + " / " + str(date[week_prefix]) + " / " + str(date[day_prefix]))
                #print(">" + line + "<")

    time.sleep(0.1)

    return product_freq