def compare_keys(frequencies: dict, subject: str):
    sums = {}

    for key, sub_freq in frequencies.items():
        sums[key] = sum(sub_freq.values())

    max_freq = max(sums, key=sums.get)
    min_freq = min(sums, key=sums.get)

    print("Best " + subject + " : " + max_freq + " - " + str(sums[max_freq]))
    print("Worst " + subject + " : " + min_freq + " - " + str(sums[min_freq]))
    print("-" * 100)

def compare_all_keys(frequencies: dict, subject: str):
    sums = {}

    for key, sub_freq in frequencies.items():
        sums[key] = sum(sub_freq.values())

    sums = {k: v for k, v in sorted(sums.items(), key=lambda item: item[1])}

    for key, value in sums.items():
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