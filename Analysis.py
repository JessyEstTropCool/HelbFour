import FileReader

days = FileReader.days
products = FileReader.products

def main():
    filename = "HELBFour_2223_project_dataset.txt"
    lines_to_read = None
    #filename = "test.txt"

    print("Reading file...")

    frequencies = FileReader.read_transact(filename, lines_to_read)

    product_freq = frequencies[FileReader.total_prefix]
    year_freq = frequencies[FileReader.year_prefix]
    week_freq = frequencies[FileReader.week_prefix]
    day_freq = frequencies[FileReader.day_prefix]

    print("Done !")
    show_max_min(product_freq)
    compare_keys(day_freq, "day")
    compare_keys(week_freq, "week")
    compare_keys(year_freq, "year")

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

main()