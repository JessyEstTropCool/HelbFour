transact = open("transact_log.txt", "r")
year = None
week = None
day = None
article_day = {}
article_number = {}
customer = {}
#article_pairs = {}

def show_max_min(frequencies: dict):
    max_freq = max(frequencies, key=frequencies.get)
    min_freq = min(frequencies, key=frequencies.get)
    total = sum(frequencies.values())

    print("Maximum : " + max_freq + " - " + str(frequencies[max_freq]))
    print("Minimum : " + min_freq + " - " + str(frequencies[min_freq]))
    print("Total : " + str(total))
    print("Values : " + str(frequencies))
    print("-" * 100)

def show_percentage(frequencies: dict):
    maxf = max(frequencies, key=frequencies.get)
    minf = min(frequencies, key=frequencies.get)
    percent = (frequencies[maxf] / frequencies[minf] - 1) * 100

    print(maxf + " is " + str(round(percent, 2)) + "% more frequent than " + minf)
    print("-" * 100)

for line in transact:
    line = line.strip()

    # dates
    if not line.startswith("["):
        if line.startswith("YEAR"):
            year = line.replace("*", "")[line.index(":") + 1::]
        elif line.startswith("WEEK"):
            week = line.replace("+", "")[line.index(":") + 1::]
        elif line.startswith("DAY"):
            day = line.replace("-", "")[line.index(":") + 1::]
            
        #print(str(year) + " / " + str(week) + " / " + str(day))
        #print(line)

    # comptage
    else:
        if day not in article_day:
            article_day[day] = 0
            customer[day] = 0

        article_days_today = line.replace("\'", "").replace("[", "").replace("]", "").split(",")
        #print(len(article_days_today))

        article_day[day] += len(article_days_today)
        customer[day] += 1

        for article in article_days_today:
            article = article.strip()

            if article not in article_number:
                article_number[article] = 0

            article_number[article] += 1

print("Customers per day : ")
show_max_min(customer)

print("Articles bought per day : ")
show_max_min(article_day)

print("Articles bought per article : ")
show_max_min(article_number)

print("Customers per day : ")
show_percentage(customer)

print("Articles bought per day : ")
show_percentage(article_day)

print("Articles bought per article : ")
show_percentage(article_number)