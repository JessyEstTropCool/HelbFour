def compare_keys(frequencies: dict, subject: str):
    sums = {}

    for key, sub_freq in frequencies.items():
        sums[key] = sum(sub_freq.values())

    max_freq = max(sums, key=sums.get)
    min_freq = min(sums, key=sums.get)

    print("Best " + subject + " : " + str(max_freq) + " - " + str(sums[max_freq]))
    print("Worst " + subject + " : " + str(min_freq) + " - " + str(sums[min_freq]))
    print("-" * 100)

def compare_all_keys(frequencies: dict, subject: str):
    sums = {}

    for key, sub_freq in frequencies.items():
        sums[key] = sum(sub_freq.values())

    sums = {k: v for k, v in sorted(sums.items(), key=lambda item: item[1])}

    for key, value in sums.items():
        print(str(key) + " - " + str(value))

    print("-" * 100)

def show_top(number_to_show: int, frequencies: dict, subject: str):
    top10 = sorted(frequencies, key=frequencies.get, reverse=True)[:number_to_show]

    print(f"Top {number_to_show} {subject}")
    for key in top10:
        print(str(key) + " - " + str(frequencies[key]))

    print("-" * 100)

def show_all(frequencies: dict, subject: str):
    frequencies = {k: v for k, v in sorted(frequencies.items(), key=lambda item: item[1])}

    for key, value in frequencies.items():
        print(key + " - " + str(value))

    print("-" * 100)

def show_max_min(frequencies: dict):
    max_freq = max(frequencies, key=frequencies.get)
    min_freq = min(frequencies, key=frequencies.get)
    total = sum(frequencies.values())

    print("Maximum : " + max_freq + " - " + str(frequencies[max_freq]))
    print("Minimum : " + min_freq + " - " + str(frequencies[min_freq]))
    print("Total : " + str(total))
    #print("Values : " + str(frequencies))
    print("-" * 100)

def print_list(l: list):
    for i in l:
        print(i)
        #print("\"" + i + "\",")

def write_errors(errors: list, indexed_errors: list):
    err_file = open("errors.txt", "w")
    index_err_file = open("indexed_errors.txt", "w")

    for err in errors:
        err_file.write(err + "\n")

    for err in indexed_errors:
        index_err_file.write(err + "\n")

    err_file.close()
    index_err_file.close()